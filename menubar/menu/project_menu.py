import os
import gtk

from util.menu import Menu
from menubar.menu.new_submenu import NewSubmenu


class ProjectMenu(Menu):
    """
        Clase base para los menus 'Project' de las 'ContextMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna: un 'ProjectMenu'.

            Crea un nuevo 'ProjectMenu'.
        """
        Menu.__init__(self)

        self._mwindow = p_mwindow

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,
                                                                 os.pardir))

        # New
        self.__new_item = self.create_item("image", "_New Project",
                            os.path.join(root, "images", "new_project.png"))
        self.append(self.__new_item)
        self.__new_item.connect("activate", self.on_new_project_activate)
        
        # Open
        self.__open_item = self.create_item("image", "_Open Project",
                            os.path.join(root, "images", "open_project.png"))
        self.append(self.__open_item)
        self.__open_item.connect("activate", self.on_open_project_activate)

        # Save
        self.__save_item = self.create_item("image", "_Save",
                            os.path.join(root, "images", "save_project.png"))
        self.append(self.__save_item)
        self.__save_item.connect("activate", self.on_save_project_activate)
        self.__save_item.set_sensitive(False)

        # Save As
        self.__save_as_item = self.create_item("image", "Save _As...",
                            os.path.join(root, "images", "save_project_as.png"))
        self.append(self.__save_as_item)
        self.__save_as_item.connect("activate", self.on_save_as_project_activate)
        self.__save_as_item.set_sensitive(False)

        # Delete
        self.__delete_item = self.create_item("image", "Delete Project",
                            os.path.join(root, "images", "delete.png"))
        self.append(self.__delete_item)
        self.__delete_item.connect("activate", self.on_delete_project_activate)
        self.__delete_item.set_sensitive(False)

        # Separator
        self.append(self.create_item("separator"))

        # Import
        self.__import_item = self.create_item("image", "_Import File",
                            os.path.join(root, "images", "import_mfile.png"))
        self.append(self.__import_item)
        self.__import_item.connect("activate", self.on_import_file_project_activate)
        self.__import_item.set_sensitive(False)

        # Separator
        self.append(self.create_item("separator"))

        # Close
        self.__close_item = self.create_item("image", "_Close Project",
                            os.path.join(root, "images", "close_project.png"))
        self.append(self.__close_item)
        self.__close_item.connect("activate", self.on_close_project_activate)
        self.__close_item.set_sensitive(False)

    def on_new_project_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            <New Project>.
        """
        self._mwindow.get_tree_project().new_project()

    def on_open_project_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            <Open Project>.
        """
        self._mwindow.get_tree_project().open_project()
    
    def on_save_project_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            <Save>.
        """
        self._mwindow.get_tree_project().save_project()

    def on_save_as_project_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            <Save As...>.
        """
        self._mwindow.get_tree_project().save_as_project()

    def on_import_file_project_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            <Import File>.
        """
        self._mwindow.get_tree_project().import_m_file()

    def on_close_project_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            <Close>.
        """
        self._mwindow.get_tree_project().confirm_close_project()

        
    def on_delete_project_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            <Delete Project>.
        """    
        self._mwindow.get_tree_project().delete_project()

    def get_new_item(self):
        """
            Retorna: un gtk.ImageMenuItem.
            
            Se utiliza para la optencion del elemento 'self.__new_item'.
        """    
        return self.__new_item

    def get_open_item(self):
        """
            Retorna: un gtk.ImageMenuItem.
            
            Se utiliza para la optencion del elemento 'self.__open_item'.
        """    
        return self.__open_item

    def get_save_item(self):
        """
            Retorna: un gtk.ImageMenuItem.
            
            Se utiliza para la optencion del elemento 'self.__save_item'.
        """    
        return self.__save_item
    
    def get_save_as_item(self):
        """
            Retorna: un gtk.ImageMenuItem.
            
            Se utiliza para la optencion del elemento 'self.__save_as_item'.
        """    
        return self.__save_as_item

    def get_delete_item(self):
        """
            Retorna: un gtk.ImageMenuItem.
            
            Se utiliza para la optencion del elemento 'self.__delete_item'.
        """    
        return self.__delete_item

    def get_import_item(self):
        """
            Retorna: un gtk.ImageMenuItem.
            
            Se utiliza para la optencion del elemento 'self.__import_item'.
        """    
        return self.__import_item

    def get_close_item(self):
        """
            Retorna: un gtk.ImageMenuItem.
            
            Se utiliza para la optencion del elemento 'self.__close_item'.
        """    
        return self.__close_item



