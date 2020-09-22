from menubar.menu.window_menu import WindowMenu


class ProjectWindowMenu(WindowMenu):
    """
        Menu 'Window' del 'ProjectWindowMenu'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'ProjectWindowMenu'.

            Crea un nuevo 'ProjectWindowMenu'.
        """
        WindowMenu.__init__(self, p_mwindow)
