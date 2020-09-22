import os
import gtk

from util.menu import Menu

class EditorTextMenu(Menu):
    """
        Menu 'Text' del 'EditorMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'EditorTextMenu'.

            Crea un nuevo 'EditorTextMenu'.
        """
        Menu.__init__(self)

        # Evaluate Selection
        self.__eval_item = self.create_item("normal", "_Evaluate Selection",
                              None, "F9")

        self.insert(self.__eval_item, 0)

        # Separator
        self.insert(self.create_item("separator"), 1)
    
        # Comment
        self.__comment_item = self.create_item("normal", "_Comment")
        self.insert(self.__comment_item, 2)

        # UnComment
        self.__uncomment_item = self.create_item("normal", "_Uncomment")
        self.insert(self.__uncomment_item, 3)

        # Separator
        self.insert(self.create_item("separator"), 4)

        # Decrease Indent
        self.__decrease_item = self.create_item("normal", "_Decrease Indent")
        self.insert(self.__decrease_item, 5)

        # Increase Indent
        self.__increase_item = self.create_item("normal", "_Increase Indent")
        self.insert(self.__increase_item, 6)

        # Smart Indent
        self.__smart_item = self.create_item("normal", "_Smart Indent")
        self.insert(self.__smart_item, 7)
