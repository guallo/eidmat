import gtk

from menubar.context_menu_bar import ContextMenuBar
from menubar.menu.editor.editor_file_menu import EditorFileMenu
from menubar.menu.editor.editor_edit_menu import EditorEditMenu
#from menubar.menu.editor.editor_text_menu import EditorTextMenu
#from menubar.menu.editor.editor_debug_menu import EditorDebugMenu
from menubar.menu.editor.editor_help_menu import EditorHelpMenu
from menubar.menu.editor.editor_window_menu import EditorWindowMenu

class EditorMenuBar(ContextMenuBar):
    """
        Barra de menu del 'EditorDebugger' de la aplicacion.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'EditorMenuBar'.

            Crea un nuevo 'EditorMenuBar'.
        """
        ContextMenuBar.__init__(self, p_mwindow)##########

        # File
        self.__file = EditorFileMenu(p_mwindow)
        self.append_item("_File", self.__file)

        # Edit
        self.__edit = EditorEditMenu(p_mwindow)
        self.append_item("_Edit", self.__edit)

        # Debug
        self.__debug = gtk.Menu()
        self.append_item("De_bug", self.__debug)

        # Text
        #self.append_item("_Text", EditorTextMenu(p_mwindow))

        # Debug
        #self.append_item("De_bug", EditorDebugMenu(p_mwindow))

        # Window
        self.append_item("_Window", EditorWindowMenu(p_mwindow))

        # Help
        self.append_item("_Help", EditorHelpMenu(p_mwindow))

    def get_file(self):
        """
            Retorna: un 'EditorFileMenu'.

            Retorna el menu 'File' de la barra de menu del 'EditorDebugger'.
        """
        return self.__file

    def get_edit(self):
        """
            Retorna: un 'EditorEditMenu'.

            Retorna el menu 'Edit' de la barra de menu del 'EditorDebugger'.
        """
        return self.__edit

    def get_debug(self):
        """
            Retorna: un 'gtk.Menu'.

            Retorna el menu 'Debug' de la barra de menu del 'EditorDebugger'.
        """
        return self.__debug
