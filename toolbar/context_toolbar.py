import os
import gtk


class ContextToolbar(gtk.Toolbar):
    """
        Clase base para todas las barras de herramientas contextuales de la
        aplicacion, es decir, que todas las barras de herramientas principales
        de la aplicacion heredan de 'ContextToolbar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'ContextToolbar'.

            Crea un nuevo 'ContextToolbar'.
        """
        gtk.Toolbar.__init__(self)

        self._mwindow = p_mwindow

        self.set_style(gtk.TOOLBAR_ICONS)

        self.connect("button-press-event", self.on_button_press_event)

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

        # Boton cortar.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "cut.png"))
        self._cut = gtk.ToolButton(img)
        self._cut.set_tooltip_text("Cut")
        self._cut.connect("clicked", self.on_cut_clicked)
        self.insert(self._cut, -1)

        # Boton copiar.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "copy.png"))
        self._copy = gtk.ToolButton(img)
        self._copy.set_tooltip_text("Copy")
        self._copy.connect("clicked", self.on_copy_clicked)
        self.insert(self._copy, -1)

        # Boton pegar.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "paste.png"))
        self._paste = gtk.ToolButton(img)
        self._paste.set_tooltip_text("Paste")
        self._paste.connect("clicked", self.on_paste_clicked)
        self.insert(self._paste, -1)

        # Separador.
        self.insert(gtk.SeparatorToolItem(), -1)

        # Boton para mostrar la ayuda.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "help.png"))
        help = gtk.ToolButton(img)
        help.set_tooltip_text("Help")
        help.connect("clicked", self.on_help_clicked)
        self.insert(help, -1)

        # Separador.
        self.insert(gtk.SeparatorToolItem(), -1)

        # Label 'Current Directory:'
        item = gtk.ToolItem()
        label = gtk.Label("Current Director_y: ")
        label.set_use_underline(True)
        label.set_mnemonic_widget(p_mwindow.get_combo())
        item.add(label)
        self.insert(item, -1)

        # Boton para seleccionar un directorio.
        browse = gtk.ToolItem()
        browse.add(gtk.Button("..."))
        browse.set_tooltip_text("Browse for folder")
        browse.child.connect("clicked", self.on_browse_clicked)
        self.insert(browse, -1)

    def get_cut(self):
        """
            Retorna: un 'gtk.ToolButton'.

            Retorna el boton 'Cut'.
        """
        return self._cut

    def get_copy(self):
        """
            Retorna: un 'gtk.ToolButton'.

            Retorna el boton 'Copy'.
        """
        return self._copy

    def get_paste(self):
        """
            Retorna: un 'gtk.ToolButton'.

            Retorna el boton 'Paste'.
        """
        return self._paste

    def remove_combo(self):
        """
            Elimina el 'ComboOfDirectories' de la 'ContextToolbar'.
        """
        item = self.get_nth_item(7)

        item.remove(self._mwindow.get_combo())
        self.remove(item)

    def remove_butt_up(self):
        """
            Elimina de la 'ContextToolbar' el boton de subir al directorio
            padre.
        """
        self.remove(self._mwindow.get_butt_up())

    def insert_combo(self):
        """
            Inserta el 'ComboOfDirectories' en la 'ContextToolbar'.
        """
        item = gtk.ToolItem()
        item.add(self._mwindow.get_combo())
        item.show_all()
        self.insert(item, 7)

    def insert_butt_up(self):
        """
            Inserta en la 'ContextToolbar' el boton de subir al directorio
            padre.
        """
        item = self._mwindow.get_butt_up()
        item.show_all()
        self.insert(item, -1)

    def on_button_press_event(self, p_tbar, p_event):
        """
            p_tbar:  el 'ContextToolbar' que recibio la sennal.
            p_event: el evento que desencadeno la sennal.

            Se ejecuta cada vez que se presiona un boton del mouse sobre
            'p_tbar'. Chequea si ocurrio el click derecho, en ese caso lanza
            el menu emergente 'PopupMenu'.
        """
        if p_event.button == 3:
            self._mwindow.get_popup_menu().popup3(p_event)

    def on_cut_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Implementado en las clases hijas: 'CDirectoryToolbar'
                                              'CMDHistoryToolbar'
                                              'CMDWindowToolbar'
        """

    def on_copy_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Implementado en las clases hijas: 'CDirectoryToolbar'
                                              'CMDHistoryToolbar'
                                              'CMDWindowToolbar'
                                              'WSpaceToolbar'
        """

    def on_paste_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Implementado en las clases hijas: 'CDirectoryToolbar'
                                              'CMDWindowToolbar'
                                              'WSpaceToolbar'
        """

    def on_help_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando el usuario da click en el boton 'Help'.
            Llama el metodo 'MainWindow.show_help'.
        """
        self._mwindow.show_help()

    def on_browse_clicked(self, p_butt):
        """
            p_butt: el 'gtk.Button' que recibio la sennal.

            Se ejecuta cuando el usuario da click en el boton
            'Browse for folder'. Llama el metodo
            'MainWindow.browse_for_folder'.
        """
        self._mwindow.get_cdirectory().browse_for_folder()
