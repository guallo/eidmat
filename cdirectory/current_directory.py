import os
import gtk

from cdirectory.current_directory_toolbar import CurrentDirectoryToolbar
from cdirectory.list_files import ListFiles
from util.select_folder_dialog import SelectFolderDialog
from menubar.cdirectory_menu_bar import CDirectoryMenuBar
from toolbar.cdirectory_toolbar import CDirectoryToolbar
from cmds.change_directory import ChangeDirectory


class CurrentDirectory(gtk.VBox):
    """
        El directorio actual del usuario.
    """
    def __init__(self, p_mwindow, p_parent, p_conn, p_combo, p_butt_up):
        """
            p_mwindow: un 'MainWindow'.
            p_parent:  un 'gtk.Window' que es la ventana principal.
            p_conn:    un 'Connection' que es la conexion con Octave.
            p_combo:   un 'ComboOfDirectories' en el cual mostrar el camino del
                       directorio actual.
            p_butt_up: un 'gtk.ToolButton' para subir al directorio padre.

            Retorna:   un nuevo 'CurrentDirectory'.

            Crea un nuevo 'CurrentDirectory' el cual esta formado por un
            'CurrentDirectoryToolbar'(barra de herramientas) y un 'ListFiles'
            (listado de las carpetas y archivos).
        """
        gtk.VBox.__init__(self)

        self.set_border_width(3)

        # Creacion de la barra de herramientas.
        self.__toolbar = CurrentDirectoryToolbar(self)
        self.pack_start(self.__toolbar, False)

        # Creacion de la lista de archivos.
        scroll = gtk.ScrolledWindow()
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.__tree = ListFiles(self)
        scroll.add(self.__tree)
        self.pack_start(scroll)

        self.__mwindow = p_mwindow
        self.__parent = p_parent
        self.__conn = p_conn
        self.__combo = p_combo
        self.__butt_up = p_butt_up
        self.__path = ""
        self.__mbar = CDirectoryMenuBar(p_mwindow)
        self.__tbar = CDirectoryToolbar(p_mwindow)

        self.update_appearance()

    def get_mbar(self):
        """
            Retorna: un CDirectoryMenuBar.

            Devuelve la barra de menus del CurrentDirectory.
        """
        return self.__mbar

    def grab_focus(self):
        """
            Hace que el foco lo tenga el 'ListFiles'(listado de carpetas y
            archivos), lo cual provoca que el 'CurrentDirectory' sea el
            componente activo en la aplicacion y los menus de la barra de menu
            de la aplicacion asi como los botones de la barra de herramientas
            de la aplicacion solo realicen operaciones sobre el mismo.
        """
        self.__tree.grab_focus()

    def get_path(self):
        """
            Retorna: el camino del directorio actual del usaurio.

            Retorna el camino que esta mostrando el 'CurrentDirectory',
            e.g. '/home/administrador/Desktop'
        """
        return self.__path

    def set_path(self, p_path):
        """
            p_path: una cadena que representa un camino a un directorio.

            Establece a 'p_path' como directorio actual del usuario. Llama el
            metodo 'ListFiles.show_path' pasando como parametro a 'p_path'.
        """
        sensitive = {"/": False}.get(p_path, True)
        self.__butt_up.set_sensitive(sensitive)
        self.__toolbar.get_button_up().set_sensitive(sensitive)

        self.__path = p_path
        self.__combo.show_path(p_path)
        self.__tree.show_path(p_path)

    def try_to_open(self, p_path):
        """
            p_path: una cadena que representa un camino a un archivo o
                    directorio.

            Si 'p_path' apunta a un directorio entonces se establece el mismo
            como directorio actual del usuario.

            Si 'p_path' apunta a un archivo se trata de abrir el mismo.
        """
        if os.path.isdir(p_path):
            if os.access(p_path, os.R_OK):
                self.__conn.append_command(ChangeDirectory(p_path))
            else:
                pass
        else:
            ext = os.path.splitext(p_path)[1]

            if ext == ".var" or ext == ".mat":
                pass
            elif ext == ".eidmat":
                pass
            else:
                self.__mwindow.show_edebugger(True, True, p_path)

    def go_up(self):
        """
            Cambia al directorio padre.
        """
        self.__conn.append_command(ChangeDirectory(os.path.dirname(self.__path)))

    def browse_for_folder(self):
        """
            Muestra una dialogo de seleccion de directorios en el cual el
            usuario escoge el directorio al que desee cambiar.
        """
        path = SelectFolderDialog("Select a Directory", self.__parent,
                                   self.get_path()).run()
        if path:
            self.try_to_open(path)

    def update_appearance(self):
        """
            Actualiza la apariencia de los menus y barra de herramientas
            correspondientes al 'CurrentDirectory', decidiendo cuales de estos
            se mostraran activos o no en dependencia de las acciones que se
            puedan realizar.
        """
        tbar = self.__tbar

        tbar.get_cut().set_sensitive(False)
        tbar.get_copy().set_sensitive(False)
        tbar.get_paste().set_sensitive(False)

    def activate(self):
        """
            Resalta el 'CurrentDirectory' en azul y muestra su barra de menus y
            de herramientas.
        """
        mwindow = self.__mwindow
        mnotebook = mwindow.get_mnotebook()
        my_page = mnotebook.page_num(self)

        if mnotebook.get_current_page() != my_page:
            mnotebook.set_current_page(my_page)

        mwindow.set_menu_bar(self.__mbar, self.__tbar, 2)
