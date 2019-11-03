from menubar.menu.help_menu import HelpMenu


class CDirectoryHelpMenu(HelpMenu):
    """
        Menu 'Help' del 'CDirectoryMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CDirectoryHelpMenu'.

            Crea un nuevo 'CDirectoryHelpMenu'.
        """
        HelpMenu.__init__(self, p_mwindow)
