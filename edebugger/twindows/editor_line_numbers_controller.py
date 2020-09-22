import gtk

from edebugger.twindows.editor_text_window_controller import EditorTextWindowController
from edebugger.twindows.editor_line_numbers_element import EditorLineNumbersElement


class EditorLineNumbersController(EditorTextWindowController):
    def __init__(self, p_text_win, p_view):
        EditorTextWindowController.__init__(self, gtk.gdk.EXPOSURE_MASK |
                                               gtk.gdk.BUTTON_PRESS_MASK)

        doc = p_view.get_buffer()
        doc.connect("changed", self.__on_document_changed, p_text_win, p_view)

        p_view.connect("style-set", self.__on_view_style_set, p_text_win)

        if p_view.has_screen():
            self.__update_text_window_width(p_text_win, p_view)
        else:
            p_view.connect("realize", self.__on_view_realize, p_text_win)

    def handle_event(self, p_event, p_text_win, p_view):
        if p_event.window != p_view.get_window(p_text_win.get_type()):
            return

        if p_event.type == gtk.gdk.EXPOSE:
            self.__handle_expose_event(p_event, p_text_win, p_view)
        elif p_event.type == gtk.gdk.BUTTON_PRESS:
            self.__handle_button_press_event(p_event, p_text_win, p_view)

    def __handle_expose_event(self, p_event, p_text_win, p_view):
        win_type = p_text_win.get_type()

        if not p_text_win.width:           # Lo mejor en este caso seria
            p_view.update_window(win_type) # dibujar completo, pero solo
            return                         # a p_text_win y NO hacer un update

        intersect = p_event.area.intersect(p_text_win)
        if not intersect.width:
            return

        elements = p_text_win.get_elements()
        del elements[:]

        first_y = intersect.y
        last_y = first_y + intersect.height

        x, first_y = p_view.window_to_buffer_coords(win_type, 0, first_y)
        x, last_y = p_view.window_to_buffer_coords(win_type, 0, last_y)

        numbers = []
        pixels = []
        heights = []

        iter_, top = p_view.get_line_at_y(first_y)

        while True:
            y, height = p_view.get_line_yrange(iter_)
            pixels.append(y)
            heights.append(height)
            numbers.append(iter_.get_line())

            if iter_.is_end() or (y + height) >= last_y:
                break
            iter_.forward_line()

        layout = p_view.create_pango_layout("")
        win_size = p_text_win.get_size()
        doc = p_view.get_buffer()
        curline = doc.get_iter_at_mark(doc.get_insert()).get_line() + 1

        for i in xrange(len(numbers)):
            x, pos = p_view.buffer_to_window_coords(win_type, 0, pixels[i])
            height = heights[i]
            num = numbers[i] + 1
            bold = num == curline

            elem = EditorLineNumbersElement(0, pos, win_size, height, num,
                                           layout, bold, win_type, win_size)
            elements.append(elem)

    def __handle_button_press_event(self, p_event, p_text_win, p_view):
        if p_event.button != 1:
            return

        if not (p_text_win.x <= p_event.x < p_text_win.x + p_text_win.width):
            return

        x, y = p_view.window_to_buffer_coords(p_text_win.get_type(),
                                     int(p_event.x), int(p_event.y))
        iter_, top = p_view.get_line_at_y(y)
        p_view.get_buffer().place_cursor(iter_)
        p_view.scroll_to_cursor(0.0)

    def __update_text_window_width(self, p_text_win, p_view):
        doc = p_view.get_buffer()
        layout = p_view.create_pango_layout("00")
        minwidth, height = layout.get_pixel_size()

        layout.set_text("0" * len(str(doc.get_line_count())))
        curwidth, height = layout.get_pixel_size()

        width = max(minwidth, curwidth) + 6

        if width != p_text_win.get_size():
            p_text_win.set_size(width)
            p_view.update_window(p_text_win.get_type())

    def __on_document_changed(self, p_doc, p_text_win, p_view):
        self.__update_text_window_width(p_text_win, p_view)

    def __on_view_style_set(self, p_view, p_previous_style, p_text_win):
        if p_previous_style:
            presize = p_previous_style.font_desc.get_size()
            cursize = p_view.get_style().font_desc.get_size()

            if presize != cursize:
                self.__update_text_window_width(p_text_win, p_view)

    def __on_view_realize(self, p_view, p_text_win):
        self.__update_text_window_width(p_text_win, p_view)
