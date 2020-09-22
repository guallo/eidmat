from menubar.menu.file_menu import FileMenu


class ProjectFileMenu(FileMenu):
    """
        Menu 'File' del 'ProjectFileMenu'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'ProjectFileMenu'.

            Crea un nuevo 'ProjectFileMenu'.
        """
        FileMenu.__init__(self, p_mwindow)
