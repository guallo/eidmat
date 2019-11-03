from util.buffer_ import Buffer


class CommandWindowBuffer(Buffer):
    """
        El buffer del 'CommandWindow'.
    """
    def __init__(self):
        """
            Retorna: un 'CommandWindowBuffer'.

            Crea un nuevo 'CommandWindowBuffer'.
        """
        Buffer.__init__(self)

        # Estos atributos se dejaron publico
        # por cuestion de ganar en velocidad.
        self.limit = 0
        self.end_mark = self.create_mark(None, 0, False)

        self.__scrollback_lines = 5000
        self.__no_editable_tag = self.create_tag(editable = False)
        self.apply_tag(self.__no_editable_tag, 0, 0)

    def update_no_editable_zone(self):
        """
            Actualiza la zona no editable del 'CommandWindow'. Esto asegura
            que el usuario no borre la salida dada por 'Octave' o algun
            comando ya enviado anteriormente al mismo.
        """
        self.remove_tag(self.__no_editable_tag, 0, self.limit)
        self.apply_tag(self.__no_editable_tag, 0, self.limit)

    def check_scrollback_lines(self):
        """
            Chequea que el numero maximo de lineas del 'CommandWindow' no
            sea mayor que el atributo 'CommandWindow.__scrollback_lines',
            en caso de ser mayor, entonces se eliminan las lineas necesarias.
        """
        diff = self.get_line_count() - self.__scrollback_lines

        if diff > 0:
            end = self.get_offset_at_line(diff)
            self.delete(0, end)
            self.limit -= end
