import os
import gtk


class WorkspaceToolbar(gtk.Toolbar):
    """
        La barra de herramientas del 'Workspace'.
    """
    def __init__(self, p_wspace):
        """
            p_wspace:    un 'Workspace'.

            Retorna:     un nuevo 'WorkspaceToolbar'.

            Crea un nuevo 'WorkspaceToolbar'.
        """
        gtk.Toolbar.__init__(self)

        self.set_style(gtk.TOOLBAR_ICONS)

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

        # Boton para crear nuevas variables.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "new_var.png"))
        new = gtk.ToolButton(img, "New")
        new.set_tooltip_text("New variable")
        new.connect("clicked", self.on_new_clicked)
        new.connect("focus", self.on_button_focus)
        self.insert(new, -1)

        # Boton para importar datos
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "import_data.png"))
        import_ = gtk.ToolButton(img, "Import")
        import_.set_tooltip_text("Import data")
        import_.connect("clicked", self.on_import_clicked)
        import_.connect("focus", self.on_button_focus)
        self.insert(import_, -1)

        # Boton para salvar el workspace
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "save_workspace.png"))
        save = gtk.ToolButton(img, "Save")
        save.set_tooltip_text("Save")
        save.connect("clicked", self.on_save_clicked)
        save.connect("focus", self.on_button_focus)
        self.insert(save, -1)

        # Separador.
        self.insert(gtk.SeparatorToolItem(), -1)

        # Boton para eliminar variables.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "delete_var.png"))
        self.__delete = gtk.ToolButton(img, "Delete")
        self.__delete.set_tooltip_text("Delete")
        self.__delete.connect("clicked", self.on_delete_clicked)
        self.__delete.connect("focus", self.on_button_focus)
        self.insert(self.__delete, -1)

        self.__workspace = p_wspace

    def get_delete(self):
        """
            Retorna: un 'gtk.ToolButton'.

            Retorna el boton de eliminar variables.
        """
        return self.__delete

    def on_new_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando se da click en el boton de crear una nueva
            variable. Llama el metodo 'Workspace.new_var'.
        """
        self.__workspace.new_var()

    def on_import_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando se da click en el boton para importar variables.
            Llama el metodo 'Workspace.import_data'.
        """
        self.__workspace.import_data()

    def on_save_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando se da click en el boton de salvar las variables.
            Llama el metodo 'Workspace.save(True)'.
        """
        self.__workspace.save()

    def on_delete_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando se da click en el boton de eliminar variables.
            Llama el metodo 'Workspace.delete'.
        """
        self.__workspace.delete()

    def on_button_focus(self, p_butt, p_direction):
        """
            p_butt:      el 'gtk.ToolButton' que recibe el foco.
            p_direction: la direccion: 'gtk.DIR_TAB_FORWARD',
                         'gtk.DIR_TAB_BACKWARD', 'gtk.DIR_UP', 'gtk.DIR_DOWN',
                         'gtk.DIR_LEFT', 'gtk.DIR_RIGHT'.

            Retorna:     'True' para detener otros manejadores que se invoquen
                         para el evento.

            Se ejecuta cuando algun boton de 'WorkspaceToolbar' recibe el foco.
            Llama el metodo 'Workspace.grab_focus'.
        """
        self.__workspace.grab_focus()
        return True
