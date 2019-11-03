from menubar.context_menu_bar import ContextMenuBar
from menubar.menu.cmdhistory.cmdhistory_file_menu import CMDHistoryFileMenu
from menubar.menu.cmdhistory.cmdhistory_edit_menu import CMDHistoryEditMenu
from menubar.menu.cmdhistory.cmdhistory_window_menu import CMDHistoryWindowMenu
from menubar.menu.cmdhistory.cmdhistory_help_menu import CMDHistoryHelpMenu


class CMDHistoryMenuBar(ContextMenuBar):
    """
        Barra de menu del 'CommandHistory'. Esta es la barra de menu que
        muestra la aplicacion cuando el 'CommandHistory' es el elemento
        activo.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDHistoryMenuBar'.

            Crea un nuevo 'CMDHistoryMenuBar'.
        """
        ContextMenuBar.__init__(self, p_mwindow)##########

        # File
        self.append_item("_File", CMDHistoryFileMenu(p_mwindow))

        # Edit
        self.__edit = CMDHistoryEditMenu(p_mwindow)
        self.append_item("_Edit", self.__edit)

        # Window
        self.append_item("_Window", CMDHistoryWindowMenu(p_mwindow))

        # Help
        self.append_item("_Help", CMDHistoryHelpMenu(p_mwindow))

        self.show_all()

    def get_edit(self):
        """
            Retorna: un 'CMDHistoryEditMenu'.

            Retorna el menu editar de la barra de menu del 'CommandHistory'.
        """
        return self.__edit
