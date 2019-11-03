import os
import gtk

from util.menu import Menu


class MenuHistory(Menu):
    """
        El menu emergente que se muestra cuando se presiona click derecho
        sobre el 'CommandHistory'.
    """
    def __init__(self, p_event, p_history):
        """
            p_history: el 'Commandhistory'.
            p_event:   el evento que provoco que se muestre el
                       'MenuHistory'.

            Retorna:   un 'MenuHistory'.

            Crea un nuevo 'MenuHistory'.
        """
        Menu.__init__(self)

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

        self.__history = p_history

        # Evaluate Selection
        eval_item = self.create_item("normal", "_Evaluate Selection")
        eval_item.connect("activate", self.on_eval_activate)

        # Separator
        sep_item = self.create_item("separator")

        # Cut
        img = os.path.join(root, "images", "cut.png")
        cut_item = self.create_item("image", "Cu_t", img, "Ctrl+X")
        cut_item.connect("activate", self.on_cut_activate)
        
        # Copy
        img = os.path.join(root, "images", "copy.png")
        copy_item = self.create_item("image", "_Copy", img, "Ctrl+C")
        copy_item.connect("activate", self.on_copy_activate)

        # Delete
        delete_item = self.create_item("image", "_Delete", gtk.STOCK_DELETE)
        delete_item.connect("activate", self.on_delete_activate)

        # Delete to Selection
        delete_to_item = self.create_item("normal", "Delete _to Selection")
        delete_to_item.connect("activate", self.on_delete_to_activate)
     
        # Separator
        sep_item = self.create_item("separator")
        
        # Clear Command History
        clear_item = self.create_item("normal", "Clear Command _History")
        clear_item.connect("activate", self.on_clear_activate)

        count = p_history.get_selection().count_selected_rows()
        if not count:
            cut_item.set_sensitive(False)
            copy_item.set_sensitive(False)
            eval_item.set_sensitive(False)
            delete_item.set_sensitive(False)
            delete_to_item.set_sensitive(False)
        elif count > 1:
            delete_to_item.set_sensitive(False)

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

    def on_cut_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Cut'.
            Llama el metodo 'CommandHistory.cut'.
        """
        self.__history.cut()

    def on_copy_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Copy'.
            Llama el metodo 'CommandHistory.copy'.
        """
        self.__history.copy()

    def on_eval_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Evaluate Selection'.
            Llama el metodo 'CommandHistory.evaluate_selection'.
        """
        self.__history.evaluate_selection()

    def on_delete_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Delete'.
            Llama el metodo 'CommandHistory.delete_selection'.
        """
        self.__history.delete_selection()

    def on_delete_to_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Delete to Selection'.
            Llama el metodo 'CommandHistory.delete_to_selection'.
        """
        self.__history.delete_to_selection()

    def on_clear_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Clear Command History'. Llama el metodo 'CommandHistory.clear'
        """
        self.__history.clear()
