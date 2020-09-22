import os
import sys
import gtk
import gtk.glade
import gtk.gdk

from help.gui.help_window import HelpWindow


class MenuStart():
    """
        Representa el menu asociado al boton Star que se encuentra en la parte 
        inferior izquierda.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: representa el MainWindow.

            Constructor de la clase MenuStart.
        """ 
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        path = os.path.join(root, "images", "gui.glade")
        self.__xml = gtk.glade.XML(path, "start_menu")
        self.__xml.signal_autoconnect(self)

        self.__menu_shortcut = self.__xml.get_widget("start_menu")
        self.__sub_menu_shortcuts = self.__xml.get_widget("sub_menu_shortcuts")
        p_elem = gtk.SeparatorMenuItem()
        p_elem.show_all()
        self.__menu_shortcut.append(p_elem)
        self.__menu_shortcut.reorder_child(p_elem, 1)  
        self.__sub_menu_shor = self.__xml.get_widget("shortcut")	
        self.__mwindow = p_mwindow

    def menu_popup(self, p_widget):
        """
            p_widget: representa un GtkButton.        

            Metodo que permite mostrar el menu emerjente encima del boton 
            <Start>.
        """
        lista = self.__mwindow.get_shortcuts_toolbar().get_children()[1:]
        childer = self.__sub_menu_shortcuts.get_children()
        for i in range(len(childer)):
            self.__sub_menu_shortcuts.remove(childer[i])
        if not lista:
            self._create_element(gtk.MenuItem(), None, "(EMPTY)", None)
        else:
            labels = []
            for i in xrange(len(lista)):
                labels.append(self.__mwindow.get_shortcuts_toolbar().get_label(
                    lista[i].get_children()[0]))                     
            lista_icos = ["shortcut.png", "icon_1.png", "icon_2.png", \
                        "icon_3.png"]
            for i in range(len(labels)):
                item = gtk.MenuItem()
                icon = lista[i].get_ico()
                dire = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]),\
                                    "images")
                self._create_element(item, os.path.join(dire, lista_icos[icon]),
                                     labels[i], self.excec_shortcut)
        self.__boton_start = p_widget
        self.__menu_shortcut.popup(None, None, self.position_actions_menu, 3, 0)

    def position_actions_menu(self, p_menu):
        """
            p_menu: representa un GtkMenu.

            Retorna: un listado donde las dos primeras posiciones representan 
                     las coordenadas X y Y donde se situara el menu y True en 
                     la tercera posicion.

            Metodo que calcula la posicion donde debe aparecer el menu 
        	emergente para que quede encima del boton Start.
    	"""
        x, window_y = \
         self.__boton_start.get_parent_window().get_position()
        rect1 = self.__boton_start.get_allocation()
        whith, heigth = self.__menu_shortcut.size_request()
        whith_b, heigth_b = self.__boton_start.size_request()
        y = window_y + rect1.y - heigth
        push_in = True        
        return (x, y, push_in)

    def on_eidmat_web_site_activate(self, p_widget, p_event = None):
        """
            p_widget: representa un GtkImageMenuItem.
            p_event: representa un GdkEvent.

            Metodo que premite visualizar en el navegador web el sitio web de 
            EIDMAT en internet (http://eidmat.wordpress.com).
        """
        os.system("firefox http://eidmat.wordpress.com/ &")

    def on_web_site_octave_activate(self, p_widget, p_event = None):
        """
            p_widget: representa un GtkImageMenuItem.
            p_event: representa un GdkEvent.

            Metodo que premite visualizar en el navegador web el sitio web de 
            octave en internet (http://www.octave.org).
        """
        os.system("firefox http://www.octave.org &")

    def on_help_menu_activate(self, p_widget):
        """
            Metodo que permite visualizar la ayuda de la aplicacion.
        """
        self.__mwindow.show_help()

    def _create_element(self, p_elem, p_stock, p_text, p_handler):
        """
            p_elem: representa un GtkMenuItem.
            p_stock: representa una cadena de texto (direccion fisica de la 
                     ubicacion de una imagen).
            p_text: representa una cadena de texto.            
            p_handler: representa una referencia al metodo <excec_shortcut>.

            Metodo auxiliar utilizado para la creacion de un <MenuItem> 
            asociado a cada elemento de los shortcuts.
        """
        if p_elem != None:
            hbox = gtk.HBox(False, 5)
            p_elem.add(hbox)
        else:
            p_elem = gtk.SeparatorMenuItem()
        if p_stock != None:
            image = gtk.Image()
            image.set_from_file(p_stock)
            hbox.pack_start(image)
            hbox.set_child_packing(image, False, False, 0, gtk.PACK_START)
        if p_text != None:
            label = gtk.Label(p_text)
            label.set_use_underline(True)
            hbox.pack_start(label)
            hbox.set_child_packing(label, False, False, 0, gtk.PACK_START)        
        if p_handler != None:
            p_elem.connect("button-press-event", p_handler)
            p_elem.connect("activate", p_handler)
        p_elem.show_all()
        self.__sub_menu_shortcuts.append(p_elem)        

    def excec_shortcut(self, p_widget, p_event = None):
        """
            p_widget: representa un GtkMenuItem.
            p_event: representa un GdkEvent.

            Metodo mediante el cual se ejecutan los comandos asociados al 
            callback del shortcut seleccionado en el submenu <Shortcuts> 
            correspondiente al menu emergente referido a la clase <MenuStart>.
        """        
        label = p_widget.get_children()[0].get_children()[1].get_text().strip()
        if p_event == None or p_event.button == 1:
            lista = self.__mwindow.get_shortcuts_toolbar().get_children()[1:]	 
            for i in xrange(len(lista)):
                if label == self.__mwindow.get_shortcuts_toolbar().get_label(
                    lista[i].get_children()[0]).strip():
                    callback = lista[i].get_callback()
                    self.__mwindow.get_shortcuts_toolbar().excect_command(callback)
                    break
