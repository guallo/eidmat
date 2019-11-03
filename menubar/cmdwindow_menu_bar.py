from menubar.context_menu_bar import ContextMenuBar
from menubar.menu.cmdwindow.cmdwindow_file_menu import CMDWindowFileMenu
from menubar.menu.cmdwindow.cmdwindow_edit_menu import CMDWindowEditMenu
from menubar.menu.cmdwindow.cmdwindow_window_menu import CMDWindowWindowMenu
from menubar.menu.cmdwindow.cmdwindow_help_menu import CMDWindowHelpMenu


class CMDWindowMenuBar(ContextMenuBar):
    """
        Barra de menu del 'CommandWindow'. Esta es la barra de menu que
        muestra la aplicacion cuando el 'CommandWindow' es el elemento
        activo.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDWindowMenuBar'.

            Crea un nuevo 'CMDWindowMenuBar'.
        """
        ContextMenuBar.__init__(self, p_mwindow)##########

        # File
        self.append_item("_File", CMDWindowFileMenu(p_mwindow))

        # Edit
        self.__edit = CMDWindowEditMenu(p_mwindow)
        self.append_item("_Edit", self.__edit)

        # Window
        self.append_item("_Window", CMDWindowWindowMenu(p_mwindow))

        # Help
        self.append_item("_Help", CMDWindowHelpMenu(p_mwindow))

        self.show_all()

    def get_edit(self):
        """
            Retorna: un 'CMDWindowEditMenu'.

            Retorna el menu editar de la barra de menu del 'CommandWindow'.
        """
        return self.__edit
