from edebugger.twindows.editor_text_window_element import EditorTextWindowElement


class EditorBreakpointsElement(EditorTextWindowElement):
    def __init__(self, p_x, p_y, p_width, p_height, p_synced, p_semi):
        EditorTextWindowElement.__init__(self, p_x, p_y, p_width, p_height)

        self.__synced = p_synced
        self.__semi = p_semi

    def draw(self, p_drawable):
        gc = p_drawable.new_gc()
        hex_ = "#ff6161" if self.__synced else "#808080"
        fill = gc.get_colormap().alloc_color(hex_)
        border = gc.get_colormap().alloc_color("#000000")

        width, height = self.get_geometry()[2:]
        w = int(min(width, height) * 0.53)
        h = int(0.6 * w) if self.__semi else w
        x = (width - w) / 2
        y = (height - h) / 2

        gc.set_foreground(fill)
        p_drawable.draw_arc(gc, True, x, y, w, h, 0, 360 * 64)

        gc.set_foreground(border)
        p_drawable.draw_arc(gc, False, x, y, w, h, 0, 360 * 64)
