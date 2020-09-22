import gtk

from menubar.context_menu_bar import ContextMenuBar
from menubar.menu.wspace.wspace_file_menu import WSpaceFileMenu
from menubar.menu.wspace.wspace_edit_menu import WSpaceEditMenu
from menubar.menu.wspace.wspace_window_menu import WSpaceWindowMenu
from menubar.menu.wspace.wspace_help_menu import WSpaceHelpMenu


class WSpaceMenuBar(ContextMenuBar):
    """
        Barra de menu del 'Workspace'. Esta es la barra de menu que
        muestra la aplicacion cuando el 'Workspace' es el elemento
        activo.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'WSpaceMenuBar'.

            Crea un nuevo 'WSpaceMenuBar'.
        """
        ContextMenuBar.__init__(self, p_mwindow)##########

        # File
        self.append_item("_File", WSpaceFileMenu(p_mwindow))

        # Edit
        self.__edit = WSpaceEditMenu(p_mwindow)
        self.append_item("_Edit", self.__edit)

        # Debug
        self.__debug = gtk.Menu()
        self.append_item("De_bug", self.__debug)
        
        # Window
        self.append_item("_Window", WSpaceWindowMenu(p_mwindow))

        # Help
        self.append_item("_Help", WSpaceHelpMenu(p_mwindow))

        self.show_all()

    def get_edit(self):
        """
            Retorna: un 'WSpaceEditMenu'.

            Retorna el menu editar de la barra de menu del 'Workspace'.
        """
        return self.__edit

    def get_debug(self):
        """
            Retorna: un 'gtk.Menu'.

            Retorna el menu 'Debug' de la barra de menu del 'Workspace'.
        """
        return self.__debug
