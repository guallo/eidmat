import gtk
import pango

from edebugger.twindows.editor_text_window_controller import EditorTextWindowController
from edebugger.twindows.editor_breakpoints_element import EditorBreakpointsElement


CLICK_INFO = "CLICK_INFO"


class EditorBreakpointsController(EditorTextWindowController):
    def __init__(self, p_text_win, p_view):
        EditorTextWindowController.__init__(self, gtk.gdk.EXPOSURE_MASK |
                                            gtk.gdk.POINTER_MOTION_MASK |
                                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                                            gtk.gdk.BUTTON_PRESS_MASK |
                                            gtk.gdk.BUTTON_RELEASE_MASK)

        self.__text_win = p_text_win
        self.__view = p_view
        self.__lines = []
        self.__synced = False
        self.__locked = True

        p_view.connect("style-set", self.__on_view_style_set, p_text_win)

        if p_view.has_screen():
            self.__update_text_window_width(p_text_win, p_view)
        else:
            p_view.connect("realize", self.__on_view_realize, p_text_win)

    def set_lines(self, p_lines):
        self.__lines = p_lines

    def set_synced(self, p_synced):
        self.__synced = p_synced

    def set_locked(self, p_locked):
        self.__locked = p_locked

        if p_locked:
            self.set_data(CLICK_INFO, None)

    def handle_event(self, p_event, p_text_win, p_view):
        if p_event.window != p_view.get_window(p_text_win.get_type()):
            return

        if p_event.type == gtk.gdk.EXPOSE:
            self.__handle_expose_event_for_motion_and_scroll(p_event, p_text_win, p_view)
            self.__handle_expose_event(p_event, p_text_win, p_view)
        elif p_event.type == gtk.gdk.BUTTON_PRESS:
            self.__handle_button_press_event(p_event, p_text_win, p_view)
        elif p_event.type == gtk.gdk.BUTTON_RELEASE:
            self.__handle_button_release_event(p_event, p_text_win, p_view)
        elif p_event.type == gtk.gdk.MOTION_NOTIFY:
            if p_text_win.get_type() == gtk.TEXT_WINDOW_RIGHT:
                self.__handle_motion_notify_event(p_event, p_text_win, p_view)

    def __handle_button_press_event(self, p_event, p_text_win, p_view):
        if self.__locked:
            return

        if p_event.button != 1:
            return

        if not self.__x_is_inside_of_window(p_event.x):
            return

        line = self.__get_line_of_y(p_event.y)
        if not line:
            return

        info = {"line": line, "show": True}
        self.set_data(CLICK_INFO, info)
        self.__update_window()

    def __handle_button_release_event(self, p_event, p_text_win, p_view):
        if p_event.button != 1:
            return

        info = self.get_data(CLICK_INFO)

        if info:
            if self.__x_is_inside_of_window(p_event.x):
                line = self.__get_line_of_y(p_event.y)

                if line == info["line"]:
                    if line in self.__lines:
                        p_view.emit("breakpoint_clear_request", line)
                    else:
                        p_view.emit("breakpoint_set_request", line)

            showing = info["show"]
            self.set_data(CLICK_INFO, None)

            if showing:
                self.__update_window()

    def __handle_motion_notify_event(self, p_event, p_text_win, p_view):
        info = self.get_data(CLICK_INFO)

        if not info:
            return

        show = self.__x_is_inside_of_window(p_event.x) and \
               self.__get_line_of_y(p_event.y) == info["line"]

        if info["show"] != show:
            info["show"] = show
            self.__update_window()

    def __handle_expose_event_for_motion_and_scroll(self, p_event, p_text_win, p_view):
        info = self.get_data(CLICK_INFO)

        if not info:
            return

        p_event_x, p_event_y = p_event.window.get_pointer()[:2]

        show = self.__x_is_inside_of_window(p_event_x) and \
               self.__get_line_of_y(p_event_y) == info["line"]

        if info["show"] != show:
            info["show"] = show
            self.__update_window()

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
        breakpoints = self.__lines

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
        synced = self.__synced
        info = self.get_data(CLICK_INFO)
        show = info["show"] if info else False

        for i in xrange(len(numbers)):
            num = numbers[i] + 1
            has_breakpoint = num in breakpoints
            has_semi = show and num == info["line"]

            if has_breakpoint or has_semi:
                x, pos = p_view.buffer_to_window_coords(win_type, 0, pixels[i])
                height = heights[i]

                if has_breakpoint:
                    elem = EditorBreakpointsElement(0, pos, win_size, height, synced, False)
                    elements.append(elem)

                if has_semi:
                    elem = EditorBreakpointsElement(0, pos, win_size, height, synced, True)
                    elements.append(elem)

                    show = False

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

    def __x_is_inside_of_window(self, p_x):
        text_win = self.__text_win
        return (text_win.x <= p_x < text_win.x + text_win.width)

    def __get_line_of_y(self, p_y):
        view = self.__view
        text_win = self.__text_win

        buff_x, buff_y = view.window_to_buffer_coords(text_win.get_type(),
                                                            0, int(p_y))
        iter_, y = view.get_line_at_y(buff_y)
        y, height = view.get_line_yrange(iter_)

        if (y <= buff_y < y + height):
            return iter_.get_line() + 1
        return None
