from menubar.menu.window_menu import WindowMenu


class EditorWindowMenu(WindowMenu):
    """
        Menu 'Window' del 'EditorMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'EditorWindowMenu'.

            Crea un nuevo 'EditorWindowMenu'.
        """
        WindowMenu.__init__(self, p_mwindow)
