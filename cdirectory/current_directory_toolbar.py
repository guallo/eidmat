import os
import gtk


class CurrentDirectoryToolbar(gtk.Toolbar):
    """
        La barra de herramientas del 'CurrentDirectory'.
    """
    def __init__(self, p_cdirectory):
        """
            p_cdirectory: un 'CurrentDirectory'.

            Retorna:      un nuevo 'CurrentDirectoryToolbar'.

            Crea un nuevo 'CurrentDirectoryToolbar'.
        """
        gtk.Toolbar.__init__(self)

        self.set_style(gtk.TOOLBAR_ICONS)

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

        # Boton para subir un nivel en el arbol de directorios.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "go_up.png"))
        self.__up = gtk.ToolButton(img, "Up")
        self.__up.set_tooltip_text("Go up one level")
        self.insert(self.__up, -1)

        self.__up.connect("clicked", self.on_button_up_clicked)
        self.__up.connect("focus", self.on_button_focus)

        self.__cdirectory = p_cdirectory

    def get_button_up(self):
        """
            Retorna: un 'gtk.ToolButton'.

            Retorna el boton que sirve para subir un nivel en el arbol de
            directorios.
        """
        return self.__up

    def on_button_up_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando se da click en el boton de subir al directorio
            padre. Llama el metodo 'CurrentDirectory.go_up'.
        """
        self.__cdirectory.go_up()

    def on_button_focus(self, p_butt, p_direction):
        """
            p_butt:      el 'gtk.ToolButton' que recibe el foco.
            p_direction: la direccion: 'gtk.DIR_TAB_FORWARD',
                         'gtk.DIR_TAB_BACKWARD', 'gtk.DIR_UP', 'gtk.DIR_DOWN',
                         'gtk.DIR_LEFT', 'gtk.DIR_RIGHT'.

            Retorna:     'True' para detener otros manejadores que se invoquen
                         para el evento.

            Se ejecuta cuando algun boton de 'CurrentDirectoryToolbar' recibe
            el foco. Llama el metodo 'CurrentDirectory.grab_focus'.
        """
        self.__cdirectory.grab_focus()
        return True
