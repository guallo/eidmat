import os
import gtk

from menubar.menu.edit_menu import EditMenu


class ProjectEditMenu(EditMenu):
    """
        Menu 'Edit' del 'ProjectMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'ProjectEditMenu'.

            Crea un nuevo 'ProjectEditMenu'.
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

            Retorna el elemento 'Cut' del menu.
        """
        return self.__cut_item

    def get_copy(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento 'Copy 'del menu.
        """
        return self.__copy_item

    def get_delete(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento 'Delete' del menu.
        """
        return self.__delete_item

    def on_cut_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 'Cut' del menu.
            Llama el metodo 'cut' referido al area de trabajo activa.
        """
        self._mwindow.get_cmdhistory().cut()

    def on_copy_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 'Copy' del menu.
            Llama el metodo 'copy' referido al area de trabajo activa.
        """
        self._mwindow.get_cmdhistory().copy()

    def on_select_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 'Select All' del
            menu. Llama el metodo 'select_all' referido al area de trabajo
            activa.
        """
        self._mwindow.get_cmdhistory().select_all()

    def on_delete_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 'Delete' del menu.
            Llama el metodo 'delete_selection' referido al area de trabajo
            activa.
        """
        self._mwindow.get_cmdhistory().delete_selection()
