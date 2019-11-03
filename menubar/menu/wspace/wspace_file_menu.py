from menubar.menu.file_menu import FileMenu


class WSpaceFileMenu(FileMenu):
    """
        Menu 'File' del 'WSpaceMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'WSpaceFileMenu'.

            Crea un nuevo 'WSpaceFileMenu'.
        """
        FileMenu.__init__(self, p_mwindow)
