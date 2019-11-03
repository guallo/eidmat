from util.menu import Menu


class EditMenu(Menu):
    """
        Clase base para los menus 'Edit' de las 'ContextMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'EditMenu'.

            Crea un nuevo 'EditMenu'.
        """
        Menu.__init__(self)

        self._mwindow = p_mwindow

        # Clear Command Window
        clear_cmdwindow = self.create_item("normal", "Clear Command _Window")
        self.append(clear_cmdwindow)
        clear_cmdwindow.connect("activate", self.on_clear_cmdwindow_activate)

        # Clear Command History
        clear_cmdhistory = self.create_item("normal", "Clear Command _History")
        self.append(clear_cmdhistory)
        clear_cmdhistory.connect("activate", self.on_clear_cmdhistory_activate)

        # Clear Workspace
        clear_wspace = self.create_item("normal", "Clear W_orkspace")
        self.append(clear_wspace)
        clear_wspace.connect("activate", self.on_clear_wspace_activate)

    def on_clear_cmdwindow_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Clear Command Window'. Llama el metodo 'CommandWindow.clear'.
        """
        self._mwindow.get_cmdwindow().clear()

    def on_clear_cmdhistory_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Clear Command History'. Llama el metodo 'CommandHistory.clear'.
        """
        self._mwindow.get_cmdhistory().clear()

    def on_clear_wspace_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Clear Workspace'. Llama el metodo 'Workspace.clear'.
        """
        self._mwindow.get_wspace().clear()
