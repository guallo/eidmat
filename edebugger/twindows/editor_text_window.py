import gtk


class EditorTextWindow(gtk.gdk.Rectangle):
    def __init__(self, p_name, p_type, p_pos, p_size, p_bg_color, p_elements):
        gtk.gdk.Rectangle.__init__(self)

        self.__name = p_name
        self.__type = p_type
        self.__pos = p_pos
        self.__size = p_size
        self.__bg_color = p_bg_color
        self.__elements = p_elements

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_pos(self):
        return self.__pos

    def get_size(self):
        return self.__size

    def get_bg_color(self):
        return self.__bg_color

    def get_elements(self):
        return self.__elements

    def set_name(self, p_name):
        self.__name = p_name

    def set_type(self, p_type):
        self.__type = p_type

    def set_pos(self, p_pos):
        self.__pos = p_pos

    def set_size(self, p_size):
        self.__size = p_size

    def set_bg_color(self, p_bg_color):
        self.__bg_color = p_bg_color

    def set_elements(self, p_elements):
        self.__elements = p_elements
