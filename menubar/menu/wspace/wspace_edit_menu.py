import os

from menubar.menu.edit_menu import EditMenu


class WSpaceEditMenu(EditMenu):
    """
        Menu 'Edit' del 'WSpaceMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'WSpaceEditMenu'.

            Crea un nuevo 'WSpaceEditMenu'.
        """
        EditMenu.__init__(self, p_mwindow)

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,
                                                      os.pardir, os.pardir))

        # Copy
        self.__copy_item = self.create_item("image", "_Copy",
                            os.path.join(root, "images", "copy.png"), "Ctrl+C")
        self.__copy_item.connect("activate", self.on_copy_activate)
        self.insert(self.__copy_item, 0)

        # Duplicate
        self.__duplicate_item = self.create_item("normal", "D_uplicate",
                                                 p_accel="Ctrl+D")
        self.__duplicate_item.connect("activate", self.on_duplicate_activate)
        self.insert(self.__duplicate_item, 1)

        # Delete
        self.__delete_item = self.create_item("image", "_Delete",
                                os.path.join(root, "images", "delete_var.png"))
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

        # Rename...
        self.__rename_item = self.create_item("normal", "_Rename...",
                                              p_accel="F2")
        self.__rename_item.connect("activate", self.on_rename_activate)
        self.insert(self.__rename_item, 6)

        # Separator
        self.insert(self.create_item("separator"), 7)

    def get_copy(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento de menu 'Copy'.
        """
        return self.__copy_item

    def get_duplicate(self):
        """
            Retorna: un 'gtk.MenuItem'.

            Retorna el elemento de menu 'Duplicate'.
        """
        return self.__duplicate_item

    def get_delete(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento de menu 'Delete'.
        """
        return self.__delete_item

    def get_rename(self):
        """
            Retorna: un 'gtk.MenuItem'.

            Retorna el elemento de menu 'Rename...'.
        """
        return self.__rename_item

    def on_copy_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Copy'.
            Llama el metodo 'Workspace.copy'.
        """
        self._mwindow.get_wspace().copy()

    def on_duplicate_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Duplicate'. Llama el metodo 'Workspace.duplicate'.
        """
        self._mwindow.get_wspace().duplicate()

    def on_select_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Select All'. Llama el metodo 'Workspace.select_all'.
        """
        self._mwindow.get_wspace().select_all()

    def on_delete_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Delete'.
            Llama el metodo 'Workspace.delete'.
        """
        self._mwindow.get_wspace().delete()

    def on_rename_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Rename...'. Llama el metodo 'Workspace.rename'.
        """
        self._mwindow.get_wspace().rename()
