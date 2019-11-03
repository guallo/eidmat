import os
import gtk

from util.menu import Menu


class ListVarsMenu(Menu):
    """
        El menu emergente que se muestra cuando se presiona click derecho
        sobre el 'ListVars' del 'Workspace'.
    """
    def __init__(self, p_wspace):
        """
            p_wspace: un 'Workspace'.

            Retorna:  un nuevo 'ListVarsMenu'.

            Crea un nuevo 'ListVarsMenu'.
        """
        Menu.__init__(self)

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

        # Save As
        self.__save_item = self.create_item("image", "Save _As...",
                                            gtk.STOCK_SAVE_AS)
        self.__save_item.connect("activate", self.on_save_activate)

        # Separator
        self.create_item("separator")

        # Copy
        img = os.path.join(root, "images", "copy.png")
        self.__copy_item = self.create_item("image", "_Copy", img, "Ctrl+C")
        self.__copy_item.connect("activate", self.on_copy_activate)

        # Duplicate
        self.__duplicate_item = self.create_item("normal", "D_uplicate",
                                                 p_accel="Ctrl+D")
        self.__duplicate_item.connect("activate", self.on_duplicate_activate)

        # Delete
        img = os.path.join(root, "images", "delete_var.png")
        self.__delete_item = self.create_item("image", "_Delete", img)
        self.__delete_item.connect("activate", self.on_delete_activate)

        # Separator
        self.create_item("separator")

        # Rename
        self.__rename_item = self.create_item("normal", "_Rename...",
                                              p_accel="F2")
        self.__rename_item.connect("activate", self.on_rename_activate)

        # Separator
        self.create_item("separator")

        # New
        img = os.path.join(root, "images", "new_var.png")
        new_item = self.create_item("image", "_New", img, "Ctrl+N")
        new_item.connect("activate", self.on_new_activate)

        self.__workspace = p_wspace

    def get_save(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento de menu 'Save As...'.
        """
        return self.__save_item

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

            Crea, adiciona y retorna un elemento de menu segun los parametros
            dados.
        """
        item = Menu.create_item(self, p_type, p_text, p_stock, p_accel)
        item.show_all()
        self.append(item)
        return item

    def on_save_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Save As...'. Llama el metodo 'Workspace.save(False)'.
        """
        self.__workspace.save(False)

    def on_copy_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Copy'.
            Llama el metodo 'Workspace.copy'.
        """
        self.__workspace.copy()

    def on_duplicate_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Duplicate'. Llama el metodo 'Workspace.duplicate'.
        """
        self.__workspace.duplicate()

    def on_delete_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Delete'.
            Llama el metodo 'Workspace.delete'.
        """
        self.__workspace.delete()

    def on_rename_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Rename...'. Llama el metodo 'Workspace.rename'.
        """
        self.__workspace.rename()

    def on_new_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'New'.
            Llama el metodo 'Workspace.new_var'.
        """
        self.__workspace.new_var()
