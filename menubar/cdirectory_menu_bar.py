from menubar.context_menu_bar import ContextMenuBar
from menubar.menu.cdirectory.cdirectory_file_menu import CDirectoryFileMenu
from menubar.menu.cdirectory.cdirectory_edit_menu import CDirectoryEditMenu
from menubar.menu.cdirectory.cdirectory_window_menu import CDirectoryWindowMenu
from menubar.menu.cdirectory.cdirectory_help_menu import CDirectoryHelpMenu


class CDirectoryMenuBar(ContextMenuBar):
    """
        Barra de menu del 'CurrentDirectory'. Esta es la barra de menu que
        muestra la aplicacion cuando el 'CurrentDirectory' es el elemento
        activo.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CDirectoryMenuBar'.

            Crea un nuevo 'CDirectoryMenuBar'.
        """
        ContextMenuBar.__init__(self, p_mwindow)##########

        # File
        self.append_item("_File", CDirectoryFileMenu(p_mwindow))

        # Edit
        self.append_item("_Edit", CDirectoryEditMenu(p_mwindow))

        # Window
        self.append_item("_Window", CDirectoryWindowMenu(p_mwindow))

        # Help
        self.append_item("_Help", CDirectoryHelpMenu(p_mwindow))

        self.show_all()
