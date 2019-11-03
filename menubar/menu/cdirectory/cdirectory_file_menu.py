from menubar.menu.file_menu import FileMenu


class CDirectoryFileMenu(FileMenu):
    """
        Menu 'File' del 'CDirectoryMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CDirectoryFileMenu'.

            Crea un nuevo 'CDirectoryFileMenu'.
        """
        FileMenu.__init__(self, p_mwindow)
