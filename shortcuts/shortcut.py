import gtk
import os
import sys

class Shortcut(gtk.ToolButton):
    """ 
        Representa un shorcut con sus 3 atributos: etiqueta (o label), imagen y
        callback (o comando de octave).
    """
    def __init__(self, p_tool_bar, p_label, p_callback, p_ico):
        """
            p_tool_bar: representa una instancia de ShortcutToolBar.
            p_label: representa una cadena de texto.
            p_callback: representa una cadena de texto.
            p_ico: representa un entero.

            Constructor de la clase Shortcut.
        """ 
        self.__image = self.w_image(p_ico)
        self.__label = p_label
        gtk.ToolButton.__init__(self, self.__image, self.__label)        
        self.__callback = p_callback
        self.set_homogeneous(False)
        self.set_expand(False)
        self.connect("clicked", p_tool_bar.on_click_shortcut)
        self.child.connect("button_press_event", 
                           p_tool_bar.on_button_press_shortcut)        
        self.set_is_important(True)
        self.__ico = p_ico

    def get_callback(self):
        """
            Retorna: una cadena de texto.

            Metodo que devuelve el comando que contiene el shortcut.
        """
        return self.__callback

    def set_callback(self, p_callback):
        """
            p_callback: representa una cadena de texto.

            Metodo para modificar el comando que contiene el shortcut.
        """
        self.__callback = p_callback

    def get_ico(self):
        """
            Retorna: un entero.
    
            Metodo que retorna la posicion que ocupa el icono en la lista de 
            iconos.
        """
        return self.__ico

    def set_ico(self, p_ico):
        """
            p_ico: representa un numero entero.

            Metodo para asignar un nuevo icono al shortcut.
        """
        self.__ico = p_ico
        self.__image = self.w_image(p_ico)
        self.set_icon_widget(self.__image)
        self.show_all()

    def w_image(self, p_ico):
        """
            p_ico: representa un numero entero.

            Retorna: una instancia de GtkImage

            Metodo que carga el icono seleccionado para ser asociado al
            shortcut.
        """
        lista_ico = ["shortcut.png", "icon_1.png", "icon_2.png", "icon_3.png"]
        dire = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]),\
                            "images", lista_ico[p_ico])
        image = gtk.Image()
        image.set_from_file(dire)
        return image
