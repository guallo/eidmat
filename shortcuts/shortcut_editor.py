import os
import sys
import gtk
import gtk.glade
import gtk.gdk

from shortcuts.help_create_new_shortcut import HelpCreateNewShortcut
from util.message import Message

class ShortcutEditor():
    """
        Clase que modela el trabajo con la ventana de edicion de shortcuts. 
        Esta ventana puede adicionar un nuevo shortcut o modificar los valores 
        de uno existente.
    """    
    def __init__(self, p_container_shorcuts):
        """
            p_container_shorcuts: representa una instancia de ShortcutToolBar.
            
            Constructor de la clase ShortcutEditor.
        """
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        self.__path = os.path.join(root, "images", "gui.glade")      
        self.__visible = False
        self.__container_shorcuts = p_container_shorcuts        
        self.__help_create_new_shortcut = HelpCreateNewShortcut(self.__path)

    def ini_(self):
        """
            Metodo para crear una nueva ventana cada vez que se instancia el 
            metodo show_.
        """
        self.__xml = gtk.glade.XML(self.__path, "shortcut_editor")
        self.__xml.signal_autoconnect(self)
        self.__shortcut_editor = self.__xml.get_widget("shortcut_editor")
        self.__label = self.__xml.get_widget("shortcut_label")
        self.__text_v = self.__xml.get_widget("shortcut_callback")

        self.__dialog = self.__xml.get_widget("hbox888")
        liststore = gtk.ListStore(gtk.gdk.Pixbuf, str)            
        self.__combo_ico = gtk.ComboBox(liststore)            
        cell = gtk.CellRendererPixbuf() 
        cell2 = gtk.CellRendererText()
        self.__combo_ico.pack_start(cell, False)
        self.__combo_ico.pack_start(cell2, False)
        self.__combo_ico.add_attribute(cell, "pixbuf", 0)
        self.__combo_ico.add_attribute(cell2, "text", 1)
        dire = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]),\
                            "images")
        pixbux = gtk.gdk.pixbuf_new_from_file(os.path.join(dire, 
                                                           "shortcut.png"))
        liststore.append([pixbux, " Standard icon"])
        pixbux = gtk.gdk.pixbuf_new_from_file(os.path.join(dire, "icon_1.png"))
        liststore.append([pixbux, "Extern connection icon"])
        pixbux = gtk.gdk.pixbuf_new_from_file(os.path.join(dire, "icon_2.png"))
        liststore.append([pixbux, "Script icon"])
        pixbux = gtk.gdk.pixbuf_new_from_file(os.path.join(dire, 
                                                           "icon_3.png"))
        liststore.append([pixbux, "Function icon"])
        self.__dialog.pack_start(self.__combo_ico)
        self.__dialog.set_child_packing(self.__combo_ico, True, True, 0, 
                                        gtk.PACK_START)        
        self.__combo_ico.set_active(0)

        # variable que decide si se esta modificando un shortcut existente        
        self.__shortcut_edit = False

    def set_edit_shortcut(self):
        """
            Metodo que precisa si la ventana se va a utilizar para modificar un 
            shortcut existente.
        """
        self.__shortcut_edit = True

    def show_(self):
        """
            Metodo que invoca la creacion y visualizacion de la ventana de
            edicion de shortcuts.
        """
        self.ini_()
        self.__shortcut_editor.show_all()
        self.__visible = True

    def hide_(self):
        """
            Metodo que controla el estado (visible o no) de la ventana 
            <shortcut editor>.
        """
        self.__visible = False        

    def is_show(self):
        """
            Retorna: True o False.

            Metodo que verifica el estado (visible o no) de la ventana 
            <shortcut editor>.
        """
        return self.__visible

    def on_button3_activate(self, p_widget):  
        """
            p_widget: representa una instancia de GtkButton.
            
            Metodo que muestra la ayuda correspondiente a la ventana 
            <shortcut editor>.
        """
        if not self.__help_create_new_shortcut.is_show():
            self.__help_create_new_shortcut.view_help_create_new_shortcut()
        else:
            self.__help_create_new_shortcut.present()

    def on_button1_activate(self, p_widget):
        """
            p_widget: representa una instancia de GtkButton.
            
            Metodo que se invoca tras hacer click sobre en el boton <save> 
            en la ventana <shortcut editor>. En el se comprueba si la solicitud
            se refiere a adicionar un nuevo shortcut o editar uno existente.
            Tambien se muestran errores asociados a las anteriores acciones.
        """
        label = self.__label.get_text()
        i, e = self.__text_v.get_buffer().get_bounds()
        callback = self.__text_v.get_buffer().get_text(i, e)        
        ver = False
        if callback =="" or label == "":
            Message(gtk.STOCK_DIALOG_ERROR, "There are empty fields", "Sorry",
                    self.__shortcut_editor).run()
        else:
            if not self.__shortcut_edit:
                ver = self.__container_shorcuts.verify_create_chortcut(label)

                if not ver:
                    Message(gtk.STOCK_DIALOG_ERROR, "A Shortcut already \
exist with this label Please \nprovide a different label for this Shortcut",
                                         "Sorry", self.__shortcut_editor).run()                
                else:
                    self.__container_shorcuts.create_chortcut(label, callback,
                                                 self.__combo_ico.get_active())
                    self.__shortcut_editor.destroy()
                    self.__shortcut_editor = None                    
            else:
                self.__shortcut_edit = False                
                ver = self.__container_shorcuts.modify_chortcut(
                    self.__edit_shortcut, label,
                    callback, self.__combo_ico.get_active())
                if not ver:
                    self.__shortcut_edit = True
                    Message(gtk.STOCK_DIALOG_ERROR, "A Shortcut already \
exist with this label Please \nprovide a different label for this Shortcut",
                                         "Sorry", self.__shortcut_editor).run()
                else:
                    self.__shortcut_editor.destroy()
                    self.__shortcut_editor = None                    

    def edit_shortcut(self, p_label, p_callback, p_ico):
        """"
            p_label: representa una cadena de texto.
            p_callback: representa una cadena de texto.
            p_ico: representa un valor entero.
            
            Metodo que precisa si la ventana se va a utilizar para editar un 
            shortcut existente.
        """
        self.show_()
        self.__edit_shortcut = p_label
        self.set_edit_shortcut()
        self.__label.set_text(p_label)
        self.__text_v.get_buffer().set_text(p_callback)
        self.__pos_ico = p_ico
        self.__combo_ico.set_active(p_ico)

    def on_button2_activate(self, p_widget):
        """
            p_widget: representa una instancia de GtkButton.
            
            Metodo que se invoca tras hacer click sobre en el boton <cancel> 
            en la ventana <shortcut editor>.
        """
        self.hide_()
        p_widget.get_parent_window().destroy()

    def on_shortcut_editor_destroy(self, p_widget):
        """
            p_widget: representa una instancia de GtkDialog.            
            
            Metodo que oculta la ventana <shortcut editor> tras cerrar la misma
            desde los controles propios de la ventana.
        """
        self.hide_()

    def present(self):
        """
            Metodo que trae al frente la ventana <shortcut editor>.
        """
        self.__shortcut_editor.present()    
