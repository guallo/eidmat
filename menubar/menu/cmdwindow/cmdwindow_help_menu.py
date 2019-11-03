from menubar.menu.help_menu import HelpMenu


class CMDWindowHelpMenu(HelpMenu):
    """
        Menu 'Help' del 'CMDWindowMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDWindowHelpMenu'.

            Crea un nuevo 'CMDWindowHelpMenu'.
        """
        HelpMenu.__init__(self, p_mwindow)
