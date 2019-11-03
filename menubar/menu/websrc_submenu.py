from util.menu import Menu


class WebSRCSubmenu(Menu):
    """
        Clase base para los submenus 'Help/Web Resources' de las
        'ContextMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'WebSRCSubmenu'.

            Crea un nuevo 'WebSRCSubmenu'.
        """
        Menu.__init__(self)

        self._mwindow = p_mwindow

        # EIDMAT Web Site
        eidmat_site = self.create_item("normal", "_EIDMAT Web Site")
        self.append(eidmat_site)
        eidmat_site.connect("activate", self.on_eidmat_site_activate)

        # OCTAVE Web Site
        oct_site = self.create_item("normal", "O_CTAVE Web Site")
        self.append(oct_site)
        oct_site.connect("activate", self.on_oct_site_activate)

    def on_eidmat_site_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'EIDMAT Web Site'. Llama el metodo
            'MainWindow.open_site("http://www.eidmat.wordpress.com")'.
        """
        self._mwindow.open_site("http://www.eidmat.wordpress.com")

    def on_oct_site_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'OCTAVE Web Site'. Llama el metodo
            'MainWindow.open_site("http://www.octave.org")'.
        """
        self._mwindow.open_site("http://www.octave.org")
