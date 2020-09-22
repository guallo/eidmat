import os
import gtk
import gobject
import gtksourceview2

from edebugger.editor_view import EditorView
from edebugger.editor_document import EditorDocument  # Solo para tipo.
from edebugger.ocompiler.source import SourceString
from edebugger.ocompiler.compiler import Compiler
from edebugger.ocompiler.visitor import FuncFileChecker, FoldingBlockChecker
from edebugger.twindows.editor_text_window import EditorTextWindow
from edebugger.twindows.editor_text_window_controller import EditorTextWindowController
from edebugger.twindows.editor_breakpoints_controller import EditorBreakpointsController
from edebugger.twindows.editor_arrows_controller import EditorArrowsController
from edebugger.twindows.editor_folding_controller import EditorFoldingController
from edebugger.editor_folding_block import EditorFoldingBlock, EditorFoldingBlockType, EditorFoldingBlockHolder, EditorFoldingBlockLabel
from edebugger.dialogs.editor_load_path_dialog import EditorLoadPathDialog
from cmds.check_breakpoints import CheckBreakpoints
from cmds.check_stack import CheckStack
from cmds.set_breakpoints import SetBreakpoints
from cmds.clear_breakpoints import ClearBreakpoints
from conn.connection import Connection  # Solo para tipo.


class EditorTabState:
    """
        Estados de un EditorTab.
    """

    # A partir de aqui ningun valor se puede repetir !!!
    NORMAL = 0  # Es necesario que sea 0

    # A partir de aqui dar valores que sean potencia de 2
    EXTERNALLY_MODIFIED_NOTIFICATION = 1
    CLOSING = 2

    LIMIT_VALUE = 4


class EditorTab(gtk.VBox):
    """
        Clase que representa un tab, el cual tiene
        asociado un EditorView y un EditorDocument.
    """

    __gsignals__ = {"tab_label_sync_request": (gobject.SIGNAL_RUN_LAST,
                                               gobject.TYPE_NONE,
                                               ()),
                    "parsed":                 (gobject.SIGNAL_RUN_LAST,
                                               gobject.TYPE_NONE,
                                               ()),
                    "octave_mode_toggled":    (gobject.SIGNAL_RUN_LAST,
                                               gobject.TYPE_NONE,
                                               (bool, ))
                    }

    def __init__(self, p_doc, p_conn):
        """
            p_doc:   un EditorDocument.
            p_conn:  una Connection.

            Retorna: un EditorTab.

            Crea un nuevo EditorTab.
        """

        assert (type(p_doc) == EditorDocument)
        assert (type(p_conn) == Connection)

        gtk.VBox.__init__(self, False, 0)

        self.__doc = p_doc
        self.__conn = p_conn
        self.__view = EditorView(p_doc)
        self.__state = EditorTabState.NORMAL
        self.__octave_env = False  # FIXME: debe ser un EditorTabState ???
        self.__synced = False  # FIXME: debe ser un EditorTabState ???
        self.__locked = True  # FIXME: debe ser un EditorTabState ???
        self.__breakpoints_changed_handler_id = None
        self.__stack_changed_handler_id = None
        self.__document_changed_handler_id = None
        self.__timeout_id = None
        self.__parse_result = None
        self.__breakpoints_map = {}
        self.__stack_map = {"positions": [], "current": False}
        self.__folding_map = EditorFoldingBlockHolder()

        scroll = gtk.ScrolledWindow(None, None)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.add(self.__view)

        self.pack_end(scroll, True, True, 0)

        active = not p_doc.get_path() or \
                 os.path.splitext(p_doc.get_name())[1] == ".m"
        self.__set_octave_enviroment(active)

        if self.__octave_env and p_doc.get_path():
            self.__sync_with_breakpoints(True)
            self.__sync_with_stack()

        p_doc.connect("name_changed", self.__on_document_name_changed)
        p_doc.connect("saved", self.__on_document_saved)
        p_doc.connect("loaded", self.__on_document_loaded)
        p_doc.connect("modified-changed", self.__on_document_modified_changed)
        p_doc.connect_after("insert-child-anchor", self.__on_document_insert_child_anchor)

        self.__view.connect("breakpoint_set_request", self.__on_view_breakpoint_set_request)
        self.__view.connect("breakpoint_clear_request", self.__on_view_breakpoint_clear_request)
        self.__view.connect("fold_toggle_request", self.__on_view_fold_toggle_request)

        # FIXME: No se esta emitiendo ya que hay alguien apuntandolo
        #        aun despues de que se cierre, creo que tiene que ver
        #        con EditorTabLabel, o no se si tenga que ver con algun
        #        'connect'.
        # OJO:   Cuidado con los gobject.GObject.set_data.
        self.connect("destroy", self.__on_destroy)
        self.connect("parsed", self.__on_parsed)

        self.show_all()

    def get_doc(self):
        """
            Retorna: un EditorDocument.

            Devuelve el documento asociado.
        """

        return self.__doc

    def get_view(self):
        """
            Retorna: un EditorView.

            Devuelve la vista del documento asociado.
        """

        return self.__view

    def get_state(self):
        """
            Retorna: un estado o combinacion de
                     estados de EditorTabState.

            Devuelve el estado del EditorTab.
        """

        return self.__state

    def set_state(self, p_state):
        """
            p_state: un estado o combinacion de estados
                     de EditorTabState.

            Establece a p_state como estado del EditorTab.
        """

        assert (type(p_state) in (int, long) and
                0 <= p_state < EditorTabState.LIMIT_VALUE)

        self.__state = p_state

    def can_close(self):
        """
            Retorna: un boolean.

            Devuelve True si el tab se puede cerrar sin que se pierdan
            los cambios del documento asociado, False en caso contrario.
        """

        return not self.__doc.is_unsaved()

    def __on_document_name_changed(self, p_doc, p_is_m):
        #FIXME: documentacion

        self.emit("tab_label_sync_request")
        self.__set_octave_enviroment(p_is_m)

    def is_in_octave_mode(self):
        return self.__octave_env

    def __set_octave_enviroment(self, p_active):
        #FIXME: documentacion

        doc = self.__doc
        view = self.__view
        octave_env = self.__octave_env

        if p_active and not octave_env:
            # Estableciendo lenguaje
            manager = gtksourceview2.LanguageManager()
            doc.set_language(manager.get_language("octave"))

            # Estableciendo indentado automatico
            view.set_auto_indent(True)

            # Mostrando breakpoints
            self.__set_show_breakpoints(True)

            # Mostrando arrows
            self.__set_show_arrows(True)

            # Mostrando folding
            self.__set_show_folding(True)

            # Parsear
            self.__document_changed_handler_id = doc.connect("changed",
                                            self.__on_document_changed)
            self.__timeout_add()

        elif not p_active and octave_env:
            # Quitando lenguaje
            doc.set_language(None)

            # Quitando indentado automatico
            view.set_auto_indent(False)

            # Ocultando breakpoints
            self.__set_show_breakpoints(False)

            # Ocultando arrows
            self.__set_show_arrows(False)

            # Ocultando folding
            self.__set_show_folding(False)

            # No parsear
            doc.disconnect(self.__document_changed_handler_id)
            self.__remove_timeout()
            self.__parse_result = None

        if octave_env != p_active:
            self.__octave_env = p_active
            self.__update_locked()
            self.emit("octave_mode_toggled", p_active)

    def __update_locked(self):
        if self.__octave_env and self.__doc.get_path():  # FIXME: creo que todas las condiciones
                                                         #        como esta deben ser cambiadas
                                                         #        por 'if not self.__locked:'
            self.__locked = False
        else:
            self.__locked = True

        self.__update_breakpoints_bar(False, False, True)

    def __set_show_breakpoints(self, p_show):
        #FIXME: documentacion

        view = self.__view
        holder = view.get_window_holder()
        exist = holder.exist_window_of_name("Breakpoints")

        if p_show and not exist:
            # Separador
            win = EditorTextWindow("Separator", gtk.TEXT_WINDOW_LEFT,
                                0.5, 1, gtk.gdk.Color("#FFFFFF"), [])
            ctrl = EditorTextWindowController(gtk.gdk.EXPOSURE_MASK)
            holder.append(win, ctrl)

            win = EditorTextWindow("Breakpoints", gtk.TEXT_WINDOW_LEFT,
                                    1, 1, gtk.gdk.Color("#EFEBE7"), [])
            ctrl = EditorBreakpointsController(win, view)
            holder.append(win, ctrl)
            self.__update_breakpoints_bar()
        elif not p_show and exist:
            # Separador
            win = holder.get_window_of_name("Separator")[0]
            holder.remove(win)

            win = holder.get_window_of_name("Breakpoints")[0]
            holder.remove(win)
            view.update_window(win.get_type())

    def __set_show_arrows(self, p_show):
        #FIXME: documentacion

        view = self.__view
        holder = view.get_window_holder()
        exist = holder.exist_window_of_name("Stack")

        if p_show and not exist:
            win = EditorTextWindow("Stack", gtk.TEXT_WINDOW_LEFT,
                                    2, 1, gtk.gdk.Color("#FFFFFF"), [])
            ctrl = EditorArrowsController(win, view)
            holder.append(win, ctrl)
            self.__update_stack_bar()
        elif not p_show and exist:
            win = holder.get_window_of_name("Stack")[0]
            holder.remove(win)
            view.update_window(win.get_type())

    def __set_show_folding(self, p_show):
        #FIXME: documentacion

        view = self.__view
        holder = view.get_window_holder()
        exist = holder.exist_window_of_name("Folding")

        if p_show and not exist:
            win = EditorTextWindow("Folding", gtk.TEXT_WINDOW_LEFT,
                                    3, 1, gtk.gdk.Color("#FFFFFF"), [])
            ctrl = EditorFoldingController(self.__folding_map, win, view)
            holder.append(win, ctrl)
            self.__update_folding_bar()
        elif not p_show and exist:
            win = holder.get_window_of_name("Folding")[0]
            holder.remove(win)
            view.update_window(win.get_type())

    def __on_document_saved(self, p_doc):
        if self.__octave_env:
            self.__sync_with_breakpoints(False)
            self.__sync_with_stack()
        else:
            if self.__synced:
                self.__desync_with_breakpoints()
            self.__desync_with_stack()

        self.__update_locked()

    def __on_document_loaded(self, p_doc):
        if self.__octave_env:
            self.__sync_with_breakpoints(True)

    def __on_document_modified_changed(self, p_doc):
        self.emit("tab_label_sync_request")

        if self.__octave_env and p_doc.get_path():
            if p_doc.get_modified():
                self.__desync_with_breakpoints()
            else:
                self.__sync_with_breakpoints(False)

    def __on_conn_breakpoints_changed(self, p_conn, p_data):
        doc = self.__doc

        if doc.was_externally_modified() or doc.was_deleted():  # FIXME: notificar al usuario ???
            self.__desync_with_breakpoints()
        else:
            dbstatus = p_data.get_data("breakpoints")
            file_ = doc.get_path()
            known = []

            for status in dbstatus:
                if status["file"] == file_:
                    function = status["function"]
                    lines = status["lines"]

                    known.append(function)
                    self.__update_breakpoints_of_function(function, lines)
            if known:
                self.__update_breakpoints_bar(True, False, False)

            def on_tab_parsed(p_tab=None, p_synced_counter=None):
                if p_tab:
                    self.disconnect(self.get_data(key_id))
                    self.set_data(key_id, None)

                    if not self.__synced or self.get_data(key) != counter or \
                        self.get_data("__sync_with_breakpoints") != p_synced_counter:  # FIXME: no falta ni sobra ???
                        return

                for funcname in self.get_funcnames():
                    function = funcname[1] if funcname[1] else funcname[0]

                    if function not in known:
                        self.__check_breakpoints_of_function(funcname)

            key = "__on_conn_breakpoints_changed"
            counter = self.get_data(key)
            counter = counter + 1 if counter else 1
            self.set_data(key, counter)

            if self.__timeout_id != None:
                id_ = self.connect("parsed", on_tab_parsed, self.get_data("__sync_with_breakpoints"))
                key_id = key + str(counter)
                self.set_data(key_id, id_)
            else:
                on_tab_parsed()

    def __on_conn_stack_changed(self, p_conn, p_data):
        if "is patch for Octave-3.2.3":
            dbwhere = p_data.get_data("where")
            file_ = self.__doc.get_path()
            positions = []
            current = False

            if dbwhere and dbwhere["file"] == file_:
                pos = (dbwhere["line"], dbwhere["column"])

                if None not in pos:
                    positions.append(pos)
                    current = True

            self.__update_stack(positions, current)
            self.__update_stack_bar()
            return

        dbstack = p_data.get_data("stack")
        file_ = self.__doc.get_path()

        positions = []
        frames = dbstack["frames"]
        current = bool(frames and frames[0]["file"] == file_)
        for frame in frames:
            if frame["file"] == file_:
                positions.append((frame["line"], frame["column"]))

        self.__update_stack(positions, current)
        self.__update_stack_bar()

    def __check_breakpoints_of_function(self, p_funcname):
        doc = self.__doc

        def on_breakpoints_update_request(p_checker, p_data):
            if not self.__synced:  # FIXME: no falta ni sobra ??? counter ??? doc.get_path() no ha cambiado ???
                return

            function = p_data.get_data("function")
            lines = p_data.get_data("lines")
            self.__update_breakpoints_of_function(function, lines)
            self.__update_breakpoints_bar(True, False, False)

        checker = CheckBreakpoints(p_funcname, doc.get_name(), doc.get_path())
        checker.connect("breakpoints_update_request", on_breakpoints_update_request)
        self.__conn.append_command(checker)

    def __check_stack(self):
        if "is patch for Octave-3.2.3":
            def on_stack_update_request(p_checker, p_data):
                if self.__doc.get_path() != doc_path:
                    return

                positions = p_data.get_data("positions")
                current = p_data.get_data("current")
                self.__update_stack(positions, current)
                self.__update_stack_bar()

            doc_path = self.__doc.get_path()
            checker = CheckStack(doc_path)
            checker.connect("stack_update_request", on_stack_update_request)
            self.__conn.append_command(checker)
            return

        def on_stack_update_request(p_checker, p_data):
            if self.__doc.get_path() != doc_path:
                return

            positions = p_data.get_data("positions")
            current = p_data.get_data("current")
            self.__update_stack(positions, current)
            self.__update_stack_bar()

        doc_path = self.__doc.get_path()
        checker = CheckStack(doc_path)
        checker.connect("stack_update_request", on_stack_update_request)
        self.__conn.append_command(checker)

    def get_lines_with_breakpoints(self):
        breakpoints = []

        for lines in self.__breakpoints_map.itervalues():
            for num in lines:
                if num not in breakpoints:
                    breakpoints.append(num)

        return breakpoints

    def get_lines_with_arrows(self):
        arrows = []

        for (line, column) in self.__stack_map["positions"]:
            if line not in arrows:
                arrows.append(line)

        return arrows

    def __update_breakpoints_of_function(self, p_funcname, p_lines):
        breakpoints_map = self.__breakpoints_map

        if p_lines:
            breakpoints_map[p_funcname] = p_lines
        elif p_funcname in breakpoints_map:
            del breakpoints_map[p_funcname]

    def __update_stack(self, p_positions, p_current):
        self.__stack_map["positions"] = p_positions
        self.__stack_map["current"] = p_current

        if p_current:
            line = p_positions[0][0]
            iter_ = self.__doc.get_iter_at_line(line - 1)
            self.__doc.place_cursor(iter_)
            self.__view.scroll_to_cursor()

    def get_funcnames(self):
        parse_result = self.__parse_result

        if not parse_result:
            return None

        docname = os.path.splitext(self.__doc.get_name())[0]
        funcnames = [func["function"] for func in parse_result["functions"]]

        if parse_result["ast"].is_script:
            funcnames = [(docname, None)]
        elif funcnames:
            funcnames[0] = (docname, None)
            for pos in xrange(1, len(funcnames)):
                funcnames[pos] = (docname, funcnames[pos])

        return funcnames

    def __sync_with_breakpoints(self, p_check):
        key = "__sync_with_breakpoints"
        counter = self.get_data(key)
        counter = counter + 1 if counter else 1
        self.set_data(key, counter)

        conn = self.__conn
        if self.__breakpoints_changed_handler_id == None:
            self.__breakpoints_changed_handler_id = conn.connect(
                "breakpoints_changed", self.__on_conn_breakpoints_changed)
            self.__synced = True

        lines = self.get_lines_with_breakpoints()
        self.__breakpoints_map.clear()
        self.__update_breakpoints_bar(True, True, False)

        if not p_check:
            self.clear_breakpoints()
            if lines:
                self.set_breakpoints(lines)

        def on_tab_parsed(p_tab=None):
            if p_tab:
                self.disconnect(self.get_data(key_id))
                self.set_data(key_id, None)

                if not self.__synced or self.get_data(key) != counter:  # FIXME: no falta ni sobra ???
                    return

            for funcname in self.get_funcnames():
                self.__check_breakpoints_of_function(funcname)

        if self.__timeout_id != None:
            id_ = self.connect("parsed", on_tab_parsed)
            key_id = key + str(counter)
            self.set_data(key_id, id_)
        else:
            on_tab_parsed()

    def __sync_with_stack(self):
        if "is patch for Octave-3.2.3":
            conn = self.__conn
            if self.__stack_changed_handler_id == None:
                id_ = conn.connect("where_changed", self.__on_conn_stack_changed)
                self.__stack_changed_handler_id = id_

            self.__update_stack([], False)
            self.__update_stack_bar()

            self.__check_stack()
            return

        conn = self.__conn
        if self.__stack_changed_handler_id == None:
            id_ = conn.connect("stack_changed", self.__on_conn_stack_changed)
            self.__stack_changed_handler_id = id_

        self.__update_stack([], False)
        self.__update_stack_bar()

        self.__check_stack()

    def __desync_with_breakpoints(self):
        self.__disconnect_breakpoints_changed_handler()
        self.__synced = False
        self.__update_breakpoints_bar(False, True, False)

    def __desync_with_stack(self):
        self.__disconnect_stack_changed_handler()
        self.__update_stack([], False)
        self.__update_stack_bar()

    def __on_view_breakpoint_set_request(self, p_view, p_line):
        self.set_breakpoints([p_line])

    def __on_view_breakpoint_clear_request(self, p_view, p_line):
        self.clear_breakpoints([p_line])

    def delimit_document_by_functions(self):
        parse_result = self.__parse_result

        if not parse_result:
            return None

        doc = self.__doc
        docname = os.path.splitext(doc.get_name())[0]
        last_line = doc.get_line_count()
        functions = parse_result["functions"]
        segments = []

        if parse_result["ast"].is_script or len(functions) == 1:
            segments.append({"funcname": (docname, None),
                             "start": 1,
                             "end": last_line})

        elif functions:  # len(functions) >= 2
            segments.append({"funcname": (docname, None),
                             "start": 1,
                             "end": functions[0]["end"]})

            for func in functions[1 : -1]:
                segments.append({"funcname": (docname, func["function"]),
                                 "start": func["start"],
                                 "end": func["end"]})

            segments.append({"funcname": (docname, functions[-1]["function"]),
                             "start": functions[-1]["start"],
                             "end": last_line})

        return segments

    def get_functions_with_lines(self, p_lines, p_top_down=False, p_all=False):
        segments = self.delimit_document_by_functions()

        if segments == None:
            return None

        def add_pair(p_funcname, p_line):
            exist = False

            for pair in pairs:
                if pair["funcname"] == p_funcname:
                    if p_line not in pair["lines"]:
                        pair["lines"].append(p_line)

                    exist = True
                    break

            if not exist:
                pairs.append({"funcname": p_funcname, "lines": [p_line]})

        pairs = []

        if not p_top_down:
            segments.reverse()

        for line in p_lines:
            for segment in segments:
                if segment["start"] <= line <= segment["end"]:
                    add_pair(segment["funcname"], line)

                    if not p_all:
                        break

        return pairs

    def set_breakpoints(self, p_lines, p_funcname=None):
        doc_path = self.__doc.get_path()

        if not self.__octave_env or not doc_path:
            return

        if not self.__synced:
            funcname = "unknown_function"
            lines = self.__breakpoints_map.get(funcname, [])[:]
            lines.extend(p_lines)
            self.__update_breakpoints_of_function(funcname, lines)
            self.__update_breakpoints_bar(True, False, False)
            return

        def on_setter_response_request(p_setter):
            toplevel = self.get_toplevel()
            parent = toplevel if isinstance(toplevel, gtk.Window) else None
            msg = "To set breakpoints in this file"
            dialog = EditorLoadPathDialog(parent, doc_path, msg)
            response = dialog.run()
            p_setter.set_data("response", response)

        def set_breakpoints(p_lines, p_funcname):
            setter = SetBreakpoints(p_lines, p_funcname, doc_path)
            setter.connect("response_request", on_setter_response_request)
            self.__conn.append_command(setter)

        if p_funcname:
            set_breakpoints(p_lines, p_funcname)
            return

        def on_tab_parsed(p_tab=None):
            if p_tab:
                self.disconnect(self.get_data(key_id))
                self.set_data(key_id, None)

            for pair in self.get_functions_with_lines(p_lines):
                set_breakpoints(pair["lines"], pair["funcname"])

        if self.__timeout_id != None:
            id_ = self.connect("parsed", on_tab_parsed)
            key = "set_breakpoints:on_tab_parsed"
            counter = self.get_data(key)
            counter = counter + 1 if counter else 1
            key_id = key + str(counter)
            self.set_data(key, counter)
            self.set_data(key_id, id_)
        else:
            on_tab_parsed()

    def clear_breakpoints(self, p_lines=None, p_funcname=None):
        doc_path = self.__doc.get_path()

        if not self.__octave_env or not doc_path:
            return

        if not self.__synced:
            if p_lines:
                for (funcname, lines) in self.__breakpoints_map.items():
                    lines = lines[:]
                    pos = 0
                    while pos < len(lines):
                        if lines[pos] in p_lines:
                            del lines[pos]
                        else:
                            pos += 1
                    self.__update_breakpoints_of_function(funcname, lines)
            else:
                self.__breakpoints_map.clear()
            self.__update_breakpoints_bar(True, False, False)
            return

        def clear_breakpoints(p_funcname, p_lines=None):
            cleaner = ClearBreakpoints(p_funcname, p_lines, doc_path)
            self.__conn.append_command(cleaner)

        if p_funcname:
            clear_breakpoints(p_funcname, p_lines)
            return

        def on_tab_parsed(p_tab=None):
            if p_tab:
                self.disconnect(self.get_data(key_id))
                self.set_data(key_id, None)

            if p_lines:
                for pair in self.get_functions_with_lines(p_lines):
                    clear_breakpoints(pair["funcname"], pair["lines"])
            else:
                for funcname in self.get_funcnames():
                    clear_breakpoints(funcname)

        if self.__timeout_id != None:
            id_ = self.connect("parsed", on_tab_parsed)
            key = "clear_breakpoints:on_tab_parsed"
            counter = self.get_data(key)
            counter = counter + 1 if counter else 1
            key_id = key + str(counter)
            self.set_data(key, counter)
            self.set_data(key_id, id_)
        else:
            on_tab_parsed()

    def __update_breakpoints_bar(self, p_lines=True, p_synced=True, p_locked=True):
        view = self.__view
        holder = view.get_window_holder()
        exist = holder.exist_window_of_name("Breakpoints")

        if exist:
            win, ctrl = holder.get_window_of_name("Breakpoints")
            if p_lines:
                ctrl.set_lines(self.get_lines_with_breakpoints())
            if p_synced:
                ctrl.set_synced(self.__synced)
            if p_locked:
                ctrl.set_locked(self.__locked)
            view.update_window(win.get_type())

    def __update_stack_bar(self, p_lines=True, p_current=True):
        view = self.__view
        holder = view.get_window_holder()
        exist = holder.exist_window_of_name("Stack")

        if exist:
            win, ctrl = holder.get_window_of_name("Stack")
            if p_lines:
                ctrl.set_lines(self.get_lines_with_arrows())
            if p_current:
                ctrl.set_current(self.__stack_map["current"])
            view.update_window(win.get_type())

    def __parse(self):
        anchor = unicode("\xef\xbf\xbc", "utf-8")
        text = unicode(self.__doc.get_all_slice(), "utf-8").replace(anchor, " ")

        source = SourceString(text)
        compiler = Compiler(source)

        symtab = compiler.symtab
        ast = compiler.compile()

        checker = FuncFileChecker(ast, symtab)
        functions = checker.check()

        self.__parse_result = {"ast": ast,
                               "symtab": symtab,
                               "functions": functions}
        self.emit("parsed")

    def __on_document_changed(self, p_doc):
        # OJO: En este metodo no se puede agregar mas nada
        #      ya que se deja de llamar cuando algun Fold
        #      se cierra o se abre.

        self.__timeout_add()

    def __timeout_add(self):
        def parse():
            self.__parse()
            self.__timeout_id = None
            return False

        self.__remove_timeout()
        self.__timeout_id = gobject.timeout_add(750, parse)

    def __update_folding(self):
        parse_result = self.__parse_result
        folding_map = self.__folding_map
        doc = self.__doc

        if not self.__octave_env or not self.__parse_result:
            return

        ast = parse_result["ast"]
        symtab = parse_result["symtab"]
        checker = FoldingBlockChecker(ast, symtab)

        # 1) New Tree
        holder = checker.check()

        blocks = holder.get_blocks_in_pre_order()
        collapsed = folding_map.get_collapsed_blocks()

        # 2) Merge Collapsed and Install
        for block in blocks:
            offset1, offset2, offset3 = block.get_initial_offsets()
            if offset2 == None:
                iter1 = doc.get_iter_at_offset(offset1)
                iter1.forward_to_line_end()
                offset2 = iter1.get_offset()
                block.set_offset2(offset2)
            else:##
                offset2 += 1##
            iter3 = doc.get_iter_at_offset(offset3)
            iter3.forward_line()
            offset3 = iter3.get_offset()
            block.set_offset3(offset3)
            block.set_doc(doc)
            if self.__document_changed_handler_id != None:
                block.get_handler_ids().append(self.__document_changed_handler_id)
            pos = 0
            while pos < len(collapsed):
                old_block = collapsed[pos]
                old_offset1, old_offset2, old_offset3 = old_block.get_offsets()
                if offset1 == old_offset1 and offset2 == old_offset2 and\
                                                offset3 == old_offset3:
                    old_block.uninstall()##
                    offset2 -= 1##
                    offset3 -= 1##
                    block.set_offset2(offset2)##
                    block.set_offset3(offset3)##
                    block.collapse()
                    del collapsed[pos]
                    break
                pos += 1
            else:##
                block.expand()##
            block.install()

        # 3) Remove Old Tree
        folding_map.uninstall_all_blocks()
        del folding_map[:]

        # 4) Set New Tree
        folding_map.extend(holder)

        self.__update_folding_bar()

    def __update_folding_bar(self):
        view = self.__view
        holder = view.get_window_holder()
        exist = holder.exist_window_of_name("Folding")

        if exist:
            win, ctrl = holder.get_window_of_name("Folding")
            view.update_window(win.get_type())

    def toggle_fold(self, p_line, p_top_level=False, p_top_down=False):
        holder = self.__folding_map
        block = holder.get_block_of_line(p_line - 1, p_top_level, p_top_down)
        if not block:
            return
        if block.is_collapsed():
            block.expand()
        else:
            block.collapse()
        self.__update_folding_bar()###################################################################################################################
        #######################################################################print block.get_offsets(), "--", self.__doc.get_end_iter().get_offset()

    def __on_view_fold_toggle_request(self, p_view, p_line):
        self.toggle_fold(p_line)

    def __on_parsed(self, p_tab):
        self.__update_folding()

    def __on_document_insert_child_anchor(self, p_doc, p_iter, p_anchor):
        label = EditorFoldingBlockLabel("...", self.__view)
        label.show_all()
        self.__view.add_child_at_anchor(label, p_anchor)

    def __on_destroy(self, p_tab):
        self.__remove_timeout()
        self.__disconnect_breakpoints_changed_handler()
        self.__disconnect_stack_changed_handler()
        # FIXME: desconectar "breakpoints_update_request"
        # FIXME: desconectar "stack_update_request"
        #        ver que mas hay que desconectar, que si hay mas

    def __disconnect_breakpoints_changed_handler(self):
        conn = self.__conn
        id_ = self.__breakpoints_changed_handler_id

        if id_ != None:
            conn.disconnect(id_)
            self.__breakpoints_changed_handler_id = None

    def __disconnect_stack_changed_handler(self):
        conn = self.__conn
        id_ = self.__stack_changed_handler_id

        if id_ != None:
            conn.disconnect(id_)
            self.__stack_changed_handler_id = None

    def __remove_timeout(self):
        if self.__timeout_id != None:
            gobject.source_remove(self.__timeout_id)
            self.__timeout_id = None
