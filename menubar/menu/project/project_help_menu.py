from menubar.menu.help_menu import HelpMenu


class ProjectHelpMenu(HelpMenu):
    """
        Menu 'Help' del 'ProjectHelpMenu'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'ProjectHelpMenu'.

            Crea un nuevo 'ProjectHelpMenu'.
        """
        HelpMenu.__init__(self, p_mwindow)
