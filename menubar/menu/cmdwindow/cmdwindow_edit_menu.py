import os
import gtk

from menubar.menu.edit_menu import EditMenu


class CMDWindowEditMenu(EditMenu):
    """
        Menu 'Edit' del 'CMDWindowMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDWindowEditMenu'.

            Crea un nuevo 'CMDWindowEditMenu'.
        """
        EditMenu.__init__(self, p_mwindow)

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,
                                                      os.pardir, os.pardir))

        # Cut
        self.__cut_item = self.create_item("image", "Cu_t",
                             os.path.join(root, "images", "cut.png"), "Ctrl+X")
        self.__cut_item.connect("activate", self.on_cut_activate)
        self.insert(self.__cut_item, 0)

        # Copy
        self.__copy_item = self.create_item("image", "_Copy",
                            os.path.join(root, "images", "copy.png"), "Ctrl+C")
        self.__copy_item.connect("activate", self.on_copy_activate)
        self.insert(self.__copy_item, 1)

        # Paste
        self.__paste_item = self.create_item("image", "_Paste",
                           os.path.join(root, "images", "paste.png"), "Ctrl+V")
        self.__paste_item.connect("activate", self.on_paste_activate)
        self.insert(self.__paste_item, 2)

        # Delete
        self.__delete_item = self.create_item("image", "_Delete",
                                              gtk.STOCK_DELETE)
        self.__delete_item.connect("activate", self.on_delete_activate)
        self.insert(self.__delete_item, 3)

        # Separator
        self.insert(self.create_item("separator"), 4)

        # Select All
        select_item = self.create_item("normal", "Select _All",
                                       p_accel="Ctrl+A")
        select_item.connect("activate", self.on_select_activate)
        self.insert(select_item, 5)

        # Separator
        self.insert(self.create_item("separator"), 6)

    def get_cut(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento de menu 'Cut'.
        """
        return self.__cut_item

    def get_copy(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento de menu 'Copy'.
        """
        return self.__copy_item

    def get_paste(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento de menu 'Paste'.
        """
        return self.__paste_item

    def get_delete(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento de menu 'Delete'.
        """
        return self.__delete_item

    def on_cut_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Cut'.
            Llama el metodo 'CommandWindow.cut'.
        """
        self._mwindow.get_cmdwindow().cut()

    def on_copy_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Copy'.
            Llama el metodo 'CommandWindow.copy'.
        """
        self._mwindow.get_cmdwindow().copy()

    def on_paste_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Paste'.
            Llama el metodo 'CommandWindow.paste'.
        """
        self._mwindow.get_cmdwindow().paste()

    def on_select_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Select All'. Llama el metodo 'CommandWindow.select_all'.
        """
        self._mwindow.get_cmdwindow().select_all()

    def on_delete_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Delete'.
            Llama el metodo 'CommandWindow.delete_selection'.
        """
        self._mwindow.get_cmdwindow().delete_selection()
