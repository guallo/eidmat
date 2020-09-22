class EditorTextWindowElement:
    def __init__(self, p_x, p_y, p_width, p_height):
        self.__x = p_x
        self.__y = p_y
        self.__width = p_width
        self.__height = p_height

    def get_geometry(self):
        return (self.__x, self.__y, self.__width, self.__height)

    def draw(self, p_drawable):
        pass
