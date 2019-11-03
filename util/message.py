import gtk


class Message(gtk.Dialog):
    """
        Dialogo de mensaje.
    """
    def __init__(self, p_stock, p_msg, p_title, p_parent):
        """
            p_stock:  un 'stock de gtk' para mostrar en el dialogo.
            p_msg:    una cadena que es el mensaje del dialogo.
            p_title:  un cadena que es el titulo del dialogo.
            p_parent: un 'gtk.Window' a tomar como padre del dialogo.

            Retorna:  un nuevo 'Message'.

            Crea un nuevo 'Message'.
        """
        gtk.Dialog.__init__(self, p_title, p_parent,
                                  gtk.DIALOG_MODAL|gtk.DIALOG_NO_SEPARATOR,
                                  (gtk.STOCK_OK, gtk.RESPONSE_OK))

        self.set_default_response(gtk.RESPONSE_OK)

        hbox = gtk.HBox(False, 12)

        # Adicionamos el icono.
        vbox = gtk.VBox()
        img = gtk.Image()
        img.set_from_stock(p_stock, gtk.ICON_SIZE_DIALOG)
        vbox.pack_start(img, False)
        hbox.pack_start(vbox)

        # Adicionamos el mensaje.
        hbox.pack_start(gtk.Label(p_msg))

        self.child.add(hbox)
        hbox.show_all()

        self.set_border_width(5)
        self.set_resizable(False)
        self.child.set_spacing(5)
        self.child.get_children()[-1].set_layout(gtk.BUTTONBOX_CENTER)

    def run(self, p_block=False):
        """
            p_block: un 'boolean'.

            Muestra el dialogo de mensaje('Message'). Si 'p_block' es
            'True' el dialogo se muestra entre 'gtk.gdk.threads_enter()' y
            'gtk.gdk.threads_leave()'.
        """
        if p_block:
            gtk.gdk.threads_enter()

        gtk.Dialog.run(self)
        self.destroy()

        if p_block:
            gtk.gdk.threads_leave()
