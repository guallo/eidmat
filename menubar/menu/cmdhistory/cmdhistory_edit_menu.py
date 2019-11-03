import os
import gtk

from menubar.menu.edit_menu import EditMenu


class CMDHistoryEditMenu(EditMenu):
    """
        Menu 'Edit' del 'CMDHistoryMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDHistoryEditMenu'.

            Crea un nuevo 'CMDHistoryEditMenu'.
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

        # Delete
        self.__delete_item = self.create_item("image", "_Delete",
                                              gtk.STOCK_DELETE)
        self.__delete_item.connect("activate", self.on_delete_activate)
        self.insert(self.__delete_item, 2)

        # Separator
        self.insert(self.create_item("separator"), 3)

        # Select All
        select_item = self.create_item("normal", "Select _All",
                                       p_accel="Ctrl+A")
        select_item.connect("activate", self.on_select_activate)
        self.insert(select_item, 4)

        # Separator
        self.insert(self.create_item("separator"), 5)

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
            Llama el metodo 'CommandHistory.cut'.
        """
        self._mwindow.get_cmdhistory().cut()

    def on_copy_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Copy'.
            Llama el metodo 'CommandHistory.copy'.
        """
        self._mwindow.get_cmdhistory().copy()

    def on_select_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Select All'. Llama el metodo 'CommandHistory.select_all'.
        """
        self._mwindow.get_cmdhistory().select_all()

    def on_delete_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Delete'.
            Llama el metodo 'CommandHistory.delete_selection'.
        """
        self._mwindow.get_cmdhistory().delete_selection()
