import os
import gobject
import gtk
import gtk.glade
import pango
import gtk.gdk

class HelpCreateNewShortcut():
    """
        Clase que muestra la ayuda correspondientes a las ventanas 
        <shortcuts organizer> y <shortcuts editor> respectivamente.
    """    
    def __init__(self, p_path):
        """
            p_path: direccion del xml del glade

            Constructor de la clase HelpCreateNewShortcut.
        """
        self.__path = p_path
        self.__visible = False

    def ini_(self):
        """
            Metodo que crea y visualiza una nueva ventana cada vez que se 
            instancia el metodo show_.
        """
        self.__xml4 = gtk.glade.XML(self.__path, "shortcut_editor_help")
        self.__xml4.signal_autoconnect(self)        
        self.__shortcut_editor_help = self.__xml4.get_widget(\
            "shortcut_editor_help")    
        self.__textview1 = self.__xml4.get_widget("textview_help_shortcuts")
        self.__textview1.set_editable(False)
        self.create_tags()

    def show_(self):
        """
            Metodo para mostrar visible la ventana.
        """
        self.__shortcut_editor_help.show_all()
        self.__visible = True

    def hide_(self):
        """
            Metodo que controla el estado (visible o no) de la ventana.
        """
        self.__visible = False

    def is_show(self):
        """
            Retorna: True o False

            Metodo que verifica el estado (visible o no) de la ventana de
            ayuda.
        """
        return self.__visible   

    def view_help_create_new_shortcut(self):
        """
            Retorna: False si ya la ventana esta visible y en ese caso la 
                     pone a la vista del usuario.

            Metodo que visualiza el texto de la ayuda correspondiente al 
            trabajo con la ventana <shortcut editor>.
        """
        if self.__visible:
            self.__shortcut_editor_help.present()
            return False
        self.ini_()
        self.show_()
        self.__textview1.get_buffer().set_text("\
\n  Shortcut Editor \n  When creating a new shortcut, provide \
values for\n  the fields listed below. When editing an existing\n  \
shortcut, make changes to these values. When\n  adding a Help browser \
favorite, you can accept\n  all the defaults and just click Save, or \
you can\n  make changes.\n\n  Label\n  Provide a name for the shortcut.\n\n  \
Callback\n  Enter the Octave statements that execute when\n  you run the \
shortcut. You can type them in, copy\n  and paste them.\n\n  If you copy the \
statements from the Command\n  Window, prompts (>>) appear in the shortcut, \
but\n  Octave removes the prompts when you save the\n  shortcut.")        
        start, end = self.__textview1.get_buffer().get_bounds()
        self.__textview1.get_buffer().apply_tag_by_name("bold",
                                                        start, end)       
        res = start.forward_search("Shortcut Editor", 
                                    gtk.TEXT_SEARCH_TEXT_ONLY)
        matchStart, matchEnd = res
        self.__textview1.get_buffer().apply_tag_by_name("red_foreground",
                                                        matchStart, matchEnd)
        res = start.forward_search("Label", gtk.TEXT_SEARCH_TEXT_ONLY)
        matchStart, matchEnd = res
        self.__textview1.get_buffer().apply_tag_by_name("red_foreground",
                                                        matchStart, matchEnd)
        res = start.forward_search("Callback", gtk.TEXT_SEARCH_TEXT_ONLY)
        matchStart, matchEnd = res
        self.__textview1.get_buffer().apply_tag_by_name("red_foreground",
                                                        matchStart, matchEnd)
        res = start.forward_search("Save", gtk.TEXT_SEARCH_TEXT_ONLY)
        matchStart, matchEnd = res
        self.__textview1.get_buffer().apply_tag_by_name("blue_foreground",
                                                        matchStart, matchEnd)

    def view_help_organize_new_shortcut(self): 
        """
            Retorna: False si ya la ventana esta visible y en ese caso la 
                     pone a la vista del usuario. 
        
            Metodo que visualiza el texto de la ayuda correspondiente al 
            trabajo con la ventana <shortcuts organizer>.
        """
        if self.__visible:
            self.present()
            return False
        self.ini_()
        self.show_()
        self.__textview1.get_buffer().set_text("\
\n  Shortcuts Organizer \n\n  New Shortcut\n  Displays the Shortcut Editor \
dialog box for you to\n  create a new shortcut. Click Help in that dialog\n \
 box for details.\n\n  Edit Shortcut\n  Displays the Shortcut Editor dialog \
box for the\n  selected shortcut. Make changes to any field and\n  click \
Save.\n\n  Delete Shortcut\n  Deletes the selected shortcut, displays a\n  \
confirmation dialog.")        
        start, end = self.__textview1.get_buffer().get_bounds()
        self.__textview1.get_buffer().apply_tag_by_name("bold",
                                                        start, end)       
        res = start.forward_search("Shortcuts Organizer", 
                                   gtk.TEXT_SEARCH_TEXT_ONLY)
        matchStart, matchEnd = res
        self.__textview1.get_buffer().apply_tag_by_name("red_foreground",
                                                        matchStart, matchEnd)
        res = start.forward_search("New Shortcut", gtk.TEXT_SEARCH_TEXT_ONLY)
        matchStart, matchEnd = res
        self.__textview1.get_buffer().apply_tag_by_name("red_foreground",
                                                        matchStart, matchEnd)
        res = start.forward_search("Edit Shortcut", gtk.TEXT_SEARCH_TEXT_ONLY)
        matchStart, matchEnd = res
        self.__textview1.get_buffer().apply_tag_by_name("red_foreground",
                                                        matchStart, matchEnd)
        res = start.forward_search("Delete Shortcut", 
                                    gtk.TEXT_SEARCH_TEXT_ONLY)
        matchStart, matchEnd = res
        self.__textview1.get_buffer().apply_tag_by_name("red_foreground",
                                                        matchStart, matchEnd)
        res = start.forward_search("Shortcut Editor", 
                                    gtk.TEXT_SEARCH_TEXT_ONLY)
        matchStart, matchEnd = res
        self.__textview1.get_buffer().apply_tag_by_name("blue_foreground",
                                                        matchStart, matchEnd)   
        res = start.forward_search("Help", gtk.TEXT_SEARCH_TEXT_ONLY)
        matchStart, matchEnd = res
        self.__textview1.get_buffer().apply_tag_by_name("blue_foreground",
                                                        matchStart, matchEnd) 
        res = start.forward_search("Save", gtk.TEXT_SEARCH_TEXT_ONLY)
        matchStart, matchEnd = res
        self.__textview1.get_buffer().apply_tag_by_name("blue_foreground",
                                                        matchStart, matchEnd)

    def on_shortcut_editor_help_destroy(self, p_widget):
        """
            p_widget: representa una instancia de GtkWindow.
            
            Metodo que indica la ocultacion de la ventana de ayuda.
        """
        self.hide_()

    def create_tags(self):
        """
            Metodo que genera los tags en el textview dandole colores y estilo 
            a las frases de encabezamiento y palabras claves.
        """
        color = gtk.gdk.color_parse("blue")
        self.__textview1.get_buffer().create_tag("blue_foreground", 
                                                 foreground_gdk = color)
        color = gtk.gdk.color_parse("red")
        self.__textview1.get_buffer().create_tag("red_foreground", 
                                                 foreground_gdk = color)        
        self.__textview1.get_buffer().create_tag("bold",
                                                 weight = pango.WEIGHT_BOLD)

    def present(self):
        """
            Metodo que trae al frente la ventana de ayuda.
        """
        self.__shortcut_editor_help.present() 
