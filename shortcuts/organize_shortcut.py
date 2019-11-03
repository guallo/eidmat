import os
import sys
import gtk
import gtk.glade
import pango
import gtk.gdk

from util.confirm import Confirm
from shortcuts.help_create_new_shortcut import HelpCreateNewShortcut


class OrganizeShortcut():
    """
        Clase que modela el trabajo con la ventana <shortcuts organizer>.
    """
    def __init__(self, p_container_shorcuts):
        """
            p_container_shorcuts: representa una instancia de ShortcutToolBar.
            
            Constructor de la clase OrganizeShortcut.
        """
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        self.__path = os.path.join(root, "images", "gui.glade")
        self.__visible = False
        self.__container_shorcuts = p_container_shorcuts
        self.__help = HelpCreateNewShortcut(self.__path)
        self.__confirmed_del = False

    def ini_(self):
        """
            Metodo para crear una nueva ventana cada vez que se instancia el 
            metodo show_.
        """
        xmlaux = gtk.glade.XML(self.__path, "organize_shortcut")
        xmlaux.signal_autoconnect(self)
        self.__organize_shortcut = xmlaux.get_widget("organize_shortcut")
        self.__treeview_shorcuts = xmlaux.get_widget("treeview_shorcuts")   
        self.__liststore_shorcuts = gtk.ListStore(gtk.gdk.Pixbuf, str)
        self.__treeview_shorcuts.set_model(self.__liststore_shorcuts)
        column = gtk.TreeViewColumn("Shortcuts")
        cell2 = gtk.CellRendererPixbuf()   
        column.pack_start(cell2, False)
        cell = gtk.CellRendererText()
        column.pack_start(cell, False)         
        column.add_attribute(cell2, "pixbuf", 0)                        
        column.add_attribute(cell, "text", 1)
        self.__lista_icos = ["shortcut.png", "icon_1.png", "icon_2.png", \
                            "icon_3.png"]
        self.__dire = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]),\
                                   "images")
        pixbux = gtk.gdk.pixbuf_new_from_file(os.path.join(self.__dire, 
                                                           "shortcut.png"))
        self.__treeview_shorcuts.append_column(column)
        self.w_listore()

    def w_listore(self):
        """
            Metodo que adiciona los elementos del liststore al treeview.
        """        
        labels = []
        labels, icons = self.__container_shorcuts.get_labels_icos()
        self.__liststore_shorcuts.clear()
        for aa in range(len(labels)):
            icon = self.__lista_icos[icons[aa]]
            pixbux = gtk.gdk.pixbuf_new_from_file(os.path.join(self.__dire, 
                                                               icon))            
            self.__liststore_shorcuts.append([pixbux, labels[aa]])

    def hide_(self):
        """
            Metodo que controla el estado (visible o no) de la ventana 
            <shortcuts organizer>.
        """
        self.__visible = False

    def is_show(self):
        """
            Retorna: True o False
            
            Metodo que verifica el estado (visible o no) de la ventana 
            <shortcuts organizer>.
        """
        return self.__visible

    def show_(self):
        """
            Metodo que invoca la creacion y visualizacion de la ventana 
            <shortcuts organizer>.
        """
        self.ini_()
        self.__organize_shortcut.show_all()
        self.__visible = True
        self.__confirmed_del = False

    def on_move_up_shortcut_activate(self, p_widget):
        """
            p_widget: representa una instancia de GtkButton.

            Metodo que invoca a metodo auxiliar <move_shortcut> de la clase
            <ShortcutToolBar> y permite trasladar hacia a la derecha o 
            izquierda un shortcut dentro de la barra.
        """
        selection = self.__treeview_shorcuts.get_selection()
        model, aux_iter, = selection.get_selected()
        if aux_iter:
            path = model.get_path(aux_iter)
            row = path[0]
            prev = self.__liststore_shorcuts.get_iter_first()
            a_row = 0
            while row-1 > a_row:
                path = model.get_path(prev)
                a_row = a_row+1
                prev  = self.__liststore_shorcuts.iter_next(prev)
            if aux_iter:
                text = model.get_value(aux_iter, 1)
                aux_hbox = self.__container_shorcuts
                if p_widget.get_name() == "move_up_shortcut":
                    if row > 0:
                        self.__liststore_shorcuts.move_before(aux_iter, prev)
                        self.__container_shorcuts.move_shortcut(row , row - 1)
                else:
                    if row < len(self.__liststore_shorcuts) -1:
                        it = self.__liststore_shorcuts.iter_next(aux_iter)
                        self.__liststore_shorcuts.move_after(aux_iter, it)
                        self.__container_shorcuts.move_shortcut(row, row + 1)

    def on_button4_activate(self, p_widget):
        """
            p_widget: representa una instancia de GtkButton.

            Metodo que invoca la ventana de edicion de shortcut.
        """
        self.__container_shorcuts.set_organize_list_store()
        self.__container_shorcuts.on_new_shortcut_activate()

    def on_button6_activate(self, p_widget):
        """
            p_widget: representa una instancia de GtkButton.

            Metodo que invoca la ventana de edicion de shortcut.
        """
        selection = self.__treeview_shorcuts.get_selection()   
        model, iter_, = selection.get_selected()        
        if iter_:
            text = model.get_value(iter_, 1)   
            self.__container_shorcuts.set_organize_list_store()
            self.__container_shorcuts.edit_shorcut_organize(text)

    def on_button10_activate(self, p_widget):        
        """
            p_widget: representa una instancia de GtkButton.

            Metodo que permite la eliminacion de un shortcut seleccionado.
        """               
        selection = self.__treeview_shorcuts.get_selection()   
        model, iter_, = selection.get_selected()         
        if iter_:
            if not self.__confirmed_del:
                msg = "Are you sure you want to delete the selected variable?"
                resp = Confirm(gtk.STOCK_DIALOG_QUESTION, msg, 
                               "Confirm delete", self.__organize_shortcut,
                               "Do not show this prompt again.").run()
                if resp:                
                    self.__confirmed_del = resp[0] 
                if not resp:
                    return
            text = model.get_value(iter_, 1) 
            path = model.get_path(iter_)
            row = path[0]
            self.__container_shorcuts.set__edit_shortcut(
                self.__container_shorcuts.get_children()[row + 1])
            self.__container_shorcuts.delete_shortcut()
            self.__liststore_shorcuts.remove(iter_)

    def on_button8_activate(self, p_widget):
        """
            p_widget: representa una instancia de GtkButton.

            Metodo que visualiza la ayuda asociada al <shortcuts organizer>.
        """
        self.__help.view_help_organize_new_shortcut()

    def on_button7_activate(self, p_widget):
        """
            p_widget: representa una instancia de GtkButton.
            
            Metodo que tras el cierre de la ventana <shortcuts organizer> 
            destruye todos los componentes asociados.
        """
        self.hide_()
        if p_widget.get_parent_window():
            p_widget.get_parent_window().destroy()

    def present(self):
        """
            Metodo que trae al frente la ventana <shortcut editor>.
        """
        self.__organize_shortcut.present()
