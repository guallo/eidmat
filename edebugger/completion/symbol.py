class Symbol:
    def __init__(self, p_lexema, p_info):
        self.__lexema = p_lexema
        self.__info = p_info

    def get_lexema(self):
        return self.__lexema

    def get_info(self):
        return self.__info
