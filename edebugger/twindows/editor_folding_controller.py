import gtk
import pango

from edebugger.twindows.editor_text_window_controller import EditorTextWindowController
from edebugger.twindows.editor_folding_element import EditorFoldingElement, EditorFoldingElementType


class EditorFoldingController(EditorTextWindowController):
    def __init__(self, p_holder, p_text_win, p_view):
        EditorTextWindowController.__init__(self, gtk.gdk.EXPOSURE_MASK |
                                               gtk.gdk.BUTTON_PRESS_MASK)

        self.__holder = p_holder
        self.__text_win = p_text_win
        self.__view = p_view

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

        if not p_text_win.width:    # Lo mejor en este caso seria
            self.__update_window()  # dibujar completo, pero solo
            return                  # a p_text_win y NO hacer un update

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

        win_size = p_text_win.get_size()

        for i in xrange(len(numbers)):
            x, pos = p_view.buffer_to_window_coords(win_type, 0, pixels[i])
            height = heights[i]

            types = self.__get_element_types_of_line(numbers[i])
            for type_ in types:
                elem = EditorFoldingElement(0, pos, win_size, height, win_type, type_)
                elements.append(elem)

    def __get_element_types_of_line(self, p_line):
        def get_types(p_block, p_line):
            if not p_block.intersect_line(p_line):
                return []
            line1, line3 = p_block.get_line_bounds()
            if p_block.is_collapsed():
                if p_line == line1:
                    return [EditorFoldingElementType.COLLAPSED]
                return []
            types = []
            if p_line == line1:
                types.append(EditorFoldingElementType.EXPANDED)
            elif p_line == line3:
                types.append(EditorFoldingElementType.END_DELIMITER)
            else:
                types.append(EditorFoldingElementType.LINE)
            for block in p_block.get_blocks():
                types.extend(get_types(block, p_line))
            return types

        element_types = []
        for block in self.__holder:
            element_types.extend(get_types(block, p_line))
        return element_types

    def __handle_button_press_event(self, p_event, p_text_win, p_view):
        if p_event.button != 1:
            return

        if not (p_text_win.x <= p_event.x < p_text_win.x + p_text_win.width):
            return

        buff_x, buff_y = p_view.window_to_buffer_coords(p_text_win.get_type(),
                                     int(p_event.x), int(p_event.y))
        iter_, y = p_view.get_line_at_y(buff_y)
        y, height = p_view.get_line_yrange(iter_)

        if not (y <= buff_y < y + height):
            return
        p_view.emit("fold_toggle_request", iter_.get_line() + 1)

    def __update_text_window_width(self, p_text_win, p_view):
        font_size = p_view.get_style().font_desc.get_size() / pango.SCALE
        to_have = int(font_size * 1.7)

        if p_text_win.get_size() != to_have:
            p_text_win.set_size(to_have)
            self.__update_window()

    def __on_view_style_set(self, p_view, p_previous_style, p_text_win):
        if p_previous_style:
            presize = p_previous_style.font_desc.get_size()
            cursize = p_view.get_style().font_desc.get_size()

            if presize != cursize:
                self.__update_text_window_width(p_text_win, p_view)

    def __on_view_realize(self, p_view, p_text_win):
        self.__update_text_window_width(p_text_win, p_view)

    def __update_window(self):
        self.__view.update_window(self.__text_win.get_type())
