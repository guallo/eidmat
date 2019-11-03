from menubar.menu.window_menu import WindowMenu


class WSpaceWindowMenu(WindowMenu):
    """
        Menu 'Window' del 'WSpaceMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'WSpaceWindowMenu'.

            Crea un nuevo 'WSpaceWindowMenu'.
        """
        WindowMenu.__init__(self, p_mwindow)
