import gtk
import time
import os
import gobject

from util.confirm import Confirm
from project.menu_m_file import MenuMFile
from project.menu_proyect import MenuProyect
from project.c_project import Project
from project.dialog_create_project import Dialog_create_project
from cmds.manage_path import ManageCommandPro
from cmds.load_vars import LoadVars
from cmds.delete_var import DeleteVar
from menubar.project_menu_bar import ProjectMenuBar
from toolbar.project_toolbar import ProjectToolbar


class TreeProject(gtk.TreeView):
    """
        Clase que representa el TreeView del proyecto.
    """
    def __init__(self, p_mwindow, p_parent):
        """
            p_mwindow: un 'MainWindow'.
            p_parent: un 'gtk.Window' que es la ventana principal.

            Retorna: un nuevo 'TreeProject'.

            Crea un nuevo 'TreeProject' en el que se carga la informacion 
            referida al proyecto que haya sido guardada previamente.
        """
        # Proyecto
        self.__project = None
        self.__tree = gtk.TreeStore(gtk.gdk.Pixbuf, str)
        gtk.TreeView.__init__(self, self.__tree)
        
        column = gtk.TreeViewColumn()
        cell = gtk.CellRendererPixbuf()
        column.pack_start(cell, False)
        column.add_attribute(cell, "pixbuf", 0)

        cell = gtk.CellRendererText()
        column.pack_start(cell)
        column.add_attribute(cell, "text", 1)

        self.append_column(column)

        self.set_headers_visible(False)
        self.set_enable_tree_lines(True)
        self.get_selection().set_mode(gtk.SELECTION_MULTIPLE)        
        self.__mwindow = p_mwindow
        self.__parent = p_parent        
        self.connect('button-press-event', self.on_button_press_event)
        self.connect("row-activated", self.on_row_activated)
        self.connect("focus-in-event", lambda p_cmdhistory, p_event:
                                              self.activate())
        self.connect("key-press-event", self.on_key_press_event)
        self.__mbar = ProjectMenuBar(p_mwindow)
        self.__tbar = ProjectToolbar(p_mwindow)

    def get_mbar(self):
        """
            Retorna: un ProjectMenuBar.

            Devuelve la barra de menus del TreeProject.
        """
        return self.__mbar
        
    def on_button_press_event(self, p_tree, p_event):
        """
            p_tree:  el 'TreeProject'.
            p_event: el evento que desencadeno la sennal.

            Retorna: 'True' si se presiono click derecho sobre el 
                     'TreeProject'. Retornar 'True' causa que se detengan otros
                     manejadores que se invoquen para el evento.

            Se ejecuta cada vez que se presiona un boton del mouse sobre el
            'TreeProject'. Una vez invocado el metodo se chequea si el 
            boton presionado es el click derecho en cuyo caso se lanza el menu
            emergente('MenuProyect' o 'MenuMFile') asociado al 'TreeProject' en
            dependencia de quien sea el (los) item seleccionado.
        """
        flags = p_event.state
        model, paths = self.get_selection().get_selected_rows()

        if p_event.button == 3:
            if paths:            
                text = "\n".join([model[path][1] for path in paths])
                if not "." in text:
                    MenuProyect(p_event, self)
                else:                    
                    MenuMFile(p_event, self)
                    return True    
        
    def on_key_press_event(self, p_tree, p_event):
        """
            p_tree:  el 'GtkTreeView'.
            p_event: el evento que desencadeno la sennal.

            Retorna: 'True' si se presiono la tecla 'Enter'. Retornar
                     'True' detiene otros manejadores que se invocan para el 
                     evento.

            Metodo que es llamado cuando se presiona una tecla sobre el
            'arbol de proyecto'.            
            Delete: invoca el metodo 'self.delete_project()' o
            'self.delete_selection()' segun este activa la raiz del proyecto o
            una (o varias) rama(s).
            Enter, Space: invoca el metodo 'self.edit(p_item)'
        """        
        ascii = p_event.keyval
        flags = p_event.state
        
        model, paths = self.get_selection().get_selected_rows() 
  
        if paths:
            if ascii == 65535:  # delete            
                if paths[0] == (0, ):
                    self.delete_project()
                else:                    
                    self.delete_selection()

            elif ascii in (65293, 65421, 32):  # enter izq, enter der, space
                self.edit(paths)
                return True

    def on_row_activated(self, p_tree_view, p_path, p_col):
        """
            p_tree_view: el 'TreeView' que recibio la sennal.
            p_path: un camino de arbol que apunta a la fila activada.
            p_col: la columna en la fila activada.
			
            Se ejecuta cuando el usuario hace doble click o presiona la tecla
            'Enter' sobre alguna fila del TreeView del proyecto.            
        """        
        self.edit(p_path)
    
    def _load(self):
        """
            Metodo encargado de inicializar el arbol de proyecto con los datos 
            del mismo.
        """                
        self.__tree.clear()
        name = self.__project.get_name_project() + "   " + \
             self.__project.get_date_project()
        img = "new_project.png"
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(root, "images",
                                                                   img))
        self._parent_iter = self.__tree.append(None,[pixbuf, name])        
        
        img = "m_file.png"
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(root, "images",
                                                                   img))
        list_m_files = self.__project.get_m_file_list()
        for i in list_m_files:
            self.__tree.append(self._parent_iter, [pixbuf, i])    
        self.expand_to_path(self.__tree.get_path(self._parent_iter))
    
    def _delete_paths(self, p_list_of_path):
        """
            p_list_of_path: lista que contiene los caminos de las filas
                            que contienen los datos que queremos eliminar.

            Metodo que elimina, si es posible, los elementos pasados como 
            parametros desde el arbol de proyecto.            
        """
        model = self.__tree
        for i in xrange(len(p_list_of_path) - 1, -1, -1):
            path = p_list_of_path[i]
            iter_ = model.get_iter(path)
            text = model.get_value(iter_, 1)
            model.remove(iter_)
            self.__project.delete_m_file(text)

    def delete_selection(self):
        """
            Elimina todos los archivos m seleccionados, del arbol de proyecto.
            Adicionalmente elimina del proyecto los ficheros seleccionados.
        """
        paths = self.get_selection().get_selected_rows()[1]

        if paths:            
            msg = "All selected files will be deleted."
            resp = Confirm(gtk.STOCK_DIALOG_WARNING, msg,
                           "Project", self.__parent,
                           None).run()
            if not resp:
                return
            self._delete_paths(paths)
        
    def evaluate_selection(self):
        """
            Evalua los comandos seleccionados como si el usuario los ubiese
            entrado por teclado en la ventana de comandos.
        """
        model, paths = self.get_selection().get_selected_rows()
        
        if paths:            
            text = "\n".join([model[path][1] for path in paths])
            text = text.split(".")[0]
            self.__mwindow.get_cmdwindow().evaluate(text + "\n")
    
    def new_project(self):
        """
            Crea un nuevo proyecto.
        """
        if self.__project:
                if not self.confirm_close_project():
                    return        
        self.__dialog_create_project = Dialog_create_project(self, self.__parent)
        self.__dialog_create_project.show_()
        
    def open_project(self):
        """
            Metodo mediante el cual el usuario abre un proyecto existente 
            y carga los datos del mismo en el arbol de proyecto.
        """
        if self.__project:
                if not self.confirm_close_project(True):
                    return
        
        dialog = gtk.FileChooserDialog("Open..",
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                   gtk.STOCK_OPEN, gtk.RESPONSE_OK))        
        dialog.set_current_folder(os.environ["HOME"])
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter_ = gtk.FileFilter()
        filter_.set_name("EIDMAT project")
        filter_.add_mime_type("EIDMAT file/eidmat")
        filter_.add_pattern("*.eidmat")
        dialog.add_filter(filter_)
        
        filter_ = gtk.FileFilter()
        filter_.set_name("All files")
        filter_.add_pattern("*")
        dialog.add_filter(filter_)
        
        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            self.__project = Project()
            path = os.path.split(dialog.get_filename())[0]
            dialog.destroy()            
            self.__project.open_project(path)
            loc = self.__project.get_localization()
            self.__mwindow.get_cmdhistory().set_project(True, loc)
            loc = self.__project.get_localization()
            path = os.path.join(loc, "HIST",  
                                "hist.txt")
            f = open(path, "r")
            hist = f.read()
            f.close()
            path = os.path.join(loc, "HIST",
                                ".hist.txt~")
            f = open(path, "w")
            f.write(hist)
            f.close() 
            self._load()
            self.__mwindow.get_cmdhistory().clear_entire_history()
            self.__mwindow.create_project()
            self.__mwindow.get_cmdwindow().clear()
            path = self.__project.get_localization()
            m = os.path.abspath(os.path.join(path, "SRC"))
            self.__mwindow.get_connection().append_command(ManageCommandPro(
                "addpath (genpath ('%s'), '-begin');\n" %(m)))
            self.__mwindow.get_connection().append_command(ManageCommandPro(
                "clear all\n"))
            self.menu_project_create()
            path = os.path.join(self.__project.get_localization(), "VAR", 
                                "vars.var")            
            self.__mwindow.get_connection().append_command(LoadVars([], path))
        else:
            dialog.destroy()
        
    
    def save_project(self):
        """
            Metodo mediante el cual se guardan toda la informacion del
            proyecto.
        """
        if not self.__project:
            return
        self.__project.save_project()
        path = os.path.join(self.__project.get_localization(), "VAR", 
                            "vars.var")
        self.__mwindow.get_wspace().save(True, path)
        
    def save_as_project(self):
        """
            Metodo mediante el cual se realiza una copia del proyecto con 
            nombre y ubicacion diferentes.
        """
        if not self.__project:
            return
        dialog = gtk.FileChooserDialog("Open..",
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_SAVE,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                   gtk.STOCK_OK, gtk.RESPONSE_OK))
        dialog.set_current_folder(os.environ["HOME"])
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter_ = gtk.FileFilter()
        filter_.set_name("EIDMAT files")
        filter_.add_mime_type("EIDMAT file/m")
        filter_.add_pattern("*.m")
        dialog.add_filter(filter_)
        
        filter_ = gtk.FileFilter()
        filter_.set_name("All files")
        filter_.add_pattern("*")
        dialog.add_filter(filter_)
        
        response = dialog.run()
        if response == gtk.RESPONSE_OK:            
            path = self.__project.get_localization()
            m = os.path.join(path, "SRC")
            self.__mwindow.get_connection().append_command(ManageCommandPro(
            "rmpath (genpath ('%s'), '-begin');\n" %(m)))
            path = os.path.split(dialog.get_filename())[0]
            name = os.path.split(dialog.get_filename())[1]            
            self.__project.save_as_project(name, path)
            m = os.path.abspath(os.path.join(path, name, "SRC"))                       
            self.__mwindow.get_connection().append_command(ManageCommandPro(
            "addpath (genpath ('%s'), '-begin');\n" %(m)))
            self._load()
            self.save_project()
        dialog.destroy()
    
    def import_m_file(self):
        """
            Metodo mediante el cual se importar al proyecto un nuevo archivo m.
        """
        if not self.__project:
            return
        dialog = gtk.FileChooserDialog("Open..",
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                   gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_current_folder(os.environ["HOME"])
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter_ = gtk.FileFilter()
        filter_.set_name("EIDMAT files")
        filter_.add_mime_type("EIDMAT file/m")
        filter_.add_pattern("*.m")
        dialog.add_filter(filter_)
        
        filter_ = gtk.FileFilter()
        filter_.set_name("All files")
        filter_.add_pattern("*")
        dialog.add_filter(filter_)
        
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.__project.import_m_file(dialog.get_filename())
            self._load()
        dialog.destroy()
        
    def close_project(self, p_is_open = None):
        """
            Metodo mediante el cual se cierra un proyecto y se pasa a trabajar 
            en modo estandar (i.e. sin la existencia de un proyecto).
        """
        if not self.__project:
            return
        self.__mwindow.get_cmdhistory().set_project(False)
        self.__mwindow.get_cmdhistory().clear_entire_history()
        self.__mwindow.close_project()
        self.__mwindow.get_connection().append_command(ManageCommandPro(
                "clear all\n"))
        if not p_is_open:
            self.__mwindow.get_cmdwindow().clear()        
        self.__project = None
        self.menu_project_create()
        
    def create_directorio(self, p_name, p_dir):
        """
            p_name: cadena de texto que representa el nombre del proyecto.
            p_localization: cadena de texto que representa la ubicacion donde 
                            se alojara el directorio del proyecto (i.e. el 
                            directorio con nombre p_name).          
            
            Metodo mediante el cual se ordena la creacion de la estructura
            de directorios del proyecto en la ubicacion (p_dir + p_name).
        """
        self.__mwindow.get_connection().append_command(ManageCommandPro(
                                                                "clear all\n"))
        self.__project = Project()
        self.menu_project_create()
        path = os.path.join(p_dir, p_name)
        self.__project.new_project(p_name, path)
        self.__mwindow.create_project()        
        loc = self.__project.get_localization()
        self.__mwindow.get_cmdhistory().set_project(True, loc)
        self.__mwindow.get_cmdhistory().clear()
        self.__mwindow.get_cmdwindow().clear()
        self.save_project()
        m = os.path.abspath(os.path.join(path, "SRC"))
        self.__mwindow.get_connection().append_command(ManageCommandPro(
            "addpath (genpath ('%s'), '-begin');\n" %(m)))
        
    def confirm_close_project(self, p_is_open = None):
        """
            Metodo que lanza un mensaje de confirmacion preguntando si desea 
            realmente cerrar el proyecto. En caso de afirmacion se invoca el 
            metodo de cerrar el proyecto.            
        """
        msg = "Are you sure you want to close your project. Maybe you don't save ?"
        resp = Confirm(gtk.STOCK_DIALOG_QUESTION, msg, "Close Proyect",
                       self.__parent).run()
        if resp:
            path = self.__project.get_localization()
            m = os.path.join(path, "SRC")
            self.__mwindow.get_connection().append_command(ManageCommandPro(
             "rmpath (genpath ('%s'), '-begin');\n" %(m)))
            self.close_project(p_is_open)
            
        return resp    
    
    def delete_project(self):
        """
            Metodo mediante el cual se elimina fisicamente el proyecto en que 
            se trabaja.
        """
        if not self.__project:
            return
        msg = "Are you sure you want to delete this project?"
        resp = Confirm(gtk.STOCK_DIALOG_QUESTION, msg, "Close Proyect",
                       self.__parent).run()
        if resp:
            path = self.__project.get_localization()
            m = os.path.join(path, "SRC")
            
            self.__mwindow.get_connection().append_command(ManageCommandPro(
             "rmpath (genpath ('%s'), '-begin');\n" %(m)))
            
            self.__mwindow.get_connection().append_command(
             ManageCommandPro('OLD_VAL_recursive = confirm_recursive_rmdir(0);\n'))
            
            self.__mwindow.get_connection().append_command(
             ManageCommandPro('rmdir ("%s", "s");\n' %(path)))
            
            self.__mwindow.get_connection().append_command(
             ManageCommandPro('confirm_recursive_rmdir(OLD_VAL_recursive);\n'))
            
            self.__mwindow.get_connection().append_command(
             DeleteVar('OLD_VAL_recursive'))            
            
            self.close_project()
            
    def menu_project_create(self):
        """
            Metodo mediante el cual se controla la sensibilidad de los items 
            del menu proyecto. En este metodo se ponen sensitivos los items 
            referentes a las operaciones dentro de un proyecto cuando el 
            usuario crea o abre un proyecto y los desabilita cuando se cierra.
        """
        menu = self.__mwindow.get_project_menu()
        if self.__project:
            menu.get_save_item().set_sensitive(True)
            menu.get_save_as_item().set_sensitive(True)
            menu.get_delete_item().set_sensitive(True)
            menu.get_import_item().set_sensitive(True)
            menu.get_close_item().set_sensitive(True)
        else:
            menu.get_save_item().set_sensitive(False)
            menu.get_save_as_item().set_sensitive(False)
            menu.get_delete_item().set_sensitive(False)
            menu.get_import_item().set_sensitive(False)
            menu.get_close_item().set_sensitive(False)                    
                
    def edit(self, p_item):
        """
            Metodo mediante el cual se envia el archivo m seleccionado al  
            editor debugger para su edicion.
        """        
        model, paths = self.get_selection().get_selected_rows()
        
        if paths:
            for i in paths:
                if i != (0, ):
                    self.wakeup_editor(os.path.join(
                        self.__project.get_localization(), "SRC", model[i][1]))
        
    def wakeup_editor(self, p_path):
        """
            p_path: una cadena que es la direccion de uno o varios fichero a 
                    abrir.

            Invoca el metodo 'MainWindow.show_edebugger' con 'p_path' como 
            argumento.
        """
        self.__mwindow.show_edebugger(True, True, p_path)

    def activate(self):
        """
            Resalta el 'Project' en azul y muestra su barra de menu y de
            herramientas.
        """
        mwindow = self.__mwindow
        mnotebook = mwindow.get_mnotebook()
        my_page = mnotebook.page_num(self)

        if mnotebook.get_current_page() != my_page:
            mnotebook.set_current_page(my_page)

        mwindow.set_menu_bar(self.__mbar, self.__tbar, 2)
