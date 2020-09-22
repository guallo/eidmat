import os
import gtk

from util.menu import Menu

class EditorDebugMenu(Menu):
    """
        Menu 'Debug' del 'EditorMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'EditorDebugMenu'.

            Crea un nuevo 'EditorDebugMenu'.
        """
        Menu.__init__(self)

        # Save and Run
        self.__run_item = self.create_item("normal", "Save and _Run",
                              None, "F5")

        self.insert(self.__run_item, 0)
