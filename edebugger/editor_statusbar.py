import gtk
import pango
import gobject


class EditorSatusbar(gtk.Statusbar):
    """
        Barra de estado del EditorDebugger.
    """

    def __init__(self):
        """
            Retorna: un EditorSatusbar.

            Crea un nuevo EditorSatusbar.
        """

        gtk.Statusbar.__init__(self)

        # Creacion de la barra de estado con el modo de insercion.
        self.__overwrite_sb = gtk.Statusbar()

        # Creacion de la barra de estado con la posicion del cursor.
        self.__cursor_sb = gtk.Statusbar()

        # Obtenemos el ancho en pixeles del caracter mas ancho.
        context = self.__overwrite_sb.get_pango_context()
        font = self.__overwrite_sb.style.font_desc
        metrics = context.get_metrics(font, context.get_language())
        digit_width = metrics.get_approximate_digit_width()
        char_width = metrics.get_approximate_char_width()
        width = pango.PIXELS(max(char_width, digit_width))

        # Reservamos espacio para evitar el crecimiento de las barras.
        self.__overwrite_sb.set_size_request(width * 3 + 38, -1)
        self.__cursor_sb.set_size_request(width * 17 + 8, -1)

        self.pack_end(self.__overwrite_sb, False, True, 0)
        self.pack_end(self.__cursor_sb, False, True, 0)

        gtk.Statusbar.set_has_resize_grip(self, False)
        self.__overwrite_sb.set_has_resize_grip(True)
        self.__cursor_sb.set_has_resize_grip(False)

        # tmp flash timeout data
        self.__flash_timeout_id = None
        self.__flash_context_id = None
        self.__flash_message_id = None

        self.connect("destroy", self.on_destroy)

    def set_overwrite(self, p_ovr):
        """
            p_ovr: un boolean o None.

            Si p_ovr es True se muestra la cadena "OVR".
            Si p_ovr es False se muestra la cadena "INS".
            Si p_ovr es None no se muestra nada.
        """

        assert (type(p_ovr) == bool or p_ovr == None)

        self.__overwrite_sb.pop(0)

        if p_ovr == None:
            return

        msg = "OVR" if p_ovr else "INS"
        self.__overwrite_sb.push(0, msg)

    def set_cursor_position(self, p_ln, p_col):
        """
            p_ln:  un entero o None.
            p_col: un entero o None.

            Si p_ln y p_col no son None entonces se muestran como
            la posicion del cursor, sino, no se muestra nada.
        """

        assert ((type(p_ln) in (int, long) and p_ln >= 0) or (p_ln == None))
        assert ((type(p_col) in (int, long) and p_col >= 0) or (p_col == None))

        self.__cursor_sb.pop(0)

        if None in (p_ln, p_col):
            return

        msg = "Ln %d, Col %d" %(p_ln, p_col)
        self.__cursor_sb.push(0, msg)

    def set_has_resize_grip(self, p_has):
        """
            p_has: un boolean.

            Si p_has es True se muestra un grip,
            sino, no se muestra.
        """

        assert (type(p_has) == bool)

        self.__overwrite_sb.set_has_resize_grip(p_has)

    def flash_message(self, p_context_id, p_msg):
        """
            p_context_id: un entero.
            p_msg:        una cadena.

            Muestra el mensaje p_msg durante pocos segundos.
        """

        assert (type(p_context_id) in (long, int) and p_context_id >= 0)
        assert (type(p_msg) == str)

        if self.__flash_timeout_id != None:
            gobject.source_remove(self.__flash_timeout_id)
            self.remove_message(self.__flash_context_id,
                                self.__flash_message_id)

        self.__flash_context_id = p_context_id
        self.__flash_message_id = self.push(p_context_id, p_msg)
        self.__flash_timeout_id = gobject.timeout_add(3000,
                                self.__remove_flash_message)

    def __remove_flash_message(self):
        """
            Retorna: False.

            Elimina el mensaje flash que se esta mostrando.
        """

        assert (self.__flash_timeout_id != None)

        self.remove_message(self.__flash_context_id, self.__flash_message_id)

        self.__flash_timeout_id = None
        return False

    def on_destroy(self, p_editor_sb):
        """
            p_editor_sb: un EditorSatusbar.

            Si se esta mostrando algun mensaje flash
            se llama la funcion gobject.source_remove.
        """

        assert (p_editor_sb == self)

        if self.__flash_timeout_id != None:
            gobject.source_remove(self.__flash_timeout_id)
