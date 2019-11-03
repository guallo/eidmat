import os
import gobject
import gtk
import gtk.glade
import pango
import gtk.gdk
import sys

from shortcuts.shortcut_editor import ShortcutEditor
from shortcuts.organize_shortcut import OrganizeShortcut
from shortcuts.help_create_new_shortcut import HelpCreateNewShortcut


class PopupMenu():
    """
        Representa el menu emergente al dar clic derecho en la barra de 
        shortcuts o en la barra de herramientas o en la barra de menu de la 
        aplicacion.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: representa el MainWindow.

            Constructor de la clase PopupMenu.
        """ 
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        path = os.path.join(root, "images", "gui.glade")

        self.__xml = gtk.glade.XML(path, "menu_shortcut")
        self.__menu_shortcut = self.__xml.get_widget("menu_shortcut")        
        self.__shortcuts_toolbar = None

        self.__mwindow = p_mwindow
        self.__shortcut_edit = False
        self.__menu_toolbar = None
        self.__xml.signal_autoconnect(self)
        elem = gtk.SeparatorMenuItem()
        elem.show_all()
        self.__menu_shortcut.append(elem)
        self.__menu_shortcut.reorder_child(elem, 2) 
        elem = gtk.SeparatorMenuItem()
        elem.show_all()
        self.__menu_shortcut.append(elem)
        self.__menu_shortcut.reorder_child(elem, 6)

    def set_shortcuts_toolbar(self, p_toolbar):
        """
            p_toolbar: representa una instancia de la clase ShortcutToolBar.

            Metodo que permite tener una referencia de la barra de shortcuts.
        """
        self.__shortcuts_toolbar = p_toolbar

    def on_delete_activate(self, p_window):
        """
            p_window: representa un GtkImageMenuItem.

            Metodo que permite la eliminacion de un shortcut tras hacer click 
            en el item <Delete>.
        """
        self.__mwindow.get_shortcuts_toolbar().delete_shortcut()

    def on_toolbar_toggled(self, p_window):
        """
            p_window: representa un GtkCheckMenuItem.
            
            Metodo encargado de la visualizacion y ocultacion de la barra de 
            shortcuts o la barra de herramientas en correspondencia con el 
            parametro de entrada.
        """
        toolbar = self.__shortcuts_toolbar
        name = p_window.get_name()
        if name == "toolbar":
            if p_window.get_active():
                self.__mwindow.get_widget("hbox8").show()
            else:            
                self.__mwindow.get_widget("hbox8").hide()
        elif name == "shortcuts_toolbar":
            if p_window.get_active():
                toolbar.show()
            else:            
                toolbar.hide()
        elif name == "show_labels":
            if p_window.get_active():                               
                toolbar.show_labels()
                toolbar.set_visible_shortcut(True)
            else:
                toolbar.hide_labels() 
                toolbar.set_visible_shortcut(False)

    def on_new_shortcut_activate(self, p_window):
        """
            p_window: representa un GtkImageMenuItem.

            Metodo que visualiza la ventana <shortcut editor> para la adiccion
            de un nuevo shortcut. 
        """
        self.__mwindow.get_shortcuts_toolbar().on_new_shortcut_activate()

    def on_organize_shortcuts_activate(self, p_window):
        """
            p_window: representa un GtkImageMenuItem.

            Metodo que visualiza la ventana <shortcuts organizer>.
        """
        self.__mwindow.get_shortcuts_toolbar().on_organize_shortcuts_activate(
                                                                      p_window)

    def on_edit_activate(self, p_window):
        """
            p_window: representa un GtkImageMenuItem.

            Metodo que visualiza la ventana <shortcut editor> para la edicion
            de un nuevo shortcut. 
        """
        self.__mwindow.get_shortcuts_toolbar().on_edit_activate(p_window)

    def _popup(self, p_event):
        """
            p_event: reopresenta un GdkEvent.
            
            Metodo que visualiza un menu emergente al hacer click derecho 
            sobre algun shortcut.
        """
        if p_event.button == 3: # Click derecho	    
            self.__menu_shortcut.show_all()
            self.__menu_shortcut.popup(None, None, None, 3, p_event.time)

    def _popup2(self, p_event):
        """
            p_event: reopresenta un GdkEvent.
            
            Metodo que visualiza un menu emergente al hacer click derecho 
            sobre la barra de shortcuts.
        """
        if p_event.button == 3: # Click derecho
            self.__menu_shortcut.show_all()
            self.__menu_shortcut.get_children()[0].hide()
            self.__menu_shortcut.get_children()[1].hide()
            self.__menu_shortcut.get_children()[2].hide()
            if not self.__mwindow.get_shortcuts_toolbar().get_children()[1:]:
                self.__menu_shortcut.get_children()[3].hide()
                self.__menu_shortcut.get_children()[5].hide()
            self.__menu_shortcut.popup(None, None, None, 3, p_event.time)

    def popup3(self, p_event):
        """
            p_event: reopresenta un GdkEvent.
            
            Metodo que visualiza un menu emergente al hacer click derecho 
            sobre la barra de menu o la barra de accesos rapidos.
        """
        for item in self.__menu_shortcut.get_children()[: 7]:
            item.hide()
        self.__menu_shortcut.popup(None, None, None, 3, p_event.time)

    def set_active(self):
        """
            Metodo mediante el cual se desactiva el item <show_labels> del 
            menu emergente al cual hace referencia la clase <PopupMenu>.        
        """
        self.__xml.get_widget("show_labels").set_active(False)
