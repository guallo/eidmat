from menubar.menu.help_menu import HelpMenu


class CMDHistoryHelpMenu(HelpMenu):
    """
        Menu 'Help' del 'CMDHistoryMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDHistoryHelpMenu'.

            Crea un nuevo 'CMDHistoryHelpMenu'.
        """
        HelpMenu.__init__(self, p_mwindow)
