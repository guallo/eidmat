import os

from menubar.menu.file_menu import FileMenu


class EditorFileMenu(FileMenu):
    """
        Menu 'File' del 'EditorMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'EditorFileMenu'.

            Crea un nuevo 'EditorFileMenu'.
        """
        FileMenu.__init__(self, p_mwindow)
    
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,
                                                      os.pardir, os.pardir))

        # Close Editor
        #close_item = self.create_item("normal", "Close Editor")
        #self.insert(close_item, 2)

        # Save
        save_item = self.create_item("image", "_Save", os.path.join(root,
                                                  "images", "save.png"))
        self.insert(save_item, 4)
        save_item.connect("activate", self.on_save_doc_activate)
        self.__editor_save = save_item

        # Save As
        save_as_item = self.create_item("normal", "Save _As...")
        self.insert(save_as_item, 5)
        save_as_item.connect("activate", self.on_save_doc_as_activate)
        self.__editor_save_as = save_as_item

        # Separator
        self.insert(self.create_item("separator"), 6)

    def on_open_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Open'. Llama el metodo 'EditorDebugger.open_document'.
        """
        self._mwindow.get_edebugger().open_document()

    def on_save_doc_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Save'.
            Llama el metodo 'EditorDebugger.save'.
        """
        self._mwindow.get_edebugger().save()

    def on_save_doc_as_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Save As...'. Llama el metodo 'EditorDebugger.save_as'.
        """
        self._mwindow.get_edebugger().save_as()

    def get_editor_save(self):
        """
            Retorna: un 'gtk.MenuItem'.

            Retorna el elemento de menu 'Save'.
        """
        return self.__editor_save

    def get_editor_save_as(self):
        """
            Retorna: un 'gtk.MenuItem'.

            Retorna el elemento de menu 'Save As...'.
        """
        return self.__editor_save_as
