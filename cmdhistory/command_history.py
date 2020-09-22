import gtk
import time
import os
import gobject

from util.confirm import Confirm
from cmdhistory.menu_history import MenuHistory
from menubar.cmdhistory_menu_bar import CMDHistoryMenuBar
from toolbar.cmdhistory_toolbar import CMDHistoryToolbar


class CommandHistory(gtk.TreeView):
    """
        El historial de comandos de la aplicacion.
    """
    def __init__(self, p_mwindow, p_parent):
        """
            p_mwindow: un 'MainWindow'.
            p_parent:  un 'gtk.Window' que es la ventana principal.

            Retorna:   un nuevo 'CommandHistory'.

            Crea un nuevo 'CommandHistory' en el que se cargan los datos 
            guardados en el fichero correspondiente al mismo, ademas de 
            adicionar la fecha en que se abre la aplicacion si no se encuentra
            en los datos cargados.
        """
        # Proyecto
        self.__project = False
        self.__localization = None

        self.__tree = gtk.TreeStore(str)
        gtk.TreeView.__init__(self, self.__tree)
        
        column = gtk.TreeViewColumn()
        cell = gtk.CellRendererText()
        column.pack_start(cell)
        column.add_attribute(cell, "text", 0)
        self.append_column(column)
        self.set_headers_visible(False)
        self.set_enable_tree_lines(True)
        self.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        
        self.__copy_of_history = []
        self._load()
        date = self._get_date()
        if len(self.__tree) != 0:
            if date != self.__tree[self.__tree[len(self.__tree) - 1].path][0]:
                self.__tree.append(None, [date])
        else:
            self.__tree.append(None, [date])
        self._update_copy()
        gobject.idle_add(lambda: self.scroll_to_cell(
                                                   self.__copy_of_history[-1])
                                                    )
        
        self.connect('button-press-event', self.on_button_press_event)
        self.connect("event-after", self.on_event_after)
        self.connect("key-press-event", self.on_key_press_event)
        self.connect("row-activated", self.on_row_activated)
        self.connect("focus-in-event", lambda p_cmdhistory, p_event:
                                              self.activate())
        self.get_selection().connect("changed", lambda p_selec:
                                                      self.update_appearance())

        self.__mwindow = p_mwindow
        self.__parent = p_parent
        self.__mbar = CMDHistoryMenuBar(p_mwindow)
        self.__tbar = CMDHistoryToolbar(p_mwindow)

        self.__pointer = {"text": None, "row": None, "patron": None}
        self.__show_menu = True
        self.__confirmed_del = False

        self.update_appearance()

    def get_mbar(self):
        """
            Retorna: un CMDHistoryMenuBar.

            Devuelve la barra de menus del CommandHistory.
        """
        return self.__mbar

    def _update_copy(self):
        """
            Metodo que actualiza el fichero del historial de comandos
            y el atributo 'CommandHistory.__copy_of_history' cada vez
            que se realiza una accion que modifique el historial de 
            comandos, e.g. 'adicionar', 'cortar'.
        """
        path = os.path.join(os.environ["HOME"], "command_history")
        if self.__project:
            path = os.path.join(self.__localization, "HIST", ".hist.txt~")
        history = self._open_file("w", path)
        model = self.__tree
        copy = []
        
        for row in model:
            copy.append(row.path)
            f = model[row.path][0]
            history.write("\t" + model[row.path][0] + "\n")
            
            for i in xrange(model.iter_n_children(row.iter)):
                copy.append((row.path[0], i))
                history.write(model[(row.path[0], i)][0] + "\n")
                
        self.__copy_of_history = copy
        history.close()
 
    def on_button_press_event(self, p_history, p_event):
        """
            p_history: el 'CommandHistory'.
            p_event:   el evento que desencadeno la sennal.

            Retorna:   'True' si se presiono click derecho sobre el 
                       'CommandHistory'. 
                       'True' causa que se detengan otros manejadores que se
                        invoquen para el evento.

            Se ejecuta cada vez que se presiona un boton del mouse sobre el
            'CommandHistory'. Chequea si ocurrio el click derecho,
            en ese caso lanza el menu emergente('MenuHistory') asociado 
            al 'CommandHistory'.
        """
        flags = p_event.state

        if p_event.button == 3:
            self.__show_menu = True
            pos = self.get_path_at_pos(int(p_event.x), int(p_event.y))

            if pos and not int(gtk.gdk.CONTROL_MASK & flags) and\
                       not int(gtk.gdk.SHIFT_MASK & flags) and\
                       self.get_selection().path_is_selected(pos[0]):

                MenuHistory(p_event, self)
                self.__show_menu = False
                return True

    def on_event_after(self, p_history, p_event):
        """
            p_history: 'CommandHistory'.
            p_event:   el evento que desencadeno la sennal.

            Se ejecuta despues de que ocurra cualquier otro manejador de
            evento para 'CommandHistory'. Chequea si el evento que ocurrio fue
            el de presionar un boton del mouse, en ese caso, verifica si fue
            click derecho y en ese caso si el atributo
            'CommandHistory.__show_menu' tiene 'True' entonces se lanza 
            el menu emergente('MenuHistory') asociado al 'Commandhistory'.
        """
        if p_event.type == gtk.gdk.BUTTON_PRESS and\
           p_event.button == 3 and self.__show_menu:

            MenuHistory(p_event, self)

        
    def on_key_press_event(self, p_cmdhistory, p_event):
        """
            p_cmdhistory: el 'CommandHistory'.
            p_event:      el evento que desencadeno la sennal.

            Retorna:      'True' si se presiono la tecla 'Enter'. Retornar
                          'True' detiene otros manejadores que se invocan
                           para el evento.

            Este metodo es llamado cuando se presiona una tecla sobre
            'p_cmdhistory'.

            Ctrl+X:              llama el metodo 'CommandHistory.cut'.
            Ctrl+C, Ctrl+Insert: llama el metodo 'CommandHistory.copy'
            Delete:              llama el metodo 'CommandHistory.delete_selection'
            Enter, Space:        llama el metodo 'Commandhistory.evaluate_selection'
        """
        ascii = p_event.keyval
        flags = p_event.state
        
        if ascii in (88, 120, 99, 67, 65379):  # x, X, c, C, insert
            if int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and\
               not int(gtk.gdk.MOD1_MASK & flags):

                {88: self.cut, 120: self.cut, 99: self.copy, 67: self.copy,
                 65379: self.copy}[ascii]()
            
        elif ascii == 65535:  # delete
            self.delete_selection()

        elif ascii in (65293, 65421, 32):  # enter izq, enter der, space
            self.evaluate_selection()
            return True

    def on_row_activated(self, p_cmdhistory, p_path, p_col):
        """
            p_cmdhistory: el 'CommandHistory' que recibio la sennal.
            p_path: un camino de arbol que apunta a la fila activada.
            p_col:  la columna en la fila activada.
			
            Se ejecuta cuando el usuario da doble click o presiona la tecla
            'Enter' sobre alguna fila del historial de comandos('CommandHistory').
            Llama el metodo 'CommandHistory.evaluate_selection'.
        """
        self.evaluate_selection()

    def _open_file(self, p_mode, p_path):
        """
            p_mode: el modo de abrir el fichero donde se guardan los datos del
					historial de comandos. 'p_mode' puede ser "r" si lo que se
					quiere es leer, o "w" para escribir en el fichero.
			p_path: una cadena que representa el camino del fichero que guarda
                    los datos del historial de comandos.
			
            Retorna: un 'file' que es la instancia del fichero abierto.

            Metodo auxiliar que retorna una instancia del fichero utilizado
            para guardar los datos del historial de comandos.
            Antes que todo se chequea si existe el fichero, de no ser asi, se
            crea uno nuevo.
        """
        if p_mode == "r":
            f = open(p_path, 'a')
            f.close()
        return open(p_path, p_mode)

    def _load(self):
        """
           Metodo que se ejecuta cuando inicia la aplicacion, es el encargado
           de inicializar el historial de comandos con los datos que quedaron 
           guardados en el fichero correspondiente al mismo.
        """
        model = self.__tree
        path = os.path.join(os.environ["HOME"], "command_history")
        if self.__project:
            path = os.path.join(self.__localization, "HIST", ".hist.txt~")
        file_ = self._open_file("r", path)
        for line in file_:
            if line[0] == "\t":
                iter_ = model.append(None, [line.strip()])
            else:
                model.append(iter_, [line.strip()])
                self.expand_to_path(model.get_path(iter_))
        file_.close()
        
    def append(self, p_text):
        """
            p_text: cadena que contiene cada comando que mandamos a ejecutar en
		            la ventana de comandos.

            Se ejecuta cuando mandamos a ejecutar un comando en la ventana de 
            comandos y su funcionalidad es adicionar este al historial de 
            comandos y al fichero correspondiente al mismo.
        """
        model = self.__tree
        last_cmd = model[self.__copy_of_history[-1]][0]
        parent = model[len(model) - 1]
        flag = False
        
        for text in p_text.strip().split("\n"):
            if  last_cmd != text and text.strip():
                model.append(parent.iter, [text])
                last_cmd = text
                flag = True

        if flag:
            self.expand_to_path(parent.path)
            self._update_copy()
            gobject.idle_add(lambda:
                             self.scroll_to_cell(self.__copy_of_history[-1]))

    def _get_date(self):
        """
            Retorna: la fecha actual con el formato que se mostrara en el
                     historial de comandos.

            Metodo que convierte la fecha actual en el formato que sera 
            mostrado en el historial de comandos 
            (%-- mes/dia/anno  hora:minuto --%)
        """
        struct = time.localtime()
        date = time.strftime("%-- %m/%d/%y  %I:%M ", struct)
        if 0 <= struct[3] <= 11:
            return date + "AM --%"
        return date + "PM --%"
    
    def copy(self):
        """
            Retorna: una lista con las direcciones de las filas seleccionadas
            	     en el historial de comandos.

            Si hay seleccion en el 'CommandHistory', entonces se copia al
            'gtk.Clipboard' el texto comprendido en la misma
        """
        list_of_path = self.get_selection().get_selected_rows()[1]

        if list_of_path:
            value = ""
            for path in list_of_path:
                value += self.__tree[path][0] + "\n"
            self.get_clipboard('CLIPBOARD').set_text(value.strip())
        return list_of_path
        
    def cut(self):
        """
            Corta los comandos seleccionados en el historial de comandos,
            en caso de que alguno no pueda ser cortado solo lo copia.
        """
        list_of_path = self.copy()

        if list_of_path:
            self._delete_paths(list_of_path)
            self._update_copy()

    def _delete_paths(self, p_list_of_path):
        """
            p_list_of_path: una lista que contiene los caminos de las filas
                            que contienen los datos que queremos eliminar.

            Este metodo elimina si es posible los caminos
            pasados como parametros del historial de comandos
            y del fichero correspondiente al mismo.
        """
        model = self.__tree
        copy = self.__copy_of_history
        
        if self.__pointer["row"] != None:
            p_r = copy[self.__pointer["row"]]
        
        for i in xrange(len(p_list_of_path) - 1, -1, -1):
            path = p_list_of_path[i]
            iter_ = model.get_iter(path)
            if not model.iter_has_child(iter_) and path != model[len(model) - 1].path:
                model.remove(iter_)
                
                if self.__pointer["row"] != None and path < p_r:
                    self.__pointer["row"] -= 1
   
    def clear(self):
        """
            Elimina todos los datos del historial de comandos y del fichero
            correspondiente al mismo, dejando en estos solo la fecha mas
            reciente.
        """
        if not self.__project:
            msg = "Are you sure you want to delete your entire history?"
            resp = Confirm(gtk.STOCK_DIALOG_QUESTION, msg, "Command History",
                       self.__parent).run()
            if not resp:
                return
        model = self.__tree
        date = model[model[len(model) - 1].path][0]
        model.clear()
        model.append(None, [date])
        
        if self.__pointer["row"] != None:
            if model[len(model) - 1].path < self.__copy_of_history[self.__pointer["row"]]:
                self.__pointer["row"] = 1
            else:
                self.__pointer["row"] = 0
    
        self._update_copy()

    def delete_selection(self):
        """
            Elimina todos los datos seleccionados, del historial de comandos
            y del fichero correspondiente al mismo.
        """
        paths = self.get_selection().get_selected_rows()[1]

        if paths:
            if not self.__confirmed_del:
                msg = "All selected commands will be deleted."
                resp = Confirm(gtk.STOCK_DIALOG_WARNING, msg,
                               "Command History", self.__parent,
                               "Do not show this prompt again.").run()
                if not resp:
                    return
                if resp[0]:
                    self.__confirmed_del = True
            self._delete_paths(paths)
            self._update_copy()
    
    def delete_to_selection(self):
        """
            Elimina del historial de comandos y del fichero 
            correspondiente al mismo todos los datos hasta la seleccion.
        """
        paths = self.get_selection().get_selected_rows()[1]

        if len(paths) != 1:
            return

        resp = Confirm(gtk.STOCK_DIALOG_QUESTION,
                       "Are you sure you want to delete all commands above the selected command?",
                       "Command History",
                       self.__parent).run()
        if resp:
            copy = self.__copy_of_history
            self._delete_paths(copy[: copy.index(paths[0])])
            self._update_copy()
        
    def evaluate_selection(self):
        """
            Evalua los comandos seleccionados como si el usuario los ubiese
            entrado por teclado en la ventana de comandos.
        """
        model, paths = self.get_selection().get_selected_rows()

        if paths:
            text = "\n".join([model[path][0] for path in paths])
            self.__mwindow.get_cmdwindow().evaluate(text + "\n")
        
    def look_up(self, p_text):
        """
			p_text:  una cadena que es el comando actual escrito en el
					 'CommandWindow'.

			Retorna: una cadena que representa el proximo comando que coincide
					 con el patron de busqueda.

			Busca hacia arriba en el historial el primer comando que enlace
			con el patron de busqueda.
        """
        copy = self.__copy_of_history
        pointer = self.__pointer
        
        if pointer["text"] != p_text:
            pointer["patron"] = p_text
            pointer["row"] = len(copy) - 1
        else:
            pointer["row"] -= 1
            
        if pointer["row"] < 0:
            pointer["text"] = None
            pointer["row"] = None
            return pointer["patron"]
        
        for row in xrange(pointer["row"], -1, -1):
            value = self.__tree[copy[row]][0]
            if value.startswith(pointer["patron"]):
                pointer["text"] = value
                pointer["row"] = row
                return value

        pointer["text"] = None
        pointer["row"] = None
        return pointer["patron"]
    
    def look_down(self, p_text):
        """
			p_text:  Una cadena que es el comando actual escrito en el
					 'CommandWindow'.

			Retorna: una cadena que representa el proximo comando que coincide
					 con el patron de busqueda.

			Busca hacia abajo en el historial el primer comando que enlace con
			el patron de busqueda.
        """        
        copy = self.__copy_of_history
        pointer = self.__pointer
        
        if pointer["text"] != p_text:
            pointer["text"] = None
            pointer["row"] = None
            return p_text

        pointer["row"] += 1
            
        if pointer["row"] >= len(copy):
            pointer["text"] = None
            pointer["row"] = None
            return pointer["patron"]
        
        for row in xrange(pointer["row"], len(copy)):
            value = self.__tree[copy[row]][0]
            if value.startswith(pointer["patron"]):
                pointer["text"] = value
                pointer["row"] = row
                return value

        pointer["text"] = None
        pointer["row"] = None
        return pointer["patron"]
    
    def select_all(self):
        """
            Selecciona todos los datos en el historial de comandos.
        """
        self.get_selection().select_all()

    def update_appearance(self):
        """
            Actualiza la apariencia de los menus correspondientes al 
            Command History, decidiendo cuales de estos se mostraran
            activos o no en dependencia de las acciones que se puedan
            realizar.
        """
        edit_menu = self.__mbar.get_edit()
        tbar = self.__tbar
        selec = self.get_selection()

        if selec.count_selected_rows():
            edit_menu.get_cut().set_sensitive(True)
            edit_menu.get_copy().set_sensitive(True)
            edit_menu.get_delete().set_sensitive(True)

            tbar.get_cut().set_sensitive(True)
            tbar.get_copy().set_sensitive(True)
        else:
            edit_menu.get_cut().set_sensitive(False)
            edit_menu.get_copy().set_sensitive(False)
            edit_menu.get_delete().set_sensitive(False)

            tbar.get_cut().set_sensitive(False)
            tbar.get_copy().set_sensitive(False)
        
        #if self.__project:
        #    project_menu.get_project().get_p_menu()

    def activate(self):
        """
            Resalta el Command History y muestra la barra de menu y de
            herramientas del mismo.
        """
        self.__mwindow.set_menu_bar(self.__mbar, self.__tbar, 1)

    def set_project(self, p_project, p_localization = None):
        """
            p_project: True o False. Identifica si se esta trabajando en un 
                       proyecto o no
		
            p_localization: una cadena de texto. Representa la localizacion 
                            del proyecto
 
            Asigna nuevos valores a las variables <self.__project> y 
            <self.__localization>
        """        
        self.__project = p_project
        self.__localization = p_localization
    
    def clear_entire_history(self):        
        """
            Elimina todos los datos del historial de comandos para levantar el 
            historial que no pertenece al proyecto.
        """        
        model = self.__tree        
        model.clear()
        self._load()
        model = self.__tree
        copy = []        
        for row in model:
            copy.append(row.path)
            for i in xrange(model.iter_n_children(row.iter)):
                copy.append((row.path[0], i))
        self.__copy_of_history = copy
        
