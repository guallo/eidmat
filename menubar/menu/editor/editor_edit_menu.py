import os
import gtk

from menubar.menu.edit_menu import EditMenu


class EditorEditMenu(EditMenu):
    """
        Menu 'Edit' del 'EditorMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'EditorEditMenu'.

            Crea un nuevo 'EditorEditMenu'.
        """
        EditMenu.__init__(self, p_mwindow)

        self.__mwindow = p_mwindow

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,
                                                      os.pardir, os.pardir))

        # Undo
        self.__undo_item = self.create_item("image", "_Undo",
                              os.path.join(root, "images", "undo.png"),
                                                                    "Ctrl+Z")
        self.insert(self.__undo_item, 0)
        self.__undo_item.connect("activate", self.on_undo_activate)
    
        # Redo
        self.__redo_item = self.create_item("image", "_Redo",
                              os.path.join(root, "images", "redo.png"), 
                                                              "Shift+Ctrl+Z")
        self.insert(self.__redo_item, 1)
        self.__redo_item.connect("activate", self.on_redo_activate)

        # Cut
        self.__cut_item = self.create_item("image", "Cu_t",
                             os.path.join(root, "images", "cut.png"),
                                                                  "Ctrl+X")
        self.__cut_item.connect("activate", self.on_cut_activate)
        self.insert(self.__cut_item, 2)

        # Copy
        self.__copy_item = self.create_item("image", "_Copy",
                            os.path.join(root, "images", "copy.png"),
                                                                  "Ctrl+C")
        self.__copy_item.connect("activate", self.on_copy_activate)
        self.insert(self.__copy_item, 3)

        # Paste
        self.__paste_item = self.create_item("image", "_Paste",
                           os.path.join(root, "images", "paste.png"),
                                                                  "Ctrl+V")
        self.__paste_item.connect("activate", self.on_paste_activate)
        self.insert(self.__paste_item, 4)

        # Separator
        self.insert(self.create_item("separator"), 5)

        # Delete
        self.__delete_item = self.create_item("normal", "_Delete")
        self.__delete_item.connect("activate", self.on_delete_activate)
        self.insert(self.__delete_item, 6)

        # Select All
        self.__select_item = self.create_item("normal", "Select _All",
                                       p_accel="Ctrl+A")
        self.__select_item.connect("activate", self.on_select_activate)
        self.insert(self.__select_item, 7)

        # Separator
        self.insert(self.create_item("separator"), 8)

    def on_undo_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Undo'.
            Llama el metodo 'EditorDebugger.undo'.
        """
        self.__mwindow.get_edebugger().undo()

    def on_redo_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Redo'.
            Llama el metodo 'EditorDebugger.redo'.
        """
        self.__mwindow.get_edebugger().redo()

    def on_cut_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Cut'.
            Llama el metodo 'EditorDebugger.cut'.
        """
        self.__mwindow.get_edebugger().cut()

    def on_copy_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Copy'.
            Llama el metodo 'EditorDebugger.copy'.
        """
        self.__mwindow.get_edebugger().copy()

    def on_paste_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Paste'.
            Llama el metodo 'EditorDebugger.paste'.
        """
        self.__mwindow.get_edebugger().paste()

    def on_select_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Select All'. Llama el metodo 'EditorDebugger.select_all'.
        """
        self.__mwindow.get_edebugger().select_all()

    def on_delete_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Delete'.
            Llama el metodo 'EditorDebugger.delete'.
        """
        self.__mwindow.get_edebugger().delete()

    def get_undo(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento de menu 'Undo'.
        """
        return self.__undo_item

    def get_redo(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento de menu 'Redo'.
        """
        return self.__redo_item

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

    def get_select(self):
        """
            Retorna: un 'gtk.ImageMenuItem'.

            Retorna el elemento de menu 'Select All'.
        """
        return self.__select_item
