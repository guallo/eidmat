from menubar.menu.file_menu import FileMenu


class CMDHistoryFileMenu(FileMenu):
    """
        Menu 'File' del 'CMDHistoryMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDHistoryFileMenu'.

            Crea un nuevo 'CMDHistoryFileMenu'.
        """
        FileMenu.__init__(self, p_mwindow)
