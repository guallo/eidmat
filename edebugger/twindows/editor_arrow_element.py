import gtk

from edebugger.twindows.editor_text_window_element import EditorTextWindowElement


class EditorArrowElement(EditorTextWindowElement):
    def __init__(self, p_x, p_y, p_width, p_height, p_win_type, p_is_current):
        EditorTextWindowElement.__init__(self, p_x, p_y, p_width, p_height)

        self.__win_type = p_win_type
        self.__is_current = p_is_current

    def draw(self, p_drawable):
        gc = p_drawable.new_gc()
        hex_ = "#00FF00" if self.__is_current else "#FFFFFF"
        fill = gc.get_colormap().alloc_color(hex_)
        border = gc.get_colormap().alloc_color("#000000")

        width, height = self.get_geometry()[2:]
        square = int(min(width, height) * 0.56)  # change here
        left = (width - square) / 2  # change here
        right = left + square
        top = (height - square) / 2  # change here
        bottom = top + square
        x_center = (left + right) / 2
        y_center = (top + bottom) / 2
        arrow_top = int(top + 0.25 * square)
        arrow_bottom = int(top + 0.75 * square)

        points = []
        if self.__win_type == gtk.TEXT_WINDOW_LEFT:
            points.append((left, arrow_bottom))
            points.append((left, arrow_top))
            points.append((x_center, arrow_top))
            points.append((x_center, top))
            points.append((right, y_center))
            points.append((x_center, bottom))
            points.append((x_center, arrow_bottom))
        else:
            points.append((right, arrow_bottom))
            points.append((right, arrow_top))
            points.append((x_center, arrow_top))
            points.append((x_center, top))
            points.append((left, y_center))
            points.append((x_center, bottom))
            points.append((x_center, arrow_bottom))

        gc.set_foreground(fill)
        p_drawable.draw_polygon(gc, True, points)

        gc.set_foreground(border)
        p_drawable.draw_polygon(gc, False, points)
