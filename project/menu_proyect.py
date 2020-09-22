import os
import gtk

from util.menu import Menu


class MenuProyect(Menu):
    """
        Menu emergente que se muestra al ser presionado el click derecho
        sobre el nombre del proyecto en el treeview del proyecto.
    """
    def __init__(self, p_event, p_tree_project):
        """
            p_tree_project: el 'ThreeProject'.
            p_event: el evento que provoco que se muestre el
                     'MenuProyect'.

            Retorna: un 'MenuProyect'.

            Crea un nuevo 'MenuProyect'.
        """
        Menu.__init__(self)

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        self.__tree_project = p_tree_project

        # Save
        img = os.path.join(root, "images", "save_project.png")
        save_item = self.create_item("image", "_Save", img)
        save_item.connect("activate", self.on_save_activate)

        # Save As
        img = os.path.join(root, "images", "save_project_as.png")
        save_as_item = self.create_item("image", "Save _As...", img)
        save_as_item.connect("activate", self.on_save_as_activate)

        # Delete
        img = os.path.join(root, "images", "delete.png")
        delete_item = self.create_item("image", "Delete Project", img)
        delete_item.connect("activate", self.on_delete_activate)

        # Separator
        sep_item = self.create_item("separator")

        # Import
        img = os.path.join(root, "images", "import_mfile.png")
        import_item = self.create_item("image", "_Import File", img)
        import_item.connect("activate", self.on_import_activate)        
     
        # Separator
        sep_item = self.create_item("separator")  

        # Close
        img = os.path.join(root, "images", "close_project.png")
        close_item = self.create_item("image", "_Close Project", img)
        close_item.connect("activate", self.on_close_activate)

        count = p_tree_project.get_selection().count_selected_rows()
        if not count:
            import_item.set_sensitive(False)            
            save_item.set_sensitive(False)
            save_as_item.set_sensitive(False)
            delete_item.set_sensitive(False)
            import_item.set_sensitive(False)
            close_item.set_sensitive(False)

        Menu.popup(self, None, None, None, 3, p_event.time)
    
    def create_item(self, p_type, p_text=None, p_stock=None, p_accel=None):
        """
            p_type:  una cadena que representa el tipo de elemento de menu a
                     crear. 'p_type' puede ser "normal", "image", "check",
                     "radio" o "separator".
            p_text:  una cadena a mostrar por el elemento de menu.
            p_stock: una cadena que represente un 'stock de gtk' o una
                     direccion de una imagen a mostrar por el elemento de menu.
            p_accel: una cadena que representa la combinacion de teclas que
                     activa a dicho elemento de menu. 'p_accel' es lo ultimo
                     que se muestra en el elemento de menu.

            Retorna: un 'gtk.MenuItem' en dependencia de los parametros dados.

            Crea, adiciona y retorna un elemento de menu segun los parametros
            dados.
        """
        item = Menu.create_item(self, p_type, p_text, p_stock, p_accel)
        item.show_all()
        self.append(item)
        return item

    def on_save_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 'Save' del menu.            
        """
        self.__tree_project.save_project()

    def on_save_as_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 'Save As...' del 
            menu.            
        """
        self.__tree_project.save_as_project()    

    def on_delete_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 'Delete Proyect'
            del menu.
        """
        self.__tree_project.delete_project()  

    def on_import_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 'Import File' del 
            menu.
        """
        self.__tree_project.import_m_file()  

    def on_close_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 'Close Project' del
            menu.
        """
        self.__tree_project.confirm_close_project()  
    
