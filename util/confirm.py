import gtk


class Confirm(gtk.Dialog):
    """
        Dialogo de confirmacion.
    """
    def __init__(self, p_stock, p_msg, p_title, p_parent, p_check_msg=None):
        """
            p_stock:     un 'stock de gtk' para mostrar en el dialogo.
            p_msg:       una cadena que es el mensaje del dialogo.
            p_title:     un cadena que es el titulo del dialogo.
            p_parent:    un 'gtk.Window' a tomar como padre del dialogo.
            p_check_msg: si se especifica tiene que ser una cadena, que se
                         mostrara en un 'gtk.CheckButton'.

            Retorna:     un nuevo 'Confirm'.

            Crea un nuevo 'Confirm'.
        """
        gtk.Dialog.__init__(self, p_title, p_parent,
                                  gtk.DIALOG_MODAL|gtk.DIALOG_NO_SEPARATOR,
                                  (gtk.STOCK_OK, gtk.RESPONSE_OK,
                                   gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

        self.set_default_response(gtk.RESPONSE_OK)

        hbox = gtk.HBox(False, 12)

        # Adicionamos el icono.
        vbox = gtk.VBox()
        img = gtk.Image()
        img.set_from_stock(p_stock, gtk.ICON_SIZE_DIALOG)
        vbox.pack_start(img, False)
        hbox.pack_start(vbox)

        # Adicionamos el mensaje.
        vbox = gtk.VBox()
        label = gtk.Label(p_msg)
        label.set_alignment(0.0, 0.5)
        vbox.pack_start(label, {None: True}.get(p_check_msg, False))

        # Adicionamos el checkbutton si es que hay.
        self.__check = None
        if p_check_msg:
            self.__check = gtk.CheckButton(p_check_msg)
            vbox.pack_end(self.__check, False)

        hbox.pack_start(vbox)

        self.child.add(hbox)
        hbox.show_all()

        self.set_border_width(5)
        self.set_resizable(False)
        self.child.set_spacing(5)
        self.child.get_children()[-1].set_layout(gtk.BUTTONBOX_CENTER)

    def run(self, p_block=False):
        """
            p_block: un 'boolean'.

            Retorna: 'False' si se cancela el 'Confirm'.
                     Si se acepta el dialogo 'Confirm' y este muestra un
                     'gtk.CheckButton', se retorna una tupla('tuple') que
                     contiene 'True' o 'False' si esta o no seleccionado
                     el 'gtk.CheckButton'.
                     Si se acepta el dialogo 'Confirm' y este NO muestra un
                     'gtk.CheckButton', entoces se retorna 'True'.

            Muestra el dialogo de confirmacion('Confirm'). Si 'p_block' es
            'True' el dialogo se muestra entre 'gtk.gdk.threads_enter()' y
            'gtk.gdk.threads_leave()'.
        """
        if p_block:
            gtk.gdk.threads_enter()

        result = False
        if gtk.Dialog.run(self) == gtk.RESPONSE_OK:
            result = True
            if self.__check:
                result = (self.__check.get_active(), )
        self.destroy()

        if p_block:
            gtk.gdk.threads_leave()

        return result
