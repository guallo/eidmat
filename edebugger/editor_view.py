import gtk
import pango
import gobject
import gtksourceview2

from edebugger.editor_document import EditorDocument  # Solo para tipo.
from edebugger.twindows.editor_text_window import EditorTextWindow
#from edebugger.twindows.editor_text_window_element import EditorTextWindowElement
#from edebugger.twindows.editor_text_window_controller import EditorTextWindowController
from edebugger.twindows.editor_text_window_holder import EditorTextWindowHolder
from edebugger.twindows.editor_line_numbers_controller import EditorLineNumbersController


EDITOR_VIEW_SCROLL_MARGIN = 0.02


class EditorView(gtksourceview2.View):
    """
        Clase que representa la vista de un EditorDocument.
    """

    __gsignals__ = {"breakpoint_set_request":   (gobject.SIGNAL_RUN_LAST,
                                                 gobject.TYPE_NONE,
                                                 (int, )),
                    "breakpoint_clear_request": (gobject.SIGNAL_RUN_LAST,
                                                 gobject.TYPE_NONE,
                                                 (int, )),
                    "fold_toggle_request":      (gobject.SIGNAL_RUN_LAST,
                                                 gobject.TYPE_NONE,
                                                 (int, ))
                   }

    def __init__(self, p_doc):
        """
            p_doc:   un EditorDocument.

            Retorna: un EditorView.

            Crea un nuevo EditorView.
        """

        assert (type(p_doc) == EditorDocument)

        gtksourceview2.View.__init__(self, p_doc)

        self.connect("expose-event", self.on_expose_event)
        self.connect("event", self.on_event)

        self.__holder = EditorTextWindowHolder()
        self.__event_mask = {gtk.TEXT_WINDOW_LEFT: None,
                             gtk.TEXT_WINDOW_RIGHT: None,
                             gtk.TEXT_WINDOW_TOP: None,
                             gtk.TEXT_WINDOW_BOTTOM: None}

        self.modify_font(pango.FontDescription("monospace Expanded 10"))
        self.set_show_line_numbers(True)
        self.set_highlight_current_line(True)
        self.set_right_margin_position(79)
        self.set_show_right_margin(True)
        self.set_smart_home_end(True)
        self.set_insert_spaces_instead_of_tabs(True)
        self.set_tab_width(4)

        #self.__holder.append(EditorTextWindow("line", gtk.TEXT_WINDOW_LEFT, 1, 1, gtk.gdk.Color("#ffffff"), []),
        #                     EditorTextWindowController(gtk.gdk.EXPOSURE_MASK))
        #self.__holder.append(EditorTextWindow("margin", gtk.TEXT_WINDOW_LEFT, 3, 11, gtk.gdk.Color("#ffffff"), []),
        #                     EditorTextWindowController(gtk.gdk.EXPOSURE_MASK))

        #self.__holder.append(EditorTextWindow("top", gtk.TEXT_WINDOW_TOP, 0, 10, gtk.gdk.Color("yellow"), []),
        #                     EditorTextWindowController(gtk.gdk.EXPOSURE_MASK))
        #self.__holder.append(EditorTextWindow("top2", gtk.TEXT_WINDOW_TOP, -1, 16, gtk.gdk.Color("red"), [EditorTextWindowElement(20, 6, 5, 5)]),
        #                     EditorTextWindowController(gtk.gdk.EXPOSURE_MASK))
        #self.__holder.append(EditorTextWindow("right", gtk.TEXT_WINDOW_RIGHT, 0, 11, gtk.gdk.Color("green"), []),
        #                     EditorTextWindowController(gtk.gdk.EXPOSURE_MASK))
        #self.__holder.append(EditorTextWindow("bottom", gtk.TEXT_WINDOW_BOTTOM, 0, 5, gtk.gdk.Color("blue"), []),
        #                     EditorTextWindowController(gtk.gdk.EXPOSURE_MASK))
        #self.update_window(gtk.TEXT_WINDOW_LEFT)
        #self.update_window(gtk.TEXT_WINDOW_RIGHT)
        #self.update_window(gtk.TEXT_WINDOW_TOP)
        #self.update_window(gtk.TEXT_WINDOW_BOTTOM)

    def scroll_to_cursor(self, p_margin=0.25):
        """
            p_margin: un float en el intervalo [0.0, 0.5).

            Mueve la vista hasta que el cursor quede visible
            con un margen de p_margin.
        """

        assert (type(p_margin) == float and 0.0 <= p_margin < 0.5)

        mark = self.get_buffer().get_insert()

        self.scroll_to_mark(mark, p_margin, False, 0.0, 0.0)

    def undo(self):
        """
            Deshace la ultima accion realizada en el documento asociado.
        """

        self.get_buffer().undo()
        self.scroll_to_cursor()

    def redo(self):
        """
            Rehace la ultima accion desecha en el documento asociado.
        """

        self.get_buffer().redo()
        self.scroll_to_cursor()

    def cut_clipboard(self):
        """
            Corta el texto seleccionado en el documento asociado.
        """

        clipboard = gtk.Window().get_clipboard(gtk.gdk.SELECTION_CLIPBOARD)

        self.get_buffer().cut_clipboard(clipboard, True)
        self.scroll_to_cursor(EDITOR_VIEW_SCROLL_MARGIN)

    def copy_clipboard(self):
        """
            Copia el texto seleccionado en el documento asociado.
        """

        clipboard = gtk.Window().get_clipboard(gtk.gdk.SELECTION_CLIPBOARD)

        self.get_buffer().copy_clipboard(clipboard)
        # no hacer scroll

    def paste_clipboard(self):
        """
            Pega el contenido del clipboard en el documento asociado.
        """

        clipboard = gtk.Window().get_clipboard(gtk.gdk.SELECTION_CLIPBOARD)

        self.get_buffer().paste_clipboard(clipboard, None, True)
        self.scroll_to_cursor(EDITOR_VIEW_SCROLL_MARGIN)

    def delete_selection(self):
        """
            Elimina el texto seleccionado en el documento asociado.
        """

        self.get_buffer().delete_selection(True, True)
        self.scroll_to_cursor(EDITOR_VIEW_SCROLL_MARGIN)

    def select_all(self):
        """
            Selecciona todo el texto en el documento asociado.
        """

        doc = self.get_buffer()

        doc.select_range(*doc.get_bounds())
        # no hacer scroll

    def set_show_line_numbers(self, p_show):
        #FIXME: documentacion

        holder = self.__holder
        exist = holder.exist_window_of_name("Line Numbers")

        if p_show and not exist:
            win = EditorTextWindow("Line Numbers", gtk.TEXT_WINDOW_LEFT,
                                    0, 1, gtk.gdk.Color("#EFEBE7"), [])
            ctrl = EditorLineNumbersController(win, self)
            holder.append(win, ctrl)
            self.update_window(win.get_type())
        elif not p_show and exist:
            win = holder.get_window_of_name("Line Numbers")[0]
            holder.remove(win)
            self.update_window(win.get_type())

    def get_window_holder(self):
        return self.__holder

    def update_window(self, p_type):
        #FIXME: documentacion

        windows = self.__holder.get_windows_of_type(p_type)
        size = 0
        event_mask = 0

        for win, ctrl in windows:
            size += win.get_size()
            event_mask |= ctrl.get_event_mask()

        window = self.get_window(p_type)

        if window:
            window.set_events(event_mask)
        elif size:
            self.__event_mask[p_type] = event_mask

        if self.get_border_window_size(p_type) == size:
            if window:
                width, height = window.get_size()
                window.invalidate_rect(gtk.gdk.Rectangle(0, 0, width, height),
                                       True)
        else:
            self.set_border_window_size(p_type, size)

    def on_expose_event(self, p_view, p_event):
        #FIXME: documentacion

        types = (gtk.TEXT_WINDOW_LEFT, gtk.TEXT_WINDOW_RIGHT,
                 gtk.TEXT_WINDOW_TOP, gtk.TEXT_WINDOW_BOTTOM)
        flag = False
        window = p_event.window

        for type_ in types:
            if window == self.get_window(type_):
                flag = True
                break

        if not flag:
            return False

        event_mask = self.__event_mask[type_]
        if event_mask != None:
            window.set_events(event_mask)
            self.__event_mask[type_] = None

        windows = self.__holder.get_windows_of_type(type_)
        size = 0

        for win, ctrl in windows:
            size += win.get_size()

        self.set_border_window_size(type_, size)

        if not size:
            return True

        width, height = window.get_size()
        x = y = 0
        gc = window.new_gc()
        vertical = type_ in (gtk.TEXT_WINDOW_LEFT, gtk.TEXT_WINDOW_RIGHT)

        for win, ctrl in windows:
            size = win.get_size()
            draw = ctrl.get_event_mask() & gtk.gdk.EXPOSURE_MASK

            if vertical:
                win.x, win.y, win.width, win.height = x, 0, size, height
                x += size
            else:
                win.x, win.y, win.width, win.height = 0, y, width, size
                y += size

            if draw:
                color = gc.get_colormap().alloc_color(win.get_bg_color())
                gc.set_foreground(color)
                win_pix = gtk.gdk.Pixmap(window, win.width, win.height, -1)
                win_pix.draw_rectangle(gc, True, 0, 0, win.width, win.height)

                for elem in win.get_elements():
                    xelem, yelem, welem, helem = elem.get_geometry()
                    if welem < 1 or helem < 1:  # FIXME: quitar estas 2 lineas y poner un
                        continue                # assert en EditorTextWidowElement.__init__ ???
                    pixmap = gtk.gdk.Pixmap(window, welem, helem, -1)
                    pixmap.draw_drawable(gc, win_pix, xelem, yelem, 0, 0, welem, helem)
                    elem.draw(pixmap)
                    win_pix.draw_drawable(gc, pixmap, 0, 0, xelem, yelem, welem, helem)

                window.draw_drawable(gc, win_pix, 0, 0, win.x, win.y, win.width, win.height)

        return True

    def on_event(self, p_view, p_event):
        if p_event.type == gtk.gdk.EXPOSE:
            types = (gtk.TEXT_WINDOW_LEFT, gtk.TEXT_WINDOW_RIGHT,
                     gtk.TEXT_WINDOW_TOP, gtk.TEXT_WINDOW_BOTTOM)
            window = p_event.window

            for type_ in types:
                if window == self.get_window(type_):
                    windows = self.__holder.get_windows_of_type(type_)
                    width, height = window.get_size()

                    if type_ in (gtk.TEXT_WINDOW_LEFT, gtk.TEXT_WINDOW_RIGHT):
                        for win, ctrl in windows:
                            win.height = height
                    else:
                        for win, ctrl in windows:
                            win.width = width

                    break

        for win, ctrl in self.__holder:
            ctrl.handle_event(p_event, win, self)
