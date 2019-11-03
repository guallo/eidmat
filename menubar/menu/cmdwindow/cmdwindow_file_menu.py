from menubar.menu.file_menu import FileMenu


class CMDWindowFileMenu(FileMenu):
    """
        Menu 'File' del 'CMDWindowMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDWindowFileMenu'.

            Crea un nuevo 'CMDWindowFileMenu'.
        """
        FileMenu.__init__(self, p_mwindow)
