from menubar.menu.window_menu import WindowMenu


class CMDHistoryWindowMenu(WindowMenu):
    """
        Menu 'Window' del 'CMDHistoryMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDHistoryWindowMenu'.

            Crea un nuevo 'CMDHistoryWindowMenu'.
        """
        WindowMenu.__init__(self, p_mwindow)
