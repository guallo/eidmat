import gtk
import gtk.glade
import os

from util.select_folder_dialog import SelectFolderDialog


class Dialog_create_project():
    """
        Clase que modela el componente visual para la creacion de un proyecto.
    """
    def __init__(self, p_tree_project, p_parente):
        """        
            Constructor de la clase Dialog_create_project.
        """
        self.__parent = p_parente
        self.__tree_project = p_tree_project
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

        self.__xml = gtk.glade.XML(os.path.join(root, "images", "gui.glade"),
                                   "dialog_create_project")
        self.__xml.signal_autoconnect(self)
        self.__window_create_project = \
            self.__xml.get_widget("dialog_create_project") 
        self.__name = self.__xml.get_widget("entry_name_project") 
        self.__dir = self.__xml.get_widget("entry_create_project_in") 
        self.__label_alredy_exist = self.__xml.get_widget("label_alredy_exist") 
        self.__button_create_project = \
            self.__xml.get_widget("button_create_project") 
        self.__button_create_project.set_sensitive(False) 
        self.__valid = False
   
    def show_(self):
        """
            Metodo mediante el cual se muestra la ventana de creacion de un 
            proyecto.
        """
        self.__dir.set_text(os.environ["HOME"])
        self.__window_create_project.show_all()
    
    def on_entry_name_project_changed(self, p_entry):
        """
            p_entry: representa un gtk.Entry.

            Metodo mediante el cual se chequea si ya existe una carpeta con el 
            nombre del proyecto y la ubicacion que el usuario asigna.
        """ 
        dir_text = self.__dir.get_text()
        if self.__name.get_text() != "":
            path = os.path.join(dir_text, self.__name.get_text())
            if os.access(path, os.F_OK):
                self.__valid = False                
                self.__label_alredy_exist.set_text("The project already exists")
            elif not os.access(dir_text, os.F_OK):
                self.__valid = False                
                self.__label_alredy_exist.set_text("The path: " + "'" + \
                    dir_text + "'" + " does not exist.")
            else:                    
                self.__valid = True                
                self.__label_alredy_exist.set_text("")
        else:            
            if not os.access(dir_text, os.F_OK):
                self.__valid = False                
                self.__label_alredy_exist.set_text("The path: " + "'" + \
                    dir_text + "'" + " does not exist.")
                    
        if self.__valid:
            self.__button_create_project.set_sensitive(True)    
        else:
            self.__button_create_project.set_sensitive(False)      
         
    def on_entry_create_project_in_changed(self, p_entry):
        """
            p_entry: representa un gtk.Entry.
            
            Metodo mediante el cual se chequea si existe una carpeta en la
            ubicacion que el usuario selecciona.
        """
        dir_text = self.__dir.get_text()
        name_text = self.__name.get_text()
        if self.__dir.get_text() != "":
            if not os.access(dir_text, os.F_OK):
                self.__valid = False                
                self.__label_alredy_exist.set_text("The path: " + "'" + \
                    dir_text + "'" + " does not exist.")
            else:
                self.__valid = True                
                self.__label_alredy_exist.set_text("")
                if name_text != "":
                    path = os.path.join(dir_text, name_text)
                        
                    if os.access(path, os.F_OK):
                        self.__valid = False                        
                        self.__label_alredy_exist.set_text(
                            "The project already exists")
                    else:
                        self.__label_alredy_exist.set_text("")
                else:
                    self.__label_alredy_exist.set_text("")
        else:
            self.__valid = False
        
        if name_text == "":
            self.__valid = False                
            
        if self.__valid:
            self.__button_create_project.set_sensitive(True)    
        else:
            self.__button_create_project.set_sensitive(False)  
            
    def on_button_create_project_activate(self, *pw):    
        """
            pw: representa una lista de parametros en dependencia de que 
            metodo llame a este. En ocaciones contiene un GtkEntry y un 
            GdkEvent mientras que en otras un GtkButton.
            
            Metodo mediante el cual se ordena la creacion de un nuevo proyecto.
        """
        if len(pw) > 1:            
            if pw[1].keyval == gtk.keysyms.Return or \
               pw[1].keyval == gtk.keysyms.KP_Enter:
                if self.__valid:
                    self.__tree_project.create_directorio(
                        self.__name.get_text(),  self.__dir.get_text())
                    self.__window_create_project.destroy()
                    self.__tree_project._load()
                                        
        else:
            self.__tree_project.create_directorio(self.__name.get_text(), 
                                                         self.__dir.get_text())
            self.__window_create_project.destroy()
            self.__tree_project._load()       
        
    
    def on_button_cancel_ne_project_activate(self, p_button):
        """
            p_button: representa un GtkButton.
            
            Cancela la creacion del proyecto.
        """        
        self.__window_create_project.destroy()
        
    def on_button_browser_project_activate(self, p_button):
        """
            p_button: representa un GtkButton.
            
            Visualiza un dialogo para la seleccion del directorio donde se
            desea crear el proyecto.
        """        
        path = SelectFolderDialog("Choose a directory", self.__parent, \
                                self.__dir.get_text()).run()
        if path:
            self.__dir.set_text(path)
                
        
