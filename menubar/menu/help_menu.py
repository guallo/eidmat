import os
import gtk

from util.menu import Menu
from menubar.menu.websrc_submenu import WebSRCSubmenu


class HelpMenu(Menu):
    """
        Clase base para los menus 'Help' de las 'ContextMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'HelpMenu'.

            Crea un nuevo 'HelpMenu'.
        """
        Menu.__init__(self)

        self._mwindow = p_mwindow

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,
                                                                 os.pardir))

        # OCTAVE Help
        oct_help = self.create_item("image", "_OCTAVE Help",
                                     os.path.join(root, "images", "help.png"))
        self.append(oct_help)
        oct_help.connect("activate", self.on_oct_help_activate)

        # Web Resources
        web_src = self.create_item("normal", "_Web Resources")
        self.append(web_src)
        web_src.set_submenu(WebSRCSubmenu(p_mwindow))

        # Separator
        self.append(self.create_item("separator"))

        # About EIDMAT
        about = self.create_item("image", "_About EIDMAT", gtk.STOCK_ABOUT)
        self.append(about)
        about.connect("activate", self.on_about_activate)

    def on_oct_help_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'OCTAVE Help'. Llama el metodo 'MainWindow.show_help'.
        """
        self._mwindow.show_help()

    def on_about_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'About EIDMAT'. Llama el metodo 'MainWindow.show_about'.
        """
        self._mwindow.show_about()
