import gtk

from menubar.context_menu_bar import ContextMenuBar
from menubar.menu.project.project_file_menu import ProjectFileMenu
from menubar.menu.project.project_edit_menu import ProjectEditMenu
from menubar.menu.project.project_window_menu import ProjectWindowMenu
from menubar.menu.project.project_help_menu import ProjectHelpMenu

class ProjectMenuBar(ContextMenuBar):
    """
        Barra de menu del 'ProjectTree'. Esta es la barra de menu que
        muestra la aplicacion cuando el 'ProjectTree' es el elemento
        activo.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'ProjectMenuBar'.

            Crea un nuevo 'ProjectMenuBar'.
        """
        ContextMenuBar.__init__(self, p_mwindow)##########

        # File
        self.append_item("_File", ProjectFileMenu(p_mwindow))

        # Edit
        self.append_item("_Edit", ProjectEditMenu(p_mwindow))

        # Debug
        self.__debug = gtk.Menu()
        self.append_item("De_bug", self.__debug)

        # Window
        self.append_item("_Window", ProjectWindowMenu(p_mwindow))

        # Help
        self.append_item("_Help", ProjectHelpMenu(p_mwindow))

        self.show_all()

    def get_debug(self):
        """
            Retorna: un 'gtk.Menu'.

            Retorna el menu 'Debug' de la barra de menu del 'ProjectTree'.
        """
        return self.__debug
