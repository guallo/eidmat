import os
import gtk

from util.menu import Menu

class MenuMFile(Menu):
    """
        Menu emergente que se muestra al precionarse el click derecho sobre el
        'TreeProject'.
    """
    def __init__(self, p_event, p_tree_project):
        """
            p_tree_project: el 'TreeProject'.
            p_event: el evento que provoco que se muestre el 'TreeProject'.

            Retorna: un 'MenuMFile'.

            Crea un nuevo 'MenuMFile'.
        """
        Menu.__init__(self)

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

        self.__tree_project = p_tree_project

        # Evaluate Selection
        #eval_item = self.create_item("normal", "_Evaluate Selection")
        #eval_item.connect("activate", self.on_eval_activate)

        # Separator
        #sep_item = self.create_item("separator")

        # Edit
        img = os.path.join(root, "images", "cut.png")
        edit_item = self.create_item("image", "Edi_t", img)
        edit_item.connect("activate", self.on_edit_activate)

        # Delete
        delete_item = self.create_item("image", "_Delete", gtk.STOCK_DELETE)
        delete_item.connect("activate", self.on_delete_activate)
     
        # Separator
        sep_item = self.create_item("separator")        

        count = p_tree_project.get_selection().count_selected_rows()
        if not count:
            edit_item.set_sensitive(False)            
            eval_item.set_sensitive(False)
            delete_item.set_sensitive(False)

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

    def on_edit_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 'Edit' del menu 
            emergente.
        """
        self.__tree_project.edit(p_item)

    def on_eval_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 
            'Evaluate Selection' del menu emergente.
        """
        self.__tree_project.evaluate_selection()

    def on_delete_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento 'Delete' del menu
            emergente.
        """
        self.__tree_project.delete_selection()    
