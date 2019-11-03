import gtk


class Menu(gtk.Menu):
    """
        Clase base para los menus emergentes.
    """
    def __init__(self):
        """
            Retorna: un nuevo 'Menu'.

            Crea un nuevo 'Menu'.
        """
        gtk.Menu.__init__(self)

        self.__size_group = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)

    def create_item(self, p_type, p_text=None, p_stock=None, p_accel=None):
        """
            p_type:  una cadena que representa el tipo de elemento de menu a
                     crear. 'p_type' puede ser "normal", "image", "check",
                     "radio" o "separator".
            p_text:  una cadena a mostrar por el elemento de menu.
            p_stock: una cadena que represente un 'stock de gtk' o una
                     direccion de una imagen a mostrar por el elemento de menu.
            p_accel: una cadena que representa la combinacion de teclas que
                     activa a dicho elemento de menu. 'p_accel' es lo ultimo
                     que se muestra en el elemento de menu.

            Retorna: un 'gtk.MenuItem' en dependencia de los parametros dados.

            Crea y retorna un elemento de menu segun los parametros dados.
        """
        if p_type == "normal":
            item = gtk.MenuItem()

        elif p_type == "image":
            item = gtk.ImageMenuItem()
            img = gtk.Image()
            if gtk.stock_lookup(p_stock):
                img.set_from_stock(p_stock, gtk.ICON_SIZE_MENU)
            else:
                img.set_from_file(p_stock)
            item.set_image(img)

        elif p_type == "check":
            item = gtk.CheckMenuItem()

        elif p_type == "radio":
            pass

        else:
            return gtk.SeparatorMenuItem()

        hbox = gtk.HBox(False, 15)

        label = gtk.Label(p_text)
        label.set_use_underline(True)
        label.set_alignment(0.0, 0.5)
        self.__size_group.add_widget(label)
        hbox.pack_start(label, False)

        if p_accel:
            hbox.pack_end(gtk.Label(p_accel), False)

        item.add(hbox)
        return item
