import os
import gtk

from util.menu import Menu
from menubar.menu.new_submenu import NewSubmenu


class FileMenu(Menu):
    """
        Clase base para los menus 'File' de las 'ContextMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'FileMenu'.

            Crea un nuevo 'FileMenu'.
        """
        Menu.__init__(self)

        self._mwindow = p_mwindow

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,
                                                                 os.pardir))

        # New
        new_item = self.create_item("image", "_New",
                            os.path.join(root, "images", "new_file.png"))
        self.append(new_item)
        new_item.set_submenu(NewSubmenu(p_mwindow))

        # Open
        self._open_item = self.create_item("image", "_Open...",
                            os.path.join(root, "images", "open.png"))
        self.append(self._open_item)
        self._open_item.connect("activate", self.on_open_activate)

        # Separator
        self.append(self.create_item("separator"))

        # Import Data...
        import_item = self.create_item("normal", "_Import Data...")
        self.append(import_item)
        import_item.connect("activate", self.on_import_activate)

        # Save Workspace As...
        save_item = self.create_item("image", "Save _Workspace As...",
                            os.path.join(root, "images", "save_workspace.png"))
        self.append(save_item)
        save_item.connect("activate", self.on_save_activate)

        # Separator
        self.append(self.create_item("separator"))

        # Exit EIDMAT
        exit_item = self.create_item("image", "E_xit EIDMAT", gtk.STOCK_QUIT)
        self.append(exit_item)
        exit_item.connect("activate", self.on_exit_activate)

    def on_open_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Open'. Llama el metodo 'MainWindow.open_'.
        """
        self._mwindow.open_()

    def on_import_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Import Data...'. Llama el metodo 'Workspace.import_data'.
        """
        self._mwindow.get_wspace().import_data()

    def on_save_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Save Workspace As...'. Llama el metodo 'Workspace.save'.
        """
        self._mwindow.get_wspace().save()

    def on_exit_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Exit EIDMAT'. Llama el metodo 'MainWindow.close'.
        """
        self._mwindow.close()
