import gtk

from edebugger.twindows.editor_text_window_element import EditorTextWindowElement


class EditorLineNumbersElement(EditorTextWindowElement):
    def __init__(self, p_x, p_y, p_width, p_height, p_num, p_layout,
                        p_bold, p_text_win_type, p_text_win_size):
        EditorTextWindowElement.__init__(self, p_x, p_y, p_width, p_height)

        self.__num = p_num
        self.__layout = p_layout
        self.__bold = p_bold
        self.__text_win_type = p_text_win_type
        self.__text_win_size = p_text_win_size

    def draw(self, p_drawable):
        layout = self.__layout
        text = "<b>%d</b>" if self.__bold else "%d"

        layout.set_markup(text %self.__num)

        if self.__text_win_type == gtk.TEXT_WINDOW_LEFT:
            width, height = layout.get_pixel_size()
            x = self.__text_win_size - 3 - width
        else:
            x = 3

        gc = p_drawable.new_gc()
        color = gc.get_colormap().alloc_color("#000000")

        gc.set_foreground(color)
        p_drawable.draw_layout(gc, x, 0, layout, None, None)
