import os
import gtk

from util.confirm import Confirm
from util.message import Message
from cmds.save_vars import SaveVars
from cmds.new_var import NewVar
from cmds.delete_var import DeleteVar
from cmds.duplicate_var import DuplicateVar
from wspace.workspace_toolbar import WorkspaceToolbar
from wspace.list_vars import ListVars
from wspace.workspace_save_dialog import WorkspaceSaveDialog
from wspace.workspace_import_dialog import WorkspaceImportDialog
from wspace.import_wizard import ImportWizard
from menubar.wspace_menu_bar import WSpaceMenuBar
from toolbar.wspace_toolbar import WSpaceToolbar


class Workspace(gtk.VBox):
    """
        El espacio de trabajo del usuario.
    """
    def __init__(self, p_mwindow, p_conn, p_cdirectory, p_parent):
        """
            p_mwindow:    un 'MainWindow'.
            p_conn:       un 'Connection' que es la conexion con Octave.
            p_cdirectory: un 'CurrentDirectory'.
            p_parent:     un 'gtk.Window' que es la ventana principal.

            Retorna:      un nuevo 'Workspace'.

            Crea un nuevo 'Workspace' el cual esta formado por una barra de
            herramientas('WorkspaceToolbar') y un listado de las variables
            definidas por el usuario('ListVars').
        """
        gtk.VBox.__init__(self)

        self.set_border_width(3)

        self.__mwindow = p_mwindow
        self.__conn = p_conn
        self.__current_dir = p_cdirectory
        self.__parent = p_parent
        self.__import_wiz = None
        self.__confirmed_del = False
        self.__confirmed_clear = False
        self.__mbar = WSpaceMenuBar(p_mwindow)
        self.__tbar = WSpaceToolbar(p_mwindow)

        # Creacion de la barra de herramientas.
        self.__toolbar = WorkspaceToolbar(self)
        self.pack_start(self.__toolbar, False)

        # Creacion de la lista de variables.
        scroll = gtk.ScrolledWindow()
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.__tree = ListVars(self.__conn, self)
        scroll.add(self.__tree)
        self.pack_start(scroll)

        self.update_appearance()

    def get_mbar(self):
        """
            Retorna: un WSpaceMenuBar.

            Devuelve la barra de menus del Workspace.
        """
        return self.__mbar

    def import_wiz_closed(self):
        """
            Informa que el asistente de importacion de variables
            ('ImportWizard') se ha cerrado.
        """
        self.__import_wiz = None

    def grab_focus(self):
        """
            Hace que el foco lo tenga el 'ListVars'(listado de variables),
            lo cual provoca que el 'Workspace' sea el componente activo en
            la aplicacion y los menus de la barra de menu de la aplicacion
            asi como los botones de la barra de herramientas de la aplicacion
            solo realicen operaciones sobre el mismo.
        """
        self.__tree.grab_focus()

    def update(self, p_vars):
        """
            p_vars: una 'list'(lista) con datos de las variables definidas por
                    el usuario como su nombre, tamanno, bytes, clase a la que
                    pertenece, entre otros.

            Este metodo es llamado cuando se necesita actualizar el 'ListVars'
            (listado de variables) del 'Workspace' con 'p_vars'. Llama el
            metodo 'ListVars.show_vars(p_vars)'.
        """
        self.__tree.show_vars(p_vars)

    def new_var(self):
        """
            Crea una nueva variable.
        """
        self.__conn.append_command(NewVar())

    def import_data(self):
        """
            Es llamado cuando el usario desea importar variables hacia el
            'Workspace'. Muestra un dialogo para que el usuario indique donde
            estan los datos a importar, una vez indicado esto, se muestra el
            'ImportWizard'(Asistente de Importacion) en el cual se listan las
            variables presentes en el archivo seleccionado.
        """
        if self.__import_wiz:
            self.__import_wiz.present()
            return

        path = WorkspaceImportDialog(self.__parent,
                                     self.__current_dir.get_path()).run()
        if not path:
            return

        # if (No existe el archivo):
        if not os.access(path, os.F_OK):
            msg = ("could not be find.",
            "Please check that you typed the location correctly and try again."
            )

        # elif (No se puede leer):
        elif not os.access(path, os.R_OK):
            msg = ("could not be open.",
                 "You do not have the permissions necessary to open the file.")

        else:
            self.__import_wiz = ImportWizard(path, self.__conn, self,
                                                   self.__parent,
                                                   self.__tree.get_model())
            return

        Message(gtk.STOCK_DIALOG_WARNING,
                "%s\n\n%s" %(path, "\n".join(msg)), "Importing Failed",
                self.__parent).run()

    def save(self, p_all=True, p_path = None):
        """
            p_all: 'True' si se quieren guardar todas las variables o 'False'
                   si solo se quieren guardar las variables seleccionadas.
            p_path: Contiene la localizacion directa del path donde se 
                   guardaran todas las variables del workspace utilizada en el 
                   trabajo con proyecto.
            
            Muestra un dialogo para que el usuario indique donde guardar las
            variables, una vez indicado el fichero, se guardan las variables
            en el mismo.
        """
        parent = self.__parent
        current_dir = self.__current_dir

        ########################## BEGIN ###############################
        while True:
            if p_path:
                path = p_path
            else:
                path = WorkspaceSaveDialog(parent, 
                                           current_dir.get_path()).run()
                if not path:
                    break
            
            save = True

            # if (Existe el archivo):
            if os.access(path, os.F_OK):

                # if (No se puede escribir):
                if not os.access(path, os.W_OK):
                    save = False
                    stock = gtk.STOCK_DIALOG_WARNING
                    msg = ("is read-only on disk.",
                        "Do you want to save to a different name or location?")

            # elif (No puede crearse):
            elif not os.access(os.path.dirname(path), os.W_OK):
                save = False
                stock = gtk.STOCK_DIALOG_QUESTION
                msg = ("cannot be saved to this location.",
                       "Do you want to save to a different location?")

            if save:
                names = []
                model, paths = self.__tree.get_selection().get_selected_rows()

                if p_all:
                    for row in model:
                        names.append(model.get_value(row.iter, 1))

                else:
                    for p in paths:
                        names.append(model.get_value(model.get_iter(p), 1))

                self.__conn.append_command(SaveVars(names, path))
                break

            elif not Confirm(stock, "%s\n\n%s" %(path, "\n".join(msg)),
                                    "Save to VAR-File:", parent).run():
                break
        ########################## END #################################

    def rename(self):
        """
            Pone en modo editable el campo nombre de la variable
            seleccionada para que el usuario ponga el nombre deseado.
        """
        tree = self.__tree
        paths = tree.get_selection().get_selected_rows()[1]

        if len(paths) == 1:
            tree.set_cursor(paths[0], tree.get_column(0), True)

    def delete(self):
        """
            Elimina las variables seleccionadas.
        """
        model, paths = self.__tree.get_selection().get_selected_rows()

        if not paths:
            return

        if not self.__confirmed_del:
            s = ""
            if len(paths) > 1:
                s = "s"
            msg = "Are you sure you want to delete the selected variable%s?" %s
            resp = Confirm(gtk.STOCK_DIALOG_QUESTION, msg, "Confirm delete",
                           self.__parent,
                           "Do not show this prompt again.").run()
            if not resp:
                return
            if resp[0]:
                self.__confirmed_del = True

        for path in paths:
            self.__conn.append_command(DeleteVar(model[path][1]))

    def copy(self):
        """
            Copia en el 'gtk.Clipboard' los nombres de las variables
            seleccionadas separados por coma, permitiendo que el usuario
            los pegue donde desee posteriormente.
        """
        model, paths = self.__tree.get_selection().get_selected_rows()

        names = [model.get_value(model.get_iter(path), 1) for path in paths]
        if names:
            self.get_clipboard("CLIPBOARD").set_text(", ".join(names))

    def duplicate(self):
        """
            Duplica las variables seleccionadas, es decir, crea una nueva
            variable por cada variable seleccionada, pero con su mismo valor.
        """
        model, paths = self.__tree.get_selection().get_selected_rows()
        method = self.__conn.append_command

        for path in paths:
            row = model[path]
            method(DuplicateVar(row[1], row[5]))

    def clear(self):
        """
            Limpia el 'Workspace', es decir que elimina todas las variables
            del usuario.
        """
        model = self.__tree.get_model()

        if not self.__confirmed_clear:
            resp = Confirm(gtk.STOCK_DIALOG_QUESTION,
                           "All variables will be deleted.", "Confirm delete",
                           self.__parent, "Do not show this prompt again."
                           ).run()
            if not resp:
                return
            if resp[0]:
                self.__confirmed_clear = True

        for row in model:
            self.__conn.append_command(DeleteVar(row[1]))

    def select_all(self):
        """
            Selecciona todas las variables.
        """
        self.__tree.get_selection().select_all()

    def update_appearance(self):
        """
            Actualiza la apariencia de los menus y barra de herramientas
            correspondientes al 'Workspace', decidiendo cuales de estos
            se mostraran activos o no en dependencia de las acciones que
            se puedan realizar.
        """
        edit_menu = self.__mbar.get_edit()
        tbar = self.__tbar
        tbar2 = self.__toolbar
        context_menu = self.__tree.get_menu()
        count = self.__tree.get_selection().count_selected_rows()

        if not count:
            edit_menu.get_copy().set_sensitive(False)
            edit_menu.get_duplicate().set_sensitive(False)
            edit_menu.get_delete().set_sensitive(False)
            edit_menu.get_rename().set_sensitive(False)

            tbar.get_copy().set_sensitive(False)

            tbar2.get_delete().set_sensitive(False)

            context_menu.get_save().set_sensitive(False)
            context_menu.get_copy().set_sensitive(False)
            context_menu.get_duplicate().set_sensitive(False)
            context_menu.get_delete().set_sensitive(False)
            context_menu.get_rename().set_sensitive(False)
        else:
            edit_menu.get_copy().set_sensitive(True)
            edit_menu.get_duplicate().set_sensitive(True)
            edit_menu.get_delete().set_sensitive(True)

            tbar.get_copy().set_sensitive(True)

            tbar2.get_delete().set_sensitive(True)

            context_menu.get_save().set_sensitive(True)
            context_menu.get_copy().set_sensitive(True)
            context_menu.get_duplicate().set_sensitive(True)
            context_menu.get_delete().set_sensitive(True)

            if count == 1:
                edit_menu.get_rename().set_sensitive(True)
                context_menu.get_rename().set_sensitive(True)
            else:
                edit_menu.get_rename().set_sensitive(False)
                context_menu.get_rename().set_sensitive(False)

    def activate(self):
        """
            Resalta el 'Workspace' en azul y muestra su barra de menus y
            de herramientas.
        """
        mwindow = self.__mwindow
        mnotebook = mwindow.get_mnotebook()
        my_page = mnotebook.page_num(self)

        if mnotebook.get_current_page() != my_page:
            mnotebook.set_current_page(my_page)

        mwindow.set_menu_bar(self.__mbar, self.__tbar, 2)
