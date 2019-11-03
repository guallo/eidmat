from menubar.menu.window_menu import WindowMenu


class CMDWindowWindowMenu(WindowMenu):
    """
        Menu 'Window' del 'CMDWindowMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDWindowWindowMenu'.

            Crea un nuevo 'CMDWindowWindowMenu'.
        """
        WindowMenu.__init__(self, p_mwindow)
