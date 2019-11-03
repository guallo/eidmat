from util.menu import Menu


class WindowMenu(Menu):
    """
        Clase base para los menus 'Window' de las 'ContextMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'WindowMenu'.

            Crea un nuevo 'WindowMenu'.
        """
        Menu.__init__(self)

        self._mwindow = p_mwindow

        # Command Window
        cmdwindow_item = self.create_item("normal", "_0 Command Window")
        self.append(cmdwindow_item)
        cmdwindow_item.connect("activate", self.on_cmdwindow_activate)

        # Command History
        cmdhistory_item = self.create_item("normal", "_1 Command History")
        self.append(cmdhistory_item)
        cmdhistory_item.connect("activate", self.on_cmdhistory_activate)

        # Current Directory
        cdirectory_item = self.create_item("normal", "_2 Current Directory")
        self.append(cdirectory_item)
        cdirectory_item.connect("activate", self.on_cdirectory_activate)

        # Workspace
        wspace_item = self.create_item("normal", "_3 Workspace")
        self.append(wspace_item)
        wspace_item.connect("activate", self.on_wspace_activate)

    def on_cmdwindow_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Command Window'. Llama el metodo 'CommandWindow.grab_focus'.
        """
        self._mwindow.get_cmdwindow().grab_focus()

    def on_cmdhistory_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Command History'. Llama el metodo 'CommandHistory.grab_focus'.
        """
        self._mwindow.get_cmdhistory().grab_focus()

    def on_cdirectory_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Current Directory'. Llama el metodo 'CurrentDirectory.grab_focus'.
        """
        self._mwindow.get_cdirectory().grab_focus()

    def on_wspace_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Workspace'. Llama el metodo 'Workspace.grab_focus'.
        """
        self._mwindow.get_wspace().grab_focus()
