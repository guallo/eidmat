from menubar.menu.window_menu import WindowMenu


class CDirectoryWindowMenu(WindowMenu):
    """
        Menu 'Window' del 'CDirectoryMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CDirectoryWindowMenu'.

            Crea un nuevo 'CDirectoryWindowMenu'.
        """
        WindowMenu.__init__(self, p_mwindow)
