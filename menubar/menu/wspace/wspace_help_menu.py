from menubar.menu.help_menu import HelpMenu


class WSpaceHelpMenu(HelpMenu):
    """
        Menu 'Help' del 'WSpaceMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'WSpaceHelpMenu'.

            Crea un nuevo 'WSpaceHelpMenu'.
        """
        HelpMenu.__init__(self, p_mwindow)
