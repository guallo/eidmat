from menubar.menu.help_menu import HelpMenu


class EditorHelpMenu(HelpMenu):
    """
        Menu 'Help' del 'EditorMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'EditorHelpMenu'.

            Crea un nuevo 'EditorHelpMenu'.
        """
        HelpMenu.__init__(self, p_mwindow)
