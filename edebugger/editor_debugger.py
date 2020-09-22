import os
import gtk

from util.confirm import Confirm
from conn.terminal import TerminalState
from cmds.run_file import RunFile
from menubar.editor_menu_bar import EditorMenuBar
from edebugger.editor_toolbar import EditorToolbar
from edebugger.editor_notebook import EditorNotebook
from edebugger.editor_tab import EditorTab, EditorTabState
from edebugger.editor_document import EditorDocument
from edebugger.editor_statusbar import EditorSatusbar
from edebugger.dialogs.editor_open_dialog import EditorOpenDialog
from edebugger.dialogs.editor_save_dialog import EditorSaveDialog
from edebugger.dialogs.editor_close_confirmation_dialog import \
                           EditorCloseConfirmationDialog
from edebugger.dialogs.editor_load_path_dialog import EditorLoadPathDialog
from edebugger.completion.provider_controller import ProviderController


class EditorDebugger(gtk.VBox):
    """
        Editor debugger de la aplicacion.
    """

    def __init__(self, p_mwindow, *p_paths):
        """
            p_mwindow: un MainWindow.
            p_paths:   un tupla de cadenas que representan
                       las direcciones de los ficheros a abrir.

            Retorna:   un EditorDebugger.

            Crea un nuevo EditorDebugger.
        """

        #assert (type(p_mwindow) == MainWindow) FIXME: import loop

        gtk.VBox.__init__(self)

        self.__mwindow = p_mwindow
        self.__provider_controller = ProviderController()
        self.__is_attach = False
        self.__curtab = None
        self.__next_num = 1
        self.__clipboard_handler_id = None

        self.__mbar = EditorMenuBar(p_mwindow)

        # FIXME: implementar barra de herramientas de la aplicacion.
        self.__tbar = None

        # 'gtk.HBox' que contiene a 'self.__mbar'.
        self.pack_start(gtk.HBox(), False, False, 0)

        # Barra de herramientas del 'EditorDebugger'.
        self.__toolbar = EditorToolbar(self)
        self.pack_start(self.__toolbar, False, False, 0)

        # Aceleradores
        self.__debug_accel_group = gtk.AccelGroup()

        # Acciones de debugeo.
        self.__debug_run_action_group = None  # toma valor en 'self.__create_actions'
        self.__debug_breakpoints_action_group = None  # toma valor en 'self.__create_actions'
        self.__debug_steps_action_group = None  # toma valor en 'self.__create_actions'
        self.__debug_opened_files_action_group = None  # toma valor en 'self.__create_actions'
        self.__create_actions()

        # Notebook del 'EditorDebugger'.
        notebook = EditorNotebook()
        notebook.connect("switch-page", self.on_notebook_switch_page)
        notebook.connect("page-added", self.on_notebook_page_added)
        notebook.connect("page-removed", self.on_notebook_page_removed)
        notebook.connect("tab_close_request",
                         self.on_notebook_tab_close_request)
        self.pack_start(notebook, True, True, 0)
        self.__notebook = notebook

        # Barra de estado del 'EditorDebugger'.
        statusbar = EditorSatusbar()
        self.pack_start(statusbar, False, False, 0)
        self.__statusbar = statusbar

        conn = p_mwindow.get_connection()
        self.__stopped_in_file_handler_id = conn.connect("stopped_in_file",
                                                self.on_conn_stopped_in_file)
        self.__state_changed_handler_id = conn.connect("state_changed",
                                                self.on_conn_state_changed)
        conn_state = conn.get_state()
        if conn_state != None:
            self.on_conn_state_changed(conn, conn_state)
        self.connect("destroy", self.on_destroy)

        # Contexts ids para la barra de estado.
        self.__flash_context_id = statusbar.get_context_id("flash message")
        #self.__tip_context_id = statusbar.get_context_id("tip message")

        self.init_update()

        if True:
            self.detach()
        else:
            self.attach()

        if not p_paths:
            self.new_document()

        for path in p_paths:
            assert (type(path) == str and path)

            self.new_document(path)

    def __create_actions(self):
        #FIXME: documentacion

        mwindow = self.__mwindow
        mwindow_debug_always_sensitive_action_group = \
                mwindow.get_debug_always_sensitive_action_group()
        mwindow_debug_steps_action_group = \
                mwindow.get_debug_steps_action_group()

        # Acciones
        debug_always_sensitive_action_group = \
                gtk.ActionGroup("DebugAlwaysSensitiveActionGroup")

        debug_always_sensitive_action_group.add_actions([
                ("StopIfErrors", None, "Stop if Errors/_Warnings...",
                 None, "Stop if errors/warnings...",
                 mwindow.on_stop_if_errors_activate)
                                                        ], self.get_window)

        debug_run_action_group = gtk.ActionGroup("DebugRunActionGroup")
        self.__debug_run_action_group = debug_run_action_group

        debug_run_action_group.add_actions([
                ("Run", None, "_Run", "F5", "Run", self.on_run_activate)
                                           ], None)

        debug_breakpoints_action_group = \
                gtk.ActionGroup("DebugBreakpointsActionGroup")
        self.__debug_breakpoints_action_group = debug_breakpoints_action_group

        debug_breakpoints_action_group.add_actions([
                ("SetClearBreakpoint", None, "Se_t/Clear Breakpoint",
                 "F12", "Set/clear breakpoint",
                 self.on_set_clear_breakpoint_activate)
                                                   ], None)

        debug_steps_action_group = gtk.ActionGroup("DebugStepsActionGroup")
        self.__debug_steps_action_group = debug_steps_action_group

        debug_steps_action_group.add_actions([
                ("Step", None, "_Step", "F9", "Step",
                 mwindow.on_step_activate),
                ("StepIn", None, "Step _In", "F11", "Step in",
                 mwindow.on_step_in_activate),
                ("StepOut", None, "Step _Out", "<Shift>F11", "Step out",
                 mwindow.on_step_out_activate),
                ("Continue", None, "Co_ntinue", "<Control>F5", "Continue",
                 mwindow.on_continue_activate)
                                             ], False)

        debug_opened_files_action_group = \
                gtk.ActionGroup("DebugOpenedFilesActionGroup")
        self.__debug_opened_files_action_group = \
                debug_opened_files_action_group

        debug_opened_files_action_group.add_actions([
                ("ClearBreakpoints", None, "Clear Breakpoints in Opened _Files",
                 None, "Clear breakpoints in opened files",
                 self.on_clear_breakpoints_activate)
                                                    ], None)

        # Aceleradores
        debug_accel_group = self.__debug_accel_group

        debug_actions = \
                [mwindow_debug_always_sensitive_action_group.get_action("OpenMFiles")] + \
                [mwindow_debug_steps_action_group.get_action("ExitDebug")] + \
                debug_always_sensitive_action_group.list_actions() + \
                debug_run_action_group.list_actions() + \
                debug_breakpoints_action_group.list_actions() + \
                debug_steps_action_group.list_actions() + \
                debug_opened_files_action_group.list_actions()

        for action in debug_actions:
            action.set_accel_group(debug_accel_group)

        # Proxies
        openmfiles_action = mwindow_debug_always_sensitive_action_group. \
                            get_action("OpenMFiles")
        exitdebug_action = mwindow_debug_steps_action_group. \
                            get_action("ExitDebug")
        stopiferrors_action = debug_always_sensitive_action_group. \
                            get_action("StopIfErrors")
        run_action = debug_run_action_group.get_action("Run")
        setclearbreakpoint_action = debug_breakpoints_action_group. \
                            get_action("SetClearBreakpoint")
        step_action = debug_steps_action_group.get_action("Step")
        stepin_action = debug_steps_action_group.get_action("StepIn")
        stepout_action = debug_steps_action_group.get_action("StepOut")
        continue_action = debug_steps_action_group.get_action("Continue")
        clearbreakpoints_action = \
            debug_opened_files_action_group.get_action("ClearBreakpoints")

        debug_menu = self.__mbar.get_debug()

        openmfiles_item = openmfiles_action.create_menu_item()
        exitdebug_item = exitdebug_action.create_menu_item()
        stopiferrors_item = stopiferrors_action.create_menu_item()
        run_item = run_action.create_menu_item()
        setclearbreakpoint_item = setclearbreakpoint_action.create_menu_item()
        step_item = step_action.create_menu_item()
        stepin_item = stepin_action.create_menu_item()
        stepout_item = stepout_action.create_menu_item()
        continue_item = continue_action.create_menu_item()
        clearbreakpoints_item = clearbreakpoints_action.create_menu_item()

        debug_menu.append(openmfiles_item)
        debug_menu.append(gtk.SeparatorMenuItem())
        debug_menu.append(step_item)
        debug_menu.append(stepin_item)
        debug_menu.append(stepout_item)
        debug_menu.append(continue_item)
        debug_menu.append(run_item)
        debug_menu.append(gtk.SeparatorMenuItem())
        debug_menu.append(setclearbreakpoint_item)
        debug_menu.append(gtk.SeparatorMenuItem())
        debug_menu.append(clearbreakpoints_item)
        debug_menu.append(stopiferrors_item)
        debug_menu.append(gtk.SeparatorMenuItem())
        debug_menu.append(exitdebug_item)

        debug_menu.show_all()

        # Proxies para la barra de herramientas
        toolbar = self.__toolbar

        setclearbreakpoint_action.connect_proxy(toolbar.get_set_clear())
        clearbreakpoints_action.connect_proxy(toolbar.get_clear_opened())
        step_action.connect_proxy(toolbar.get_step())
        stepin_action.connect_proxy(toolbar.get_step_in())
        stepout_action.connect_proxy(toolbar.get_step_out())
        continue_action.connect_proxy(toolbar.get_continue_())
        run_action.connect_proxy(toolbar.get_run())
        exitdebug_action.connect_proxy(toolbar.get_exit_debug())

    def get_window(self):
        """
            Retorna: un gtk.Window o None.

            Devuelve la ventana del EditorDebugger
            o None si no tiene ninguna.
        """

        toplevel = self.get_toplevel()

        return toplevel if (type(toplevel) == gtk.Window) else None

    def on_window_state_event(self, p_window, p_event):
        """
            p_window: un gtk.Window.
            p_event:  un gtk.gdk.Event.

            Decide si la barra de estado del EditorDebugger
            muestra o no un grip.
            Si la ventana del EditorDebugger esta MAXIMIZED
            o FULLSCREEN entonces no se muestra el grip, en
            otro caso si.
        """

        window = self.get_window()

        assert (window and p_window == window)
        assert (type(p_event) == gtk.gdk.Event and
                p_event.type == gtk.gdk.WINDOW_STATE)

        bitwise_or = (gtk.gdk.WINDOW_STATE_MAXIMIZED |
                      gtk.gdk.WINDOW_STATE_FULLSCREEN)

        if p_event.changed_mask & bitwise_or:
            show = not (p_event.new_window_state & bitwise_or)
            self.__statusbar.set_has_resize_grip(show)

    def on_notebook_switch_page(self, p_notebook, p_gpointer, p_num):
        """
            p_notebook: un EditorNotebook.
            p_gpointer: un GPointer.
            p_num:      un entero que representa el indice
                        de la nueva pagina actual.

            Actualiza la apariencia del EditorDebugger de
            acuerdo con la nueva pagina activa.
        """

        assert (p_notebook == self.__notebook)
        assert (type(p_num) in (long, int))

        self.__curtab = p_notebook.get_nth_page(p_num)

        assert (self.__curtab)

        self.update_undo()
        self.update_redo()
        self.update_appearance()
        self.update_cursor_position_statusbar()
        self.update_overwrite_mode_statusbar()
        self.update_debug_run_action_group()
        self.update_debug_breakpoints_action_group()

    def on_notebook_page_added(self, p_notebook, p_tab, p_num):
        """
            p_notebook: un EditorNotebook.
            p_tab:      un EditorTab.
            p_num:      un entero que representa el indice de p_tab.

            Conecta algunas sennales a p_tab y al EditorDocument y al
            EditorView correspondientes a este.
            Si p_notebook solamente contiene a p_tab, es decir, si p_tab
            es la primera pagina, entonces se conecta la sennal "owner-change"
            al clipboard gtk.gdk.SELECTION_CLIPBOARD y se actualiza la
            apariencia del EditorDebugger.
        """

        assert (p_notebook == self.__notebook)
        assert (type(p_tab) == EditorTab and p_tab.get_parent() == p_notebook)
        assert (type(p_num) in (long, int) and
                p_notebook.get_nth_page(p_num) == p_tab)

        doc = p_tab.get_doc()
        view = p_tab.get_view()

        on_document_can_undo = lambda p_doc, p_can: self.update_undo()
        on_document_can_redo = lambda p_doc, p_can: self.update_redo()
        on_document_selection_changed = lambda p_doc, p_has: \
                                        self.update_appearance()
        on_document_cursor_moved = lambda p_doc, p_pos: \
                                   self.update_cursor_position_statusbar()

        on_view_toogle_overwrite = lambda p_view: \
                                   self.update_overwrite_mode_statusbar()

        p_tab.connect("octave_mode_toggled", self.on_tab_octave_mode_toggled)
        if p_tab.is_in_octave_mode():
            self.on_tab_octave_mode_toggled(p_tab, True)

        doc.connect("notify::can-undo", on_document_can_undo)
        doc.connect("notify::can-redo", on_document_can_redo)
        doc.connect("notify::has-selection", on_document_selection_changed)
        doc.connect("notify::cursor-position", on_document_cursor_moved)
        doc.connect("saving", self.on_document_saving)
        doc.connect("saved", self.on_document_saved)

        view.connect_after("toggle-overwrite", on_view_toogle_overwrite)
        view.connect_after("focus-in-event", self.on_view_focus_in_event,
                                                                   p_tab)

        if p_notebook.get_n_pages() == 1:
            clipboard = gtk.Window().get_clipboard(gtk.gdk.SELECTION_CLIPBOARD)

            on_clipboard_owner_change = lambda p_clip, p_event: \
                                        self.update_paste()

            self.__clipboard_handler_id = clipboard.connect("owner-change",
                                                 on_clipboard_owner_change)

            ###########################################################
            self.__curtab = p_tab  # FIXME: Debe haber una mejor forma
            self.update_paste()    #        de evitar el AssertionError
            ###########################################################

            file_menu = self.__mbar.get_file()
            file_menu.get_editor_save().set_sensitive(True)
            file_menu.get_editor_save_as().set_sensitive(True)
            self.__mbar.get_edit().get_select().set_sensitive(True)
            self.__toolbar.get_save().set_sensitive(True)

            self.__debug_opened_files_action_group.set_sensitive(True)

    def on_notebook_page_removed(self, p_notebook, p_tab, p_num):
        """
            p_notebook: un EditorNotebook.
            p_tab:      un EditorTab.
            p_num:      un entero que representa el indice de p_tab.

            Si p_notebook no tiene paginas, es decir, si p_tab era la
            ultima pagina, entonces se desconecta la sennal "owner-change"
            del clipboard gtk.gdk.SELECTION_CLIPBOARD y se actualiza la
            apariencia del EditorDebugger.
        """

        assert (p_notebook == self.__notebook)
        assert (type(p_tab) == EditorTab and not p_tab.get_parent())
        assert (type(p_num) in (long, int) and p_num >= 0)

        if not p_notebook.get_n_pages():
            self.__curtab = None

            clipboard = gtk.Window().get_clipboard(gtk.gdk.SELECTION_CLIPBOARD)
            clipboard.disconnect(self.__clipboard_handler_id)

            self.init_update()

    def on_notebook_tab_close_request(self, p_notebook, p_tab):
        """
            p_notebook: un EditorNotebook.
            p_tab:      un EditorTab.

            Se ejecuta cuando se solicita cerrar a p_tab.
            Llama el metodo EditorDebugger.close_tab(p_tab).
        """

        assert (p_notebook == self.__notebook)
        assert (type(p_tab) == EditorTab and p_tab.get_parent() == p_notebook)

        self.close_tab(p_tab)

    def on_tab_octave_mode_toggled(self, p_tab, p_octave_mode):
        if p_tab == self.__curtab:
            self.update_debug_run_action_group()

        completion = p_tab.get_view().get_completion()
        providers = self.__provider_controller.get_providers()

        if p_octave_mode:
            method = completion.add_provider
        else:
            method = completion.remove_provider

        for provider in providers:
            method(provider)

    def on_view_focus_in_event(self, p_view, p_event, p_tab):
        """
            p_view:  un EditorView.
            p_event: un gtk.gdk.Event.
            p_tab:   un EditorTab.

            Si el documento correspondiente a p_tab ha sido
            modificado externamente, entonces se le notifica
            al usuario por si desea recargarlo.
        """

        assert (type(p_tab) == EditorTab and
                p_tab.get_parent() == self.__notebook)
        assert (p_tab.get_view() == p_view)
        assert (type(p_event) == gtk.gdk.Event and
                p_event.type == gtk.gdk.FOCUS_CHANGE)

        doc = p_tab.get_doc()

        bitwise_or = (EditorTabState.EXTERNALLY_MODIFIED_NOTIFICATION |
                      EditorTabState.CLOSING)

        if not (p_tab.get_state() & bitwise_or) and \
           doc.get_ask() and \
           doc.was_externally_modified():  # FIXME: p_tab.__desync_with_breakpoints() ???

            p_tab.set_state(EditorTabState.EXTERNALLY_MODIFIED_NOTIFICATION |
                            p_tab.get_state())

            if doc.get_modified():
                msg = "has been externally modified.\nDo you want " \
                      "to drop your changes and reload the file?"
            else:
                msg = "has been externally modified.\nDo you want " \
                      "to reload the file?"

            window = self.get_window()

            dialog = Confirm(gtk.STOCK_DIALOG_WARNING,
                             "%s\n\n%s" %(doc.get_path(), msg),
                             "M-File:",
                             window)

            if dialog.run():
                doc.load(False, window)
            else:
                doc.set_ask(False)

            p_tab.set_state(EditorTabState.EXTERNALLY_MODIFIED_NOTIFICATION ^
                            p_tab.get_state())

    def on_document_saving(self, p_doc, p_path):
        """
            p_doc:  un EditorDocument.
            p_path: una cadena que representa la direccion
                    en donde se esta salvando p_doc.

            Muestra un mensaje en la barra de estado indicando
            que se esta salvando p_doc en la direccion p_path.
        """

        assert (type(p_doc) == EditorDocument)
        assert (type(p_path) == str and p_path)

        context_id = self.__flash_context_id
        msg = "Saving file '%s'..." %p_path

        self.__statusbar.flash_message(context_id, msg)

    def on_document_saved(self, p_doc):
        curtab = self.__curtab
        if not curtab:
            return
        if p_doc != curtab.get_doc():
            return
        self.update_debug_breakpoints_action_group()

    def on_document_loading(self, p_doc, p_path):
        """
            p_doc:  un EditorDocument.
            p_path: una cadena que representa la direccion
                    de donde se esta cargando p_doc.

            Muestra un mensaje en la barra de estado indicando
            que se esta cargando p_doc desde la direccion p_path.
        """

        assert (type(p_doc) == EditorDocument)
        assert (type(p_path) == str and p_path)

        context_id = self.__flash_context_id
        msg = "Loading file '%s'..." %p_path

        self.__statusbar.flash_message(context_id, msg)

    def on_conn_stopped_in_file(self, p_conn, p_file):
        notebook = self.__notebook
        num = notebook.find_doc_with_path(p_file)
        if num != -1:
            notebook.set_current_page(num)
            self.__curtab.get_view().grab_focus()

    def on_conn_state_changed(self, p_conn, p_state):
        group = self.__debug_steps_action_group

        if p_state == TerminalState.READY:
            group.set_sensitive(False)
        elif p_state == TerminalState.DEBUGGING:
            group.set_sensitive(True)

    def on_destroy(self, p_edebugger):
        conn = self.__mwindow.get_connection()
        id1 = self.__stopped_in_file_handler_id
        id2 = self.__state_changed_handler_id
        conn.disconnect(id1)
        conn.disconnect(id2)

    def detach(self):
        """
            Muestra al EditorDebugger fuera de la ventana principal
            de la aplicacion, es decir, que lo muestra en una nueva
            ventana.
        """

        # FIXME: Este metodo no se puede ejecutar despues de
        #        una llamada al metodo 'EditorDebugger.close'
        assert (self.__is_attach or not self.get_window())

        if self.__is_attach:
            # remove self y self.__mbar from MainWindow.
            # disconnect "window-state-event" from MainWindow.
            # quitar self.__debug_accel_group from MainWindow.
            pass

        self.get_children()[0].pack_start(self.__mbar, True)

        # FIXME: Analizar si poner win.set_transient_for(MainWindow),
        #        esto serviria para coger el icono desde MainWindow y
        #        no desde una foto si siempre el icono sera el mismo
        #        de MainWindow, por otra parte, sirve para decir que
        #        el editor no es una ventana independiente, sino que
        #        tiene un padre que seria MainWindow.
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,
                                                     "images", "logo.png"))
        win.set_icon_from_file(path)
        #win.set_default_size(600, 600)
        win.maximize()
        win.set_title("Editor")
        win.add(self)
        win.connect("window-state-event", self.on_window_state_event)
        win.connect("delete-event", lambda p_window, p_event:
                              True if self.close() else True)
        win.add_accel_group(self.__debug_accel_group)
        win.show_all()

        self.__is_attach = False

    def attach(self):
        """
            Empotra al EditorDebugger en la ventana principal
            de la aplicacion.
        """

        # FIXME: este metodo no se puede ejecutar despues de
        #        una llamada al metodo 'EditorDebugger.close'
        assert (not self.__is_attach)

        if self.get_window(): # Existe el editor y esta fuera.
            # remove self from self.get_window().
            # self.get_window().destroy().
            # remove self.__mbar from self.
            pass

        # add self to MainWindow.
        # connect "window-state-event" to MainWindow.
        # poner self.__debug_accel_group to MainWindow.
        self.__is_attach = True

    def is_attach(self):
        """
            Retorna: un boolean.

            Devuelve True si el EditorDebugger esta empotrado en la
            ventana principal de la aplicacion, False en otro caso.
        """

        return self.__is_attach

    def new_document(self, p_path=None, p_jump_to=True):
        """
            p_path:    None o una cadena que representa la direccion
                       de un fichero.
            p_jump_to: un boolean.

            Crea un nuevo documento.
            Si p_path es None se crea un documento vacio, sino se
            crea un documento con el contenido del fichero indicado
            por p_path.
            Si p_jump_to es True el nuevo documento se pone activo.
        """

        assert ((p_path == None) or (type(p_path) == str and p_path))
        assert (type(p_jump_to) == bool)

        notebook = self.__notebook

        if not p_path:
            num = self.__next_num
            name = "untitled" if (num == 1) else "untitled%s" %num
            self.__next_num += 1

        else:
            num = notebook.find_doc_with_path(p_path)
            if num != -1:
                if p_jump_to:
                    notebook.set_current_page(num)
                    self.__curtab.get_view().grab_focus()
                return
            name = os.path.basename(p_path)

        doc = EditorDocument(name, p_path)
        doc.connect("loading", self.on_document_loading)

        if not doc.load(True, self.get_window()):
            return

        tab = EditorTab(doc, self.__mwindow.get_connection())
        notebook.add_tab(tab, -1, p_jump_to)

    def open_document(self):
        """
            Muestra un dialogo para que el usuario indique
            los archivos a abrir.
        """

        curdir = self.__mwindow.get_cdirectory().get_path()

        assert (type(curdir) == str and curdir)

        paths = EditorOpenDialog(self.get_window(), curdir).run()

        if paths:
            for path in paths:
                self.new_document(path)

    def undo(self):
        """
            Deshace la ultima accion realizada en el documento actual.
        """

        if not self.__curtab:
            return

        view = self.__curtab.get_view()

        view.undo()
        view.grab_focus()

    def redo(self):
        """
            Rehace la ultima accion desecha en el documento actual.
        """

        if not self.__curtab:
            return

        view = self.__curtab.get_view()

        view.redo()
        view.grab_focus()

    def cut(self):
        """
            Corta el texto seleccionado en el documento actual.
        """

        if not self.__curtab:
            return

        view = self.__curtab.get_view()

        view.cut_clipboard()
        view.grab_focus()

    def copy(self):
        """
            Copia el texto seleccionado en el documento actual.
        """

        if not self.__curtab:
            return

        view = self.__curtab.get_view()

        view.copy_clipboard()
        view.grab_focus()

    def paste(self):
        """
            Pega el contenido del clipboard en el documento actual.
        """

        if not self.__curtab:
            return

        view = self.__curtab.get_view()

        view.paste_clipboard()
        view.grab_focus()

    def delete(self):
        """
            Elimina el texto seleccionado en el documento actual.
        """

        if not self.__curtab:
            return

        view = self.__curtab.get_view()

        view.delete_selection()
        view.grab_focus()

    def select_all(self):
        """
            Selecciona todo el texto en el documento actual.
        """

        if not self.__curtab:
            return

        view = self.__curtab.get_view()

        view.select_all()
        view.grab_focus()

    def init_update(self):
        """
            Actualiza la apariencia del EditorDebugger para
            cuando no hay ningun documento abierto.
        """

        assert (not self.__curtab)

        toolbar = self.__toolbar
        file_menu = self.__mbar.get_file()
        edit_menu = self.__mbar.get_edit()

        toolbar.get_save().set_sensitive(False)
        file_menu.get_editor_save().set_sensitive(False)
        file_menu.get_editor_save_as().set_sensitive(False)

        toolbar.get_cut().set_sensitive(False)
        edit_menu.get_cut().set_sensitive(False)

        toolbar.get_copy().set_sensitive(False)
        edit_menu.get_copy().set_sensitive(False)

        toolbar.get_paste().set_sensitive(False)
        edit_menu.get_paste().set_sensitive(False)

        toolbar.get_undo().set_sensitive(False)
        edit_menu.get_undo().set_sensitive(False)

        toolbar.get_redo().set_sensitive(False)
        edit_menu.get_redo().set_sensitive(False)

        edit_menu.get_delete().set_sensitive(False)
        edit_menu.get_select().set_sensitive(False)

        self.__statusbar.set_overwrite(None)
        self.__statusbar.set_cursor_position(None, None)

        self.__debug_run_action_group.set_sensitive(False)
        self.__debug_opened_files_action_group.set_sensitive(False)
        self.__debug_breakpoints_action_group.set_sensitive(False)

    def update_undo(self):
        """
            Actualiza la apariencia del EditorDebugger de
            acuerdo a si se puede o no realizar la operacion
            undo.
        """

        assert (self.__curtab)

        can_undo = self.__curtab.get_doc().can_undo()

        self.__toolbar.get_undo().set_sensitive(can_undo)
        self.__mbar.get_edit().get_undo().set_sensitive(can_undo)

    def update_redo(self):
        """
            Actualiza la apariencia del EditorDebugger de
            acuerdo a si se puede o no realizar la operacion
            redo.
        """

        assert (self.__curtab)

        can_redo = self.__curtab.get_doc().can_redo()

        self.__toolbar.get_redo().set_sensitive(can_redo)
        self.__mbar.get_edit().get_redo().set_sensitive(can_redo)

    def update_appearance(self):
        """
            Actualiza la apariencia del EditorDebugger de
            acuerdo a si se pueden o no realizar las operaciones
            cut, copy, delete.
        """

        assert (self.__curtab)

        toolbar = self.__toolbar
        edit_menu = self.__mbar.get_edit()
        has_selection = self.__curtab.get_doc().get_has_selection()

        toolbar.get_cut().set_sensitive(has_selection)
        edit_menu.get_cut().set_sensitive(has_selection)

        toolbar.get_copy().set_sensitive(has_selection)
        edit_menu.get_copy().set_sensitive(has_selection)

        edit_menu.get_delete().set_sensitive(has_selection)

    def update_paste(self):
        """
            Actualiza la apariencia del EditorDebugger de
            acuerdo a si se puede o no realizar la operacion
            paste.
        """

        assert (self.__curtab)

        def received_clipboard_text(p_clip, p_text, p_self):
            if p_self.__curtab:
                sens = bool(p_text)
                p_self.__mbar.get_edit().get_paste().set_sensitive(sens)
                p_self.__toolbar.get_paste().set_sensitive(sens)

        clipboard = gtk.Window().get_clipboard(gtk.gdk.SELECTION_CLIPBOARD)
        clipboard.request_text(received_clipboard_text, self)

    def update_cursor_position_statusbar(self):
        """
            Actualiza la barra de estado con la posicion del cursor.
        """

        tab = self.__curtab

        assert (tab)

        line, col = self.get_cursor_position(tab)
        self.__statusbar.set_cursor_position(line, col)

    def get_cursor_position(self, p_tab):
        doc = p_tab.get_doc()
        view = p_tab.get_view()

        iter_ = doc.get_iter_at_mark(doc.get_insert())
        line = iter_.get_line()
        col = 0

        start = doc.get_iter_at_line(line)
        tab_size = view.get_tab_width()

        while not start.equal(iter_):
            if start.get_char() == "\t":
                col += tab_size - (col  % tab_size)
            else:
                col += 1
            start.forward_char()

        return (line + 1, col + 1)

    def update_overwrite_mode_statusbar(self):
        """
            Actualiza la barra de estado con el modo de sobre-escritura.
        """

        assert (self.__curtab)

        ovr = self.__curtab.get_view().get_overwrite()
        self.__statusbar.set_overwrite(ovr)

    def update_debug_run_action_group(self):
        assert (self.__curtab)

        sens = self.__curtab.is_in_octave_mode()
        self.__debug_run_action_group.set_sensitive(sens)

    def update_debug_breakpoints_action_group(self):
        curtab = self.__curtab
        assert (curtab)

        sens = bool(curtab.is_in_octave_mode() and curtab.get_doc().get_path())
        self.__debug_breakpoints_action_group.set_sensitive(sens)

    def close_tab(self, p_tab):
        """
            p_tab:   un EditorTab.

            Retorna: True si se cerro p_tab, False en caso contrario.

            Trata de cerrar a p_tab.
        """

        assert (type(p_tab) == EditorTab)

        notebook = p_tab.get_parent()

        assert (notebook == self.__notebook)

        p_tab.set_state(EditorTabState.CLOSING | p_tab.get_state())

        if not p_tab.can_close():
            dialog = EditorCloseConfirmationDialog([p_tab], self.get_window())
            result = dialog.run()

            if result:
                close = self.save(p_tab)
            else:
                close = result != False

        else:
            close = True

        if close:
            notebook.remove_tab(p_tab)
        else:
            p_tab.set_state(EditorTabState.CLOSING ^ p_tab.get_state())

        return close

    def close_all_tabs(self):
        """
            Retorna: True si se cerraron todos los tabs,
                     False en caso contrario.

            Trata de cerrar a todos los tabs.
        """

        notebook = self.__notebook
        children = notebook.get_children()

        for tab in children:
            tab.set_state(EditorTabState.CLOSING | tab.get_state())

        tabs = notebook.get_tabs_of_unsaved_docs()

        if not tabs:
            notebook.remove_all_tabs()
            return True

        if len(tabs) == 1:
            notebook.set_current_page(notebook.page_num(tabs[0]))

        dialog = EditorCloseConfirmationDialog(tabs, self.get_window())
        result = dialog.run()

        if result == False:
            for tab in children:
                tab.set_state(EditorTabState.CLOSING ^ tab.get_state())
            return False

        if not result:
            notebook.remove_all_tabs()
            return True

        for tab in children:
            if tab not in result:
                notebook.remove_tab(tab)

        for tab in result:
            notebook.set_current_page(notebook.page_num(tab))
            if self.save(tab):
                notebook.remove_tab(tab)

        children = notebook.get_children()

        for tab in children:
            tab.set_state(EditorTabState.CLOSING ^ tab.get_state())

        return not children

    def close(self):
        """
            Retorna: True si se cerro el EditorDebugger,
                     False en caso contrario.

            Trata de cerrar el EditorDebugger.
        """

        window = self.get_window()

        assert (window)

        if self.close_all_tabs():

            if self.__is_attach:
                # remove self y self.__mbar from MainWindow.
                # disconnect "window-state-event" from MainWindow.
                self.destroy()
            else:
                window.destroy()

            return True

        return False

    def save(self, p_tab=None, p_path=None):
        """
            p_tab:   None o un EditorTab.
            p_path:  None o una cadena que representa la direccion
                     de un fichero.

            Retorna: True si se salvo, False en caso contrario.

            Trata de salvar a p_tab en el fichero indicado por p_path.
            Si p_tab es None la accion se realiza al EditorTab activo.
            Si p_path es None se utiliza la direccion del documento
            correspondiente a p_tab.
        """

        assert ((p_tab == None) or (type(p_tab) == EditorTab and
                                    p_tab.get_parent() == self.__notebook))
        assert ((p_path == None) or (type(p_path) == str and p_path))

        if not p_tab:
            p_tab = self.__curtab

            if not p_tab:
                return

        doc = p_tab.get_doc()
        doc_path = doc.get_path()
        p_path = doc_path if (not p_path) else p_path

        if not p_path:
            return self.save_as(p_tab)

        window = self.get_window()

        if not (p_tab.get_state() & EditorTabState.CLOSING) and \
           p_path == doc_path and \
           doc.was_externally_modified():

            msg = "has been externally modified.\nIf you save it, all " \
                  "the external changes could be lost. Save it anyway?"

            dialog = Confirm(gtk.STOCK_DIALOG_WARNING,
                             "%s\n\n%s" %(p_path, msg),
                             "Save to M-File:",
                             window)

            if not dialog.run():
                return False

        return doc.save(p_path, window)

    def save_as(self, p_tab=None):
        """
            p_tab:   None o un EditorTab.

            Retorna: True si se salvo, False en caso contrario.

            Muestra un dialogo al usuario para que indique la direccion
            donde salvar a p_tab.
            Llama el metodo EditorDebugger.save(p_tab, nueva_direccion).
            Si p_tab es None la accion se realiza al EditorTab activo.
        """

        assert ((p_tab == None) or (type(p_tab) == EditorTab and
                                    p_tab.get_parent() == self.__notebook))

        if not p_tab:
            p_tab = self.__curtab

            if not p_tab:
                return

        doc = p_tab.get_doc()
        path = doc.get_path()
        curname = doc.get_name()

        if path:
            curdir = os.path.dirname(path)
        else:
            curdir = self.__mwindow.get_cdirectory().get_path()
            curname += ".m"

        path = EditorSaveDialog(self.get_window(), curdir, curname).run()

        if path:
            return self.save(p_tab, path)
        return False

    def set_breakpoints(self, p_tab, p_lines, p_funcname=None):
        p_tab.set_breakpoints(p_lines, p_funcname)

    def clear_breakpoints(self, p_tab, p_lines=None, p_funcname=None):
        p_tab.clear_breakpoints(p_lines, p_funcname)

    def get_lines_with_breakpoints(self, p_tab):
        return p_tab.get_lines_with_breakpoints()

    def run(self, p_tab):
        assert (type(p_tab) == EditorTab and
                p_tab.get_parent() == self.__notebook)

        if not p_tab.is_in_octave_mode():
            return

        doc = p_tab.get_doc()

        if not doc.get_path() or doc.is_unsaved():
            primary_text = 'File "%s" is unsaved or was externally modified.' \
                            %doc.get_name()
            secundary_text = "To run this file you need saved it."

            dialog = gtk.MessageDialog(parent=self.get_window(),
                                        flags=gtk.DIALOG_MODAL,
                                        message_format=primary_text)

            dialog.format_secondary_text(secundary_text)

            img = gtk.Image()
            img.set_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
            img.set_alignment(0.5, 0.0)
            img.show()
            dialog.set_image(img)

            dialog.add_buttons("_Save and Run", 0, "_Cancel", 1)
            dialog.child.get_children()[-1].set_layout(gtk.BUTTONBOX_CENTER)
            dialog.set_default_response(0)

            response = dialog.run()
            dialog.destroy()

            if response != 0:
                return

            if not self.save(p_tab):
                return

            if not p_tab.is_in_octave_mode():
                return

        def on_runner_response_request(p_runner):
            parent = self.get_window()
            msg = "To run this file"
            dialog = EditorLoadPathDialog(parent, doc_path, msg)
            response = dialog.run()
            p_runner.set_data("response", response)

        doc_path = doc.get_path()
        funcname = os.path.splitext(doc.get_name())[0]
        runner = RunFile(p_funcname=funcname, p_file=doc_path)
        runner.connect("response_request", on_runner_response_request)
        self.__mwindow.get_connection().append_command(runner)

    def on_run_activate(self, p_action):
        #FIXME: documentacion

        if not self.__curtab:
            return

        self.run(self.__curtab)

    def on_set_clear_breakpoint_activate(self, p_action):
        #FIXME: documentacion

        curtab = self.__curtab

        if not curtab:
            return

        line = self.get_cursor_position(curtab)[0]
        breakpoints = self.get_lines_with_breakpoints(curtab)

        if line in breakpoints:
            self.clear_breakpoints(curtab, [line])
        else:
            self.set_breakpoints(curtab, [line])

    def on_clear_breakpoints_activate(self, p_action):
        #FIXME: documentacion

        if not self.__notebook.get_n_pages():
            return
        self.__notebook.foreach(self.clear_breakpoints)
