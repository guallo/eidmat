import os
import gtk.glade

from mwindow.combo_of_directories import ComboOfDirectories
from mwindow.mwindow_open_dialog import MWindowOpenDialog
from mwindow.popup_menu import PopupMenu
from mwindow.menu_start import MenuStart
from cmdhistory.command_history import CommandHistory
from cmdwindow.command_window import CommandWindow
from cdirectory.current_directory import CurrentDirectory
from wspace.workspace import Workspace
from edebugger.editor_debugger import EditorDebugger
from edebugger.dialogs.editor_debug_on_event_dialog import EditorDebugOnEventDialog
from help.gui.help_window import HelpWindow
from toolbar.context_toolbar import ContextToolbar
from menubar.context_menu_bar import ContextMenuBar
from menubar.menu.project_menu import ProjectMenu
from shortcuts.shortcut_toolbar import ShortcutToolBar
from project.tree_project import TreeProject
from conn.connection import Connection
from conn.terminal import TerminalState
from cmds.exit_debug_mode import ExitDebugMode
from cmds.continue_exec import ContinueExec
from cmds.step import Step
from cmds.check_debug_on_event import CheckDebugOnEvent
from cmds.set_debug_on_event import SetDebugOnEvent


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
        self.__window.maximize()
        self.__window.connect("delete-event", lambda p_win, p_event:
                                                     self.close())

        # Creacion de la 'Connection'.
        self.__conn = Connection(self)
        self.__conn.connect("stopped_in_file", self.on_conn_stopped_in_file)
        self.__conn.connect("state_changed", self.on_conn_state_changed)

        # Creacion del 'Combo of directories'.
        self.__combo = ComboOfDirectories(self)

        # Creacion del boton para subir al directorio padre.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "go_up.png"))
        self.__butt_up = gtk.ToolButton(img, "Up")
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

        # Creacion del 'TreeProject'        
        self.__tree_project = TreeProject(self, self.__window)

        # Creacion del Menu Project.
        self.__project_item = gtk.MenuItem("_Project")
        self.__project_item.set_submenu(ProjectMenu(self))
        self.__project_item.show_all()

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

        # Acciones de debugeo
        debug_always_sensitive_action_group = \
                gtk.ActionGroup("DebugAlwaysSensitiveActionGroup")
        self.__debug_always_sensitive_action_group = \
                debug_always_sensitive_action_group

        debug_always_sensitive_action_group.add_toggle_actions([
                ("OpenMFiles", None, "Open M-Files When Debu_gging",
                  None, "Open M-Files when debugging", None, True)
                                                               ], None)
        debug_always_sensitive_action_group.add_actions([
                ("StopIfErrors", None, "Stop if Errors/_Warnings...",
                 None, "Stop if errors/warnings...",
                 self.on_stop_if_errors_activate)
                                                        ], self.get_window)

        debug_steps_action_group = gtk.ActionGroup("DebugStepsActionGroup")
        self.__debug_steps_action_group = debug_steps_action_group

        debug_steps_action_group.add_actions([
                ("Step", None, "_Step", "F9", "Step",
                 self.on_step_activate),
                ("StepIn", None, "Step _In", "F11", "Step in",
                 self.on_step_in_activate),
                ("StepOut", None, "Step _Out", "<Shift>F11", "Step out",
                 self.on_step_out_activate),
                ("Continue", None, "Co_ntinue", "<Control>F5", "Continue",
                 self.on_continue_activate)
                                             ], True)

        debug_steps_action_group.add_actions([
                ("ExitDebug", None, "Exit _Debug Mode", None,
                 "Exit debug mode", self.on_exit_debug_activate)
                                             ], None)

        # Aceleradores para las acciones de debugeo
        debug_accel_group = gtk.AccelGroup()
        self.__window.add_accel_group(debug_accel_group)

        debug_actions = debug_always_sensitive_action_group.list_actions() + \
                        debug_steps_action_group.list_actions()

        for action in debug_actions:
            action.set_accel_group(debug_accel_group)

        # Proxies para las acciones de debugeo
        openmfiles_action = debug_always_sensitive_action_group. \
                            get_action("OpenMFiles")
        stopiferrors_action = debug_always_sensitive_action_group. \
                            get_action("StopIfErrors")
        step_action = debug_steps_action_group.get_action("Step")
        stepin_action = debug_steps_action_group.get_action("StepIn")
        stepout_action = debug_steps_action_group.get_action("StepOut")
        continue_action = debug_steps_action_group.get_action("Continue")
        exitdebug_action = debug_steps_action_group.get_action("ExitDebug")

        contexts = (self.__cmdhistory, self.__command_win, self.__cdirectory,
                    self.__wspace, self.__tree_project)

        for context in contexts:
            debug_menu = context.get_mbar().get_debug()

            openmfiles_item = openmfiles_action.create_menu_item()
            stopiferrors_item = stopiferrors_action.create_menu_item()
            step_item = step_action.create_menu_item()
            stepin_item = stepin_action.create_menu_item()
            stepout_item = stepout_action.create_menu_item()
            continue_item = continue_action.create_menu_item()
            exitdebug_item = exitdebug_action.create_menu_item()

            debug_menu.append(openmfiles_item)
            debug_menu.append(gtk.SeparatorMenuItem())
            debug_menu.append(step_item)
            debug_menu.append(stepin_item)
            debug_menu.append(stepout_item)
            debug_menu.append(continue_item)
            debug_menu.append(gtk.SeparatorMenuItem())
            debug_menu.append(stopiferrors_item)
            debug_menu.append(gtk.SeparatorMenuItem())
            debug_menu.append(exitdebug_item)

            debug_menu.show_all()

        self.__conn.start()
        self.__window.show_all()
        self.__command_win.activate()

        self.__help = None
        self.__edebugger = None

    def get_debug_always_sensitive_action_group(self):
        """
            Retorna: un 'gtk.ActionGroup'.

            Retorna el grupo de acciones de
            debugeo que siempre estaran sensibles.
        """
        return self.__debug_always_sensitive_action_group

    def get_debug_steps_action_group(self):
        """
            Retorna: un 'gtk.ActionGroup'.

            Retorna el grupo de acciones de debugeo
            que tienen que ver con los Steps.
        """
        return self.__debug_steps_action_group

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

    def get_menu_bar(self):
        """
            Retorna: un 'ContextMenuBar'(barra de menus principal),
                     o 'None' si no hay ninguna todavia.

            Retorna la barra de menus principal de la aplicacion,
            o 'None' si es que todavia no se ha establecido ninguna.
        """
        mbar = self.get_widget("hbox6").get_children()[0]
        if isinstance(mbar, ContextMenuBar):
            return mbar
        return None

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

    def get_edebugger(self):
        """
            Retorna: un 'EditorDebugger' o 'None'.

            Devuelve el editor debugger de la aplicacion
            si esta abierto, o 'None' en caso contrario.
        """
        return self.__edebugger

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

            Se ejecuta cuando se intercambia entre los elementos 
            'CurrentDirectory', 'Workspace' y 'Project' y muestra el nombre del
            elemento activo ("Current Directory", "Workspace" o "Project").
        """
        who = p_notebook.get_nth_page(p_page)
        text = {self.__cdirectory: "Current Directory",
                self.__wspace: "Workspace", self.__tree_project: "Project"}[who]
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
                     antes de que se cierre el 'EditorDebugger' si es que
                     se quedo abierto, o antes de que se cierre la coneccion
                     con Octave.

            Si el 'EditorDebugger' esta abierto se manda a cerrar,
            si se cerro, entonces se cierra la coneccion con Octave,
            lo que trae como consecuencia que termine el ciclo principal
            de 'Connection' ('Connection.run') y se llame el metodo
            'MainWindow.close_now', provocando este ultimo el cierre de
            la aplicacion.
        """
        edebugger = self.__edebugger

        if edebugger:
            edebugger.get_window().present()
            if not edebugger.close():
                return True

        # FIXME: No sale de Octave cuando esta activo debug_on_interrupt.
        #        Probar con "\x03 \nexit\n"
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

    def show_edebugger(self, p_present, p_jump_to, *p_paths):
        """
            p_present: un boolean que decide si darle el foco
                       al editor.
            p_jump_to: un boolean que decide si estara activo
                       o no el documento que se desea abrir.
            p_paths:   un 'tuple' de cadenas, donde cada una
                       representa la direccion de un fichero
                       a abrir.

            Muestra el editor debugger de la aplicacion.
        """
        edebugger = self.__edebugger

        if edebugger:
            if p_present:
                if edebugger.is_attach():
                    pass  # poner activo el editor debugger cuando se pueda empotrar.
                else:
                    edebugger.get_window().present()

            if not p_paths:
                edebugger.new_document(None, p_jump_to)

            for path in p_paths:
                edebugger.new_document(path, p_jump_to)

        else:
            edebugger = EditorDebugger(self, *p_paths)
            edebugger.connect("destroy", self.on_edebugger_destroy)
            self.__edebugger = edebugger

    def on_edebugger_destroy(self, p_edebugger):
        """
            p_edebugger: un 'EditorDebugger'.

            Informa que el Editor Debugger se ha cerrado.
        """
        self.__edebugger = None

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
        old_mbar = self.get_menu_bar()

        if old_mbar == p_mbar:
            return

        # Ponemos la nueva barra de menu.
        if old_mbar:
            old_mbar.remove(self.__project_item)

        p_mbar.insert(self.__project_item, 2)

        hbox = self.get_widget("hbox6")
        hbox.remove(hbox.get_children()[0])
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

    def open_(self):
        """
            Muestra un dialogo para que el usuario indique los archivos
            a abrir, y por cada archivo, segun su tipo, se realiza una
            accion determinada.
        """
        paths = MWindowOpenDialog(self.__window, self.__cdirectory.get_path()).run()

        if paths:
            splitext = os.path.splitext

            for path in paths:
                ext = splitext(path)[1]

                if ext == ".var" or ext == ".mat":
                    pass
                elif ext == ".eidmat":
                    pass
                else:
                    self.show_edebugger(True, True, path)
        
    def get_tree_project(self):
        return self.__tree_project

    def get_project_menu(self):
        return self.__project_item.get_submenu()
    
    def create_project(self):
        """ 
            Metodo mediante el cual se adiciona el tag del projecto al 
            <self.__mnotebook>.
        """
        if self.__mnotebook.get_n_pages() < 3:
            self.__mnotebook.append_page(self.__tree_project, gtk.Label("Project"))
        else:
            self.close_project()
            self.__mnotebook.append_page(self.__tree_project, gtk.Label("Project"))
        self.__mnotebook.show_all()
        
    def close_project(self):
        """ 
            Elimina la hoja <Proyecto> durante el cierre del mismo.
        """
        self.__mnotebook.remove_page(2)

    def on_conn_stopped_in_file(self, p_conn, p_file):
        #FIXME: documentacion

        group = self.__debug_always_sensitive_action_group
        action = group.get_action("OpenMFiles")

        if action.get_active():
            self.show_edebugger(False, False, p_file)

    def on_conn_state_changed(self, p_conn, p_state):
        group = self.__debug_steps_action_group

        if p_state == TerminalState.READY:
            group.set_sensitive(False)
        elif p_state == TerminalState.DEBUGGING:
            group.set_sensitive(True)

    def on_step_activate(self, p_action, p_verbose=True):
        #FIXME: documentacion

        if self.__conn.get_state() != TerminalState.DEBUGGING:
            return
        self.__conn.append_command(Step(1, p_verbose))

    def on_step_in_activate(self, p_action, p_verbose=True):
        #FIXME: documentacion

        if self.__conn.get_state() != TerminalState.DEBUGGING:
            return
        self.__conn.append_command(Step(True, p_verbose))

    def on_step_out_activate(self, p_action, p_verbose=True):
        #FIXME: documentacion

        if self.__conn.get_state() != TerminalState.DEBUGGING:
            return
        self.__conn.append_command(Step(False, p_verbose))

    def on_continue_activate(self, p_action, p_verbose=True):
        #FIXME: documentacion

        if self.__conn.get_state() != TerminalState.DEBUGGING:
            return
        self.__conn.append_command(ContinueExec(p_verbose))

    def on_stop_if_errors_activate(self, p_action, p_get_parent):
        #FIXME: documentacion

        dialog = EditorDebugOnEventDialog(p_get_parent())
        before = dialog.get_active_buttons()
        dialog.set_spinner_visible(True)

        def on_checker_debug_on_event_update_request(p_checker, p_data):
            if not dialog:
                return

            def replace():
                result = p_data.get_data("debug_on_event")
                dialog.set_active_buttons(result["err"], result["war"], result["int"])

            def hide_replacer(*p_args):
                dialog.set_replacer_visible(False)

            def replace_and_hide(*p_args):
                replace()
                hide_replacer()

            dialog.set_spinner_visible(False)
            after = dialog.get_active_buttons()

            # FIXME: puede que el usuario haya hecho algo
            # y sin embargo after == before.
            if after != before:
                dialog.set_replacer_visible(True)
                dialog.connect_replacer_callbacks(replace_and_hide, hide_replacer)
            else:
                replace()

        checker = CheckDebugOnEvent()
        checker.connect("debug_on_event_update_request", on_checker_debug_on_event_update_request)
        self.__conn.append_command(checker)

        result = dialog.run()
        dialog = None

        if not result:
            return

        result = {"err": result[0], "war": result[1], "int": result[2]}
        setter = SetDebugOnEvent(result)
        self.__conn.append_command(setter)

    def on_exit_debug_activate(self, p_action):
        #FIXME: documentacion

        if self.__conn.get_state() != TerminalState.DEBUGGING:
            return
        self.__conn.append_command(ExitDebugMode())
