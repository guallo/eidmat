import os

from util.menu import Menu


class NewSubmenu(Menu):
    """
        Clase base para los submenus 'File/New' de las 'ContextMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'NewSubmenu'.

            Crea un nuevo 'NewSubmenu'.
        """
        Menu.__init__(self)

        self._mwindow = p_mwindow

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,
                                                                 os.pardir))

        # Variable
        var_item = self.create_item("image", "_Variable",
                                   os.path.join(root, "images", "new_var.png"))
        self.append(var_item)
        var_item.connect("activate", self.on_var_activate)

    def on_var_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Variable'. Llama el metodo 'Workspace.new_var'.
        """
        wspace = self._mwindow.get_wspace()

        wspace.grab_focus()
        wspace.new_var()
