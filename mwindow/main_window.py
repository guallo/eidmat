import os
import gtk.glade

from mwindow.combo_of_directories import ComboOfDirectories
from conn.connection import Connection
from cmdhistory.command_history import CommandHistory
from cmdwindow.command_window import CommandWindow
from cdirectory.current_directory import CurrentDirectory
from wspace.workspace import Workspace
from help.gui.help_window import HelpWindow
from toolbar.context_toolbar import ContextToolbar
from mwindow.popup_menu import PopupMenu
from shortcuts.shortcut_toolbar import ShortcutToolBar
from mwindow.menu_start import MenuStart


class MainWindow:
    """
        Clase que representa la ventana principal de la aplicacion.
    """
    def __init__(self):
        """
            Retorna: un nuevo 'MainWindow'.

            Crea un nuevo 'MainWindow'.
        """
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

        self.__xml = gtk.glade.XML(os.path.join(root, "images", "gui.glade"),
                                   "window1")
        self.__xml.signal_autoconnect(self)
        self.__window = self.get_widget("window1")
        self.__window.connect("delete-event", lambda p_win, p_event:
                                                     self.close())

        # Creacion de la 'Connection'.
        self.__conn = Connection(self)

        # Creacion del 'Combo of directories'.
        self.__combo = ComboOfDirectories(self)

        # Creacion del boton para subir al directorio padre.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "go_up.png"))
        self.__butt_up = gtk.ToolButton(img)
        self.__butt_up.set_tooltip_text("Go up one level")
        self.__butt_up.connect("clicked", self.on_button_up_clicked)

        # Creacion del 'Command history'.
        self.__cmdhistory = CommandHistory(self, self.__window)
        self.get_widget("scrolledwindow1").add(self.__cmdhistory)

        # Creacion del 'Command window'.
        self.__command_win = CommandWindow(self, self.__window, self.__conn,
                                           self.__cmdhistory)
        self.get_widget("scrolledwindow4").add(self.__command_win)

        # Creacion de 'Current directory'.
        self.__cdirectory = CurrentDirectory(self, self.__window, self.__conn,
                                             self.__combo, self.__butt_up)

        # Creacion del 'Workspace'.
        self.__wspace = Workspace(self, self.__conn, self.__cdirectory,
                                  self.__window)

        # Creacion del 'Main notebook'.
        mnotebook = gtk.Notebook()
        mnotebook.set_tab_pos(gtk.POS_BOTTOM)
        self.get_widget("alignment3").add(mnotebook)
        mnotebook.connect("switch-page", self.on_mnotebook_switch_page)
        mnotebook.connect("focus-in-event", self.on_mnotebook_focus_in_event)
        mnotebook.append_page(self.__cdirectory,
                              gtk.Label("Current Directory"))
        mnotebook.append_page(self.__wspace, gtk.Label("Workspace"))
        self.__mnotebook = mnotebook

        # Creacion del menu emergente.
        self.__popup_menu = PopupMenu(self)

        # Creacion de la barra de shortcuts.
        self.__shortcuts_toolbar = ShortcutToolBar(self)
        self.get_widget("hbox3").add(self.__shortcuts_toolbar)

        # Creacion del Menu Inicio.
        self.__start_menu = MenuStart(self)

        self.__conn.start()
        self.__window.show_all()
        self.__command_win.activate()
        self.__help = None

    def get_connection(self):
        """
            Retorna: un 'Connection'.

            Retorna la conexion con 'Octave'.
        """
        return self.__conn

    def get_combo(self):
        """
            Retorna: un 'ComboOfDirectories'.

            Retorna el combo de directorios de la aplicacion.
        """
        return self.__combo

    def get_butt_up(self):
        """
            Retorna: un 'gtk.ToolButton'.

            Retorna el boton de subir al directorio padre.
        """
        return self.__butt_up

    def get_mnotebook(self):
        """
            Retorna: un 'gtk.Notebook'.

            Retorna el notebook principal de la aplicacion, en el cual estan
            empotrados el 'CurrentDirectory' y el 'Workspace'.
        """
        return self.__mnotebook

    def get_popup_menu(self):
        """
            Retorna: un 'PopupMenu'.

            Retorna el menu emergente que sale al dar click derecho en la
            barra de accesos directos('ShortcutToolBar') o en la barra de
            herramientas('ContextToolbar') o en la barra de menus
            ('ContextMenuBar') de la aplicacion.
        """
        return self.__popup_menu

    def get_shortcuts_toolbar(self):
        """
            Retorna: un 'ShortcutToolBar'.

            Retorna la barra de accesos directos.
        """
        return self.__shortcuts_toolbar

    def get_cmdwindow(self):
        """
            Retorna: un 'CommandWindow'.

            Retorna la ventana de comandos.
        """
        return self.__command_win

    def get_cmdhistory(self):
        """
            Retorna: un 'CommandHistory'.

            Retorna el historial de comandos.
        """
        return self.__cmdhistory

    def get_cdirectory(self):
        """
            Retorna: un 'CurrentDirectory'.

            Retorna el componente que representa el directorio actual del
            usuario, en el cual se muestran todos los archivos del mismo.
        """
        return self.__cdirectory

    def get_wspace(self):
        """
            Retorna: un 'Workspace'.

            Retorna el componente que representa el espacio de trabajo del
            usuario, en el cual se registran todas las variables definidas.
        """
        return self.__wspace

    def get_window(self):
        """
            Retorna: un 'gtk.Window'.

            Retorna la ventana principal de la aplicacion.
        """
        return self.__window

    def get_widget(self, p_name):
        """
            p_name: una cadena que representa el nombre de un elemento
                    disennado en Glade.

            Retorna: un 'gtk.Widget'.

            Retorna el elemento llamado 'p_name' que se encuentra en el
            archivo '*.glade' correspondiente a la ventana principal.
        """
        return self.__xml.get_widget(p_name)

    def get_toolbar(self):
        """
            Retorna: un 'ContextToolbar'(barra de herramientas principal),
                     o 'None' si no hay ninguna todavia.

            Retorna la barra de herramientas principal de la aplicacion,
            o 'None' si es que todavia no se ha establecido ninguna.
        """
        tbar = self.get_widget("hbox8").get_children()[0]
        if isinstance(tbar, ContextToolbar):
            return tbar
        return None

    def on_realize(self, p_window):
        """
            p_window: un 'gtk.Window' que es la ventana principal.

            Se ejecuta cuando se muestra la ventana principal al inicio
            de la aplicacion. Hace que el foco lo tenga el 'CommandWindow'
            (ventana de comandos), lo cual provoca que este sea el componente
            activo en la aplicacion y los menus de la barra de menus de la
            aplicacion asi como los botones de la barra de herramientas de la
            aplicacion solo realicen operaciones sobre el mismo.
        """
        self.__command_win.grab_focus()

    def on_mnotebook_switch_page(self, p_notebook, p_gpointer, p_page):
        """
            p_notebook: el 'gtk.Notebook' principal quien posee dentro al
                        'CurrentDirectory' y al 'Workspace'.
            p_gpointer: un 'GPointer'.
            p_page:     el indice de la pagina actual en 'p_notebook'.

            Se ejecuta cuando se cambia del 'CurrentDirectory' al 'Workspace'
            y viceversa. Muestra el nombre del elemento que se esta mostrando
            ("Current Directory" o "Workspace").
        """
        who = p_notebook.get_nth_page(p_page)
        text = {self.__cdirectory: "Current Directory",
                self.__wspace: "Workspace"}[who]
        self.get_widget("frame3").get_label_widget().set_text(text)

    def on_mnotebook_focus_in_event(self, p_notebook, p_event):
        """
            p_notebook: el 'gtk.Notebook' que recibio la sennal.
            p_event:    el evento que desencadeno la sennal.

            Retorna:    'True' para detener otros manejadores que se invoquen
                         para el evento.

            Ocurre cuando el notebook principal de la aplicacion('p_notebook')
            recibe el foco. Si 'p_notebook' esta mostrando al
            'CurrentDirectory' entonces llama el metodo
            'CurrentDirectory.grab_focus', sino, llama el metodo
            'Workspace.grab_focus'.
        """
        p_notebook.get_nth_page(p_notebook.get_current_page()).grab_focus()
        return True

    def on_start_button_clicked(self, p_butt):
        """
            p_butt: un 'gtk.Button' que es el boton 'Start' de la aplicacion.

            Ocurre cuando se da click en el boton 'Start' de la aplicacion.
            Muestra el Menu Inicio de la aplicacion.
        """
        self.__start_menu.menu_popup(p_butt)

    def close(self):
        """
            Retorna: 'True' para evitar que se cierre la ventana principal
                     antes de que se cierre la coneccion con Octave.

            Cierra la coneccion con Octave, luego termina el ciclo principal de
            'Connection'('Connection.run') y posteriormente se llama el metodo
            'MainWindow.close_now' lo que provoca el cierre de la aplicacion.
        """
        self.__conn.write("\x03 exit\n")
        return True

    def close_now(self):
        """
            Este metodo es llamado cuando termina el ciclo principal de la
            coneccion con Octave('Connection.run'). Salva todos los cambios
            necesarios y cierra la aplicacion.
        """
        self.__shortcuts_toolbar.save_shortcut()

        gtk.main_quit()

    def show_help(self):
        """
            Muestra la ayuda de Octave.
        """
        if self.__help:
            self.__help.present()
        else:
            self.__help = HelpWindow(self)

    def help_closed(self):
        """
            Informa que la ayuda de Octave se ha cerrado.
        """
        self.__help = None

    def open_site(self, p_url):
        """
            p_url: una cadena que representa la direccion de un archivo o un
                   sitio web. e.g. "http://google.com", "file:///home/archivo".

            Abre la direccion 'p_url' en un navegador web.
        """
        os.system("firefox '%s' &" %p_url)  # <--- hacerlo generico --->

    def on_button_up_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando se da click en el boton de cambiar al directorio
            padre, el cual se encuentra en la barra de herramientas principal
            de la aplicacion. Llama el metodo 'CurrentDirectory.go_up'.
        """
        self.__cdirectory.go_up()

    def set_menu_bar(self, p_mbar, p_tbar, p_index):
        """
            p_mbar:  un 'ContextMenuBar'.
            p_tbar:  un 'ContextToolbar'.
            p_index: un entero que puede ser '0', '1' o '2'.

            Establece como barra de menus de la aplicacion a 'p_mbar' y como
            barra de heramientas de la aplicacion a 'p_tbar'.

            Si 'p_index' = '0' se resalta el 'CommandWindow' en azul.
            Si 'p_index' = '1' se resalta el 'CommandHistory' en azul.
            Si 'p_index' = '2' se resalta en azul al 'CurrentDirectory'
            si es que este se esta mostrando, sino resalta al 'Workspace'.
        """
        hbox = self.get_widget("hbox6")
        old_mbar = hbox.get_children()[0]

        if old_mbar is not p_mbar:
            # Ponemos la nueva barra de menu.
            hbox.remove(old_mbar)
            hbox.add(p_mbar)

            # Ponemos la nueva barra de herramientas.
            old_tbar = self.get_toolbar()
            if old_tbar:
                old_tbar.remove_combo()
                old_tbar.remove_butt_up()
            p_tbar.insert_combo()
            p_tbar.insert_butt_up()
            hbox = self.get_widget("hbox8")
            hbox.remove(hbox.get_children()[0])
            hbox.add(p_tbar)

            # Resaltamos el nombre del elemento activo.
            labels = [self.get_widget("label7"), self.get_widget("label6"),
                      self.get_widget("label8")]
            states = {True: 'background="#80a5d1" foreground="#ffffff"',
                      False: 'foreground="#84857b"'}

            for pos, label in enumerate(labels):
                state = states[pos == p_index]
                text = label.get_text()
                label.set_markup('<span %s><b>%s</b></span>' %(state, text))

    def show_about(self):
        """
            Muestra la ventana 'About EIDMAT' de la aplicacion, la cual
            contiene informacion acerca de quienes trabajan en el proyecto
            y la licencia de EIDMAT.
        """
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        path = os.path.join(root, "images", "about.glade")

        about = gtk.glade.XML(path, "about").get_widget("about")
        about.run()
        about.destroy()
