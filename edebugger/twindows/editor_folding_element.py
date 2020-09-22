import gtk

from edebugger.twindows.editor_text_window_element import EditorTextWindowElement


class EditorFoldingElementType:
    (EXPANDED,
    COLLAPSED,
    LINE,
    END_DELIMITER,
    ) = xrange(4)


class EditorFoldingElement(EditorTextWindowElement):
    def __init__(self, p_x, p_y, p_width, p_height, p_win_type, p_type):
        EditorTextWindowElement.__init__(self, p_x, p_y, p_width, p_height)

        self.__win_type = p_win_type
        self.__type = p_type

    def draw(self, p_drawable):
        gc = p_drawable.new_gc()
        fill = gc.get_colormap().alloc_color("#FFFFFF")
        border = gc.get_colormap().alloc_color("#666666")

        width, height = self.get_geometry()[2:]
        square = int(min(width, height) * 0.53)  # change here
        left = (width - square) / 2  # change here
        right = left + square
        top = (height - square) / 2  # change here
        bottom = top + square
        x_center = (left + right) / 2
        y_center = (top + bottom) / 2

        if self.__type in (EditorFoldingElementType.EXPANDED,
                           EditorFoldingElementType.COLLAPSED):
            points = []
            points.append((left, bottom))
            points.append((left, top))
            points.append((right, top))
            points.append((right, bottom))

            gc.set_foreground(fill)
            p_drawable.draw_polygon(gc, True, points)
            gc.set_foreground(border)
            p_drawable.draw_polygon(gc, False, points)

            x1 = int(left + 0.25 * square)
            x2 = int(left + 0.75 * square)
            p_drawable.draw_line(gc, x1, y_center, x2, y_center)

            if self.__type == EditorFoldingElementType.EXPANDED:
                p_drawable.draw_line(gc, x_center, bottom, x_center, height)
            else:
                y1 = int(top + 0.25 * square)
                y2 = int(top + 0.75 * square)
                p_drawable.draw_line(gc, x_center, y1, x_center, y2)
        elif self.__type == EditorFoldingElementType.LINE:
            gc.set_foreground(border)
            p_drawable.draw_line(gc, x_center, 0, x_center, height)
        else:
            gc.set_foreground(border)
            p_drawable.draw_line(gc, x_center, 0, x_center, y_center)

            if self.__win_type == gtk.TEXT_WINDOW_LEFT:
                p_drawable.draw_line(gc, x_center, y_center, right, y_center)
            else:
                p_drawable.draw_line(gc, x_center, y_center, left, y_center)
