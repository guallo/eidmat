import gtk
import os
import sys

from shortcuts.shortcut_editor import ShortcutEditor
from shortcuts.organize_shortcut import OrganizeShortcut
from shortcuts.shortcut import Shortcut


class ShortcutToolBar(gtk.Toolbar):
    """
        Representa la barra de shortcuts. Esta clase implementa los metodos 
        asociados a la creacion, edicion y reorganizacion de los shortcuts asi
        como aquellos asociados a la ejecucion de los callback.    
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: representa el MainWindow.

            Constructor de la clase ShortcutToolBar.
        """ 
        gtk.Toolbar.__init__(self)
        self.__visible_shortcut = True
        self.__main_win = p_mwindow
        self.connect("button_press_event", self.on_button_press_event)
        label = gtk.Label("Shortcuts")
        item = gtk.ToolItem()
        item.add(label)
        self.insert(item, 0)
        self.__edit_shortcut = None	 
        self.__shortcut_editor = ShortcutEditor(self)
        self.__organize_shortcuts = OrganizeShortcut(self)
        self.__organize_list_store = False
        p_mwindow.get_popup_menu().set_shortcuts_toolbar(self)
        self.load_shortcut()
        self.show_all()

    def on_button_press_shortcut(self, p_widget, p_event):
        """
            p_widget: representa una instancia de GtkButton.
            p_event: representa una instancia de GdkEvent.

            Metodo que muestra un menu emergente tras hacer clic derecho sobre
            un shortcut.
        """
        if p_event.button == 3: # Click derecho            
            label = self.get_label(p_widget)
            lista = self.get_children()[1:]
            for i in xrange(len(lista)):
                label2 = self.get_label(lista[i].get_children()[0])
                if label == label2:
                    self.__edit_shortcut = lista[i]
                    break
            self.__main_win.get_popup_menu()._popup(p_event)

    def on_click_shortcut(self, p_widget):    
        """
            p_widget: representa una instancia de GtkToolButton.

            Metodo que permite, mediante una llamada al metodo auxiliar 
            <excect_command>, ejecutar el callback asociado al shorcut 
            <p_widget>.
        """
        self.excect_command(p_widget.get_callback())

    def excect_command(self, p_command):
        """
            p_command: representa una cadena de texto.

            Metodo auxiliar que permite ejecutar el callback asociado a un 
            shortcut.
        """ 
        if p_command[-1] != "\n":
            p_command += "\n"	
        self.__main_win.get_cmdwindow().evaluate(p_command)

    def on_button_press_event(self, p_widget, p_event):
        """
            p_widget: representa una instancia de GtkToolbar.
            p_event: representa una instancia de GdkEvent.
            
            Metodo que muestra un menu emergente tras hacer clic derecho sobre
            la barra de shortcuts.
        """
        if p_event.button == 3:
            self.__main_win.get_popup_menu()._popup2(p_event)

    def delete_shortcut(self):
        """
            Metodo para eliminar un shortcut.
        """
        self.remove(self.__edit_shortcut)

    def	on_new_shortcut_activate(self):
        """
            Metodo que muestra la ventana <shortcut editor> tras solicitar la
            creacion de un nuevo shortcut.
        """
        if not self.__shortcut_editor.is_show():            
            self.__shortcut_editor.show_()
        else:
            self.__shortcut_editor.present()

    def verify_create_chortcut(self, p_label):
        """
            p_label: representa una cadena de texto.

            Retorna: True o False

            Metodo que verifica la existencia de un shortcur con el nombre 
            <p_label> y de ser asi retorna Falso. En caso contrario retorna
            Verdadero.
        """	
        lista = self.get_children()[1:]
        for i in xrange(len(lista)):
            if p_label == self.get_label(lista[i].get_children()[0]).strip():
                return False
        return True

    def	create_chortcut(self, p_label, p_callback, p_ico):
        """
            p_label: representa una cadena de texto.
            p_callback: representa una cadena de texto.
            p_ico:  representa un numero entero.
            
            Metodo para crear un nuevo shortcut a partir de los parametros de
            entrada.
        """
        shortcut = Shortcut(self, p_label, p_callback, p_ico)
        self.insert(shortcut, -1)
        shortcut.show_all()
        if self.__organize_list_store:
            self.__organize_shortcuts.w_listore()

    def	save_shortcut(self):
        """
            Metodo encargado de realizar la salva de los shortcuts en la 
            seccion propia de cada usuario.
        """	
        lista = self.get_children()[1:]	 
        dir_ = os.path.join(os.environ['HOME'], '.shortcuts_EIDMAT')
        f = open(dir_, "w")
        f.write("")
        if self.__visible_shortcut:
            f.writelines("v\n")
        else:
            f.writelines("f\n")	
        if lista:
            for i in xrange(len(lista)):
                label = self.get_label(lista[i].get_children()[0])
                callback = lista[i].get_callback()
                ico = lista[i].get_ico()
                f.writelines(label + '\n')
                f.writelines(str(ico) + '\n')
                f.writelines(callback + '\n' + "12__back" + '\n')                
            f.close()

    def load_shortcut(self):
        """
            Metodo para cargar los shortcuts desde el fichero generado en la 
            seccion del usuario, una vez iniciada la aplicacion.
        """
        dir_ = os.path.join(os.environ['HOME'], '.shortcuts_EIDMAT')
        if os.path.exists(dir_):
            f = open(dir_, "r")
            show = linea = f.readline().strip()
            if show == "f":
                self.__visible_shortcut = False
                self.__main_win.get_popup_menu().set_active()
            else:                
                self.__visible_shortcut = True
                self.show_labels()
            while True:
                linea = f.readline()
                if not linea:
                    break                      
                label = linea.replace('\n','')
                ico = f.readline().strip()
                ico = int(ico)
                aux = f.readline()
                callback = ""
                while aux != "12__back\n":                    
                    callback += aux
                    aux = f.readline()
                callback = callback[:-1]
                self.create_chortcut(label, callback, ico)
            f.close()

    def on_edit_activate (self, p_widget):
        """
            p_widget: representa un GtkImageMenuItem.
        
            Metodo que muestra la ventana <shortcut editor> para posibilitar al 
            usuario la edicion de un shortcut. Si la ventana se encuentra 
            activa esta se mostrara al frente.
        """	
        if not self.__shortcut_editor.is_show():	    
            label = self.get_label(
                self.__edit_shortcut.get_children()[0])
            callback = self.__edit_shortcut.get_callback()
            ico = self.__edit_shortcut.get_ico()
            self.__shortcut_editor.edit_shortcut(label, callback, ico)
        else:
            self.__shortcut_editor.present()

    def modify_chortcut(self, p_name, p_label, p_callback, p_ico):
        """
            p_name: representa una cadena de texto.
            p_label: representa una cadena de texto.
            p_callback: representa una cadena de texto.
            p_ico: representa un numero entero.

            Retorna True o False

            Metodo que permite modificar atributos de un shortcut existente. 
            Puede modificarse la etiqueta, el callback, el icono o cualquier 
            combinacion factible de estos. 
            El metodo retornara Falso si ya existia un label con ese nombre y 
            Verdadero si se realizo alguna modificacion de manera satisfactoria.            
        """
        lista = self.get_children()[1:]
        label_list = []
        if lista:
            for i in xrange(len(lista)):
                label_list.append(self.get_label(
                    lista[i].get_children()[0]).strip())
                if self.get_label(
                    lista[i].get_children()[0]).strip() == p_name:
                    self.__edit_shortcut = lista[i]
        if p_name != p_label and (not p_label in label_list):
            self.__edit_shortcut.set_callback(p_callback)
            self.__edit_shortcut.set_ico(p_ico)
            self.__edit_shortcut.set_label(p_label)
        elif p_name == p_label:
            self.__edit_shortcut.set_callback(p_callback)
            self.__edit_shortcut.set_ico(p_ico)
        elif p_label in label_list:
            return False    
        if self.__organize_list_store:
            self.__organize_shortcuts.w_listore()
        return True

    def on_organize_shortcuts_activate(self, p_window):
        """
            p_window: representa un GtkImageMenuItem.
            
            Metodo que muestra el cuadro de dialogo relativo a la organizacion
            de los shortcuts. Si la misma se encuentra activa esta se presenta 
            al frente.
        """
        if not self.__organize_shortcuts.is_show():
            self.__organize_shortcuts.show_()
        else:	    
            self.__organize_shortcuts.present()

    def edit_shorcut_organize(self, p_label):       
        """
            p_label: representa una cadena de texto.

            Metodo que permite editar un shortcut desde el cuadro de dialogo 
            destinado a la organizacion de los shortcuts.
        """	
        if not self.__shortcut_editor.is_show():
            lista = self.get_children()[1:]
            if lista:
                for i in xrange(len(lista)):
                    if self.get_label(
                        lista[i].get_children()[0]) == p_label:
                        callback = lista[i].get_callback()
                        ico = lista[i].get_ico()
                        break
            self.__shortcut_editor.edit_shortcut(p_label, callback, ico)	 
        else:
            self.__shortcut_editor.present()

    def get_label(self, p_widget):
        """
            p_widget: representa un GtkButton.
            
            Retorna: una cadena de texto.

            Metodo que retornar la etiqueta de un shortcut dado un widget.
        """
        if not self.__visible_shortcut:
            self.show_labels()
        label = p_widget.get_children()[0].get_children()[1].get_text()
        if not self.__visible_shortcut:
            self.hide_labels()
        return label

    def move_shortcut(self, p_posi, p_posf):
        """
            p_posi: un numero entero.
            p_posf: un numero entero.
    
            Metodo que permite trasladar hacia a la derecha o izquierda un 
            shortcut.
        """
        element = self.get_children()[p_posi + 1]
        self.remove(self.get_children()[p_posi + 1])
        self.insert(element, p_posf + 1)	

    def set__edit_shortcut(self, p_e_short):
        """
            p_e_short: representa un GtkToolButton.

            Metodo destinado a contener en una variable el shortcut que se 
            desea modificar ya sea para su eliminacion o edicion desde las 
            diferentes ventanas.
        """
        self.__edit_shortcut = p_e_short

    def set_organize_list_store(self):
        """
            Metodo para reconocer modificaciones realizadas sobre algun 
            shortcut siempre que este activa la ventana <shortcut organizer>.
        """
        self.__organize_list_store = True

    def show_labels(self):
        """
            Metodo que muestra la etiqueta de los shortcuts junto a los iconos.
        """
        self.set_style(gtk.TOOLBAR_BOTH_HORIZ)

    def hide_labels(self):
        """
            Metodo que oculta la etiqueta de los shortcuts y mantiene solo los 
            iconos.
        """
        self.set_style(gtk.TOOLBAR_ICONS)

    def set_visible_shortcut(self, p_visible):
        """
            p_visible: representa True o False.
    
            Metodo que controla la visibilidad o no de las etiquetas de los
            shortcuts.
        """
        self.__visible_shortcut = p_visible


    def get_labels_icos(self):
        """
            Retorna: una lista generica.

            Metodo que devuelve una lista generica con dos listas asociadas y
            llenas a partir de las etiquetas de los shortcuts y los iconos 
            asociados a los mismos respectivamente.
        """	
        lista = self.get_children()[1:]
        label_list = []
        label_icos = []
        if lista:
            for i in xrange(len(lista)):
                label_list.append(self.get_label(lista[i].get_children()[0]))
                label_icos.append(lista[i].get_ico())
        lista_label_ico = [label_list, label_icos]
        return lista_label_ico

