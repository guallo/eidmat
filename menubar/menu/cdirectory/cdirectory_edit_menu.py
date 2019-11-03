from menubar.menu.edit_menu import EditMenu


class CDirectoryEditMenu(EditMenu):
    """
        Menu 'Edit' del 'CDirectoryMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CDirectoryEditMenu'.

            Crea un nuevo 'CDirectoryEditMenu'.
        """
        EditMenu.__init__(self, p_mwindow)
