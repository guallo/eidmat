import gtk
import pango

from edebugger.twindows.editor_text_window_controller import EditorTextWindowController
from edebugger.twindows.editor_arrow_element import EditorArrowElement


class EditorArrowsController(EditorTextWindowController):
    def __init__(self, p_text_win, p_view):
        EditorTextWindowController.__init__(self, gtk.gdk.EXPOSURE_MASK)

        self.__text_win = p_text_win
        self.__view = p_view
        self.__lines = []
        self.__current = False

        p_view.connect("style-set", self.__on_view_style_set, p_text_win)

        if p_view.has_screen():
            self.__update_text_window_width(p_text_win, p_view)
        else:
            p_view.connect("realize", self.__on_view_realize, p_text_win)

    def set_lines(self, p_lines):
        self.__lines = p_lines

    def set_current(self, p_current):
        self.__current = p_current

    def handle_event(self, p_event, p_text_win, p_view):
        if p_event.window != p_view.get_window(p_text_win.get_type()):
            return

        if p_event.type == gtk.gdk.EXPOSE:
            self.__handle_expose_event(p_event, p_text_win, p_view)

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
        arrows = self.__lines

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
        current = arrows[0] if self.__current else None

        for i in xrange(len(numbers)):
            num = numbers[i] + 1

            if num in arrows:
                x, pos = p_view.buffer_to_window_coords(win_type, 0, pixels[i])
                height = heights[i]
                is_current = num == current

                elem = EditorArrowElement(0, pos, win_size, height, win_type, is_current)
                elements.append(elem)

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
