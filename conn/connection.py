import os
import re
import gtk
import time
import gobject
import threading

from util.tail_with_priority import TailWithPriority
from util.constants import PS1, PS2, PS3, VAR
from util.data import Data
from conn.terminal import Terminal, TerminalState


class Connection(threading.Thread, gobject.GObject):
    """
        Establece la conexion con 'Octave'. Es a traves de esta clase que nos
        podemos comunicar con 'Octave'.
    """
    __gsignals__ = {"state_changed":          (gobject.SIGNAL_RUN_LAST,
                                               gobject.TYPE_NONE,
                                               (int, )),
                    "breakpoints_changed":    (gobject.SIGNAL_RUN_LAST,
                                               gobject.TYPE_NONE,
                                               (Data, )),
                    "where_changed":          (gobject.SIGNAL_RUN_LAST,
                                               gobject.TYPE_NONE,
                                               (Data, )),
                    "stack_changed":          (gobject.SIGNAL_RUN_LAST,
                                               gobject.TYPE_NONE,
                                               (Data, )),
                    "stopped_in_file":        (gobject.SIGNAL_RUN_LAST,
                                               gobject.TYPE_NONE,
                                               (str, )),
                    "changed":                (gobject.SIGNAL_RUN_LAST,
                                               gobject.TYPE_NONE,
                                               (Data, ))
                   }

    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   una 'Connection'.

            Crea una nueva 'Connection'.
        """
        threading.Thread.__init__(self)
        gobject.GObject.__init__(self)

        self.__mwindow = p_mwindow
        self.__continue = True
        self.__term = Terminal(self)

        # Aqui se almacenan los comandos
        # que envia el usuario a octave.
        self.__tail = []

        # Aqui se almacenan los comandos que se
        # ejecutaran cuando el octave este listo.
        self.__tail_prio = TailWithPriority()

        self.__dbstatus_code = self.__get_dbstatus_code()
        self.__dbstack_code = self.__get_dbstack_code()

        self.__prestate = None
        self.__predbstack = None
        self.__predbwhere = None
        self.__predbstatus = None
        self.__predir = None
        #self.__prevars = None# para emitir un "vars_changed"

        flag = Data()
        key = "key"
        self.connect("changed", self.__on_changed, flag, key)
        self.connect("stack_changed", self.__on_stack_changed, flag, key)
        self.connect("where_changed", self.__on_where_changed, flag, key)

    def __get_dbstatus_code(self):
        path = os.path.join(os.path.dirname(__file__), "dbstatus.m")

        file_ = open(path, "r")
        code = file_.read().strip()
        file_.close()

        replacer = lambda match: {"mainstruct": VAR,
                                  "pos": "%s1" %VAR,
                                  "substrct": "%s2" %VAR,
                                  os.linesep: ""
                                 }[match.group()]

        pattern = re.compile("(mainstruct|pos|substrct|%s)" %os.linesep)
        code = re.sub(pattern, replacer, code)

        return code + os.linesep

    def __get_dbstack_code(self):
        path = os.path.join(os.path.dirname(__file__), "dbstack.m")

        file_ = open(path, "r")
        code = file_.read().strip()
        file_.close()

        replacer = lambda match: {"mainstruct": VAR,
                                  "III": "%s1" %VAR,
                                  "pos": "%s2" %VAR,
                                  "substrct": "%s3" %VAR,
                                  os.linesep: ""
                                 }[match.group()]

        pattern = re.compile("(mainstruct|III|pos|substrct|%s)" %os.linesep)
        code = re.sub(pattern, replacer, code)

        return code + os.linesep

    def get_mwindow(self):
        """
            Retorna: un 'MainWindow'.

            Retorna el objeto que modela la ventana principal de la aplicacion.
        """
        return self.__mwindow

    def get_terminal(self):
        """
            Retorna: una 'Terminal'.

            Retorna la terminal virtual en la que se ejecuta 'Octave'.
        """
        return self.__term

    def get_state(self):
        return self.__prestate

    def get_tail_with_priority(self):
        """
            Retorna: una 'TailWithPriority'.

            Retorna la cola con prioridad que almacena aquellos comandos
            ('Command') que  seran enviados a 'Octave' solo cuando este listo.
            Por ejemplo: cuando un usuario crea una nueva variable a traves de
            las funcionalidades del 'Workspace', lo que se hace es que se
            encola el comando('Command') correspondiente para realizar esto en
            la cola con prioridad('TailWithPriority').
        """
        return self.__tail_prio

    def _init_oct(self):
        """
            Metodo auxiliar para inicializar 'Octave'. Aqui se cambia el
            'PS1'(prompt 1) y el 'PS2'(prompt 2) a una combinacion de
            caracteres extrannos con el objetivo de poder determinar en
            cualquier momento el estado de 'Octave'. Tambien se adiciona
            al 'path' de 'Octave' la direccion de la carpeta que contiene
            todos los '*.m' que utiliza la aplicacion.
        """
        term = self.__term
        buff = term.buff
        m = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, "m"))

        term.feed_child("addpath (genpath ('%s'), '-begin');" \
                        "if (exist ('OCTAVE_VERSION') == 5);" \
                        "PS1 ('%s');"                         \
                        "PS2 ('%s');"                         \
                        "else;"                               \
                        "PS1 = '%s';"                         \
                        "PS2 = '%s';"                         \
                        "endif;\n" %(m, PS1, PS2, PS1, PS2)
                        )

        pattern = re.compile("[^']%s\Z" %PS1)

        while True:
            end = buff.get_char_count()
            text = buff.get_text(0, end, True)

            if re.search(pattern, text):
                buff.delete(0, end - len(PS1))
                return

            time.sleep(0.001)

    def write(self, p_text):
        """
            p_text: una cadena que representa un comando para enviarle
                    a 'Octave'.

            Adiciona 'p_text' a la cola de comandos para ser enviado
            inmediatamente a 'Octave'. Por ejemplo: cuando el usuario
            escribe algun comando en el 'CommnadWindow' y da 'Enter',
            lo que se hace es llamar este metodo pasando a dicho comando
            como parametro.
        """
        self.__tail.append(p_text)

    def append_command(self, p_cmd):
        """
            p_cmd: un 'Command'.

            Adiciona 'p_cmd' a la cola con prioridad('TailWithPriority') para
            ser ejecutado cuando 'Octave' este listo. Por ejemplo: cuando un
            usuario crea una nueva variable a traves de las funcionalidades del
            'Workspace', lo que se hace es crear una instancia de la clase
            'NewVar' y llamar el metodo 'Connection.append_command' pasandole
            dicho objeto como parametro.
        """
        self.__tail_prio.append(p_cmd)

    def stop(self):
        """
            Pone el atributo 'Connection.__continue' en 'False' lo que provoca
            que se termine el ciclo principal de la 'Connection' terminando asi
            la comunicacion con 'Octave'.
        """
        self.__continue = False

    def run(self):
        """
            Este metodo es el que mantiene mediante un ciclo principal la
            comunicacion con 'Octave', el mismo se ejecuta en un hilo diferente
            del hilo en el que corre la aplicacion. Se encarga de enviar los
            comandos a 'Octave' y de mostrar su salida en el 'CommandWindow'.
        """
        tail = self.__tail
        tail_prio = self.__tail_prio
        term = self.__term
        buff = term.buff
        sent, pass_ = True, False
        bitwise_2or = TerminalState.READY | TerminalState.DEBUGGING
        bitwise_3or = bitwise_2or | TerminalState.WAITING_FOR_COMPLETE_STATMENT

        self._init_oct()

        while self.__continue:
            if tail:
                term.feed_child(tail.pop(0))
                sent, pass_ = True, False

            time.sleep(0.001)
            text = buff.get_all()
            if text:
                self._print(text)
                count, pass_ = 0, True

            if term.state_ & bitwise_3or and pass_ and not buff.get_char_count():
                count += 1
                if count > 29:
                    self._check_state(term.state_)

                    if term.state_ & bitwise_2or:
                        not_clean = False

                        while not tail_prio.is_empty():
                            not_clean = bool(tail_prio.extract().execute(self))
                            sent = True
                            if not_clean:
                                break

                        if not_clean:
                            pass_ = False

                        elif sent:
                            curdir = self.get_curdir()
                            vars_ = self.get_vars()
                            curdbstatus = self.dbstatus()
                            curdbstack = self.dbstack()
                            curdbwhere = self.dbwhere() if curdbstack["frames"] else {}

                            # Tiene que ser el primero.
                            data = Data()
                            data.set_data("curdir", curdir)
                            data.set_data("vars", vars_)
                            data.set_data("breakpoints", curdbstatus)
                            data.set_data("stack", curdbstack)
                            data.set_data("where", curdbwhere)
                            self.emit_("changed", data)

                            self._check_dir(curdir)
                            self._check_vars(vars_)
                            self._check_dbstatus(curdbstatus)
                            self._check_dbstack(curdbstack)
                            self._check_dbwhere(curdbwhere)

                            sent = False
                    else:  # TerminalState.WAITING_FOR_COMPLETE_STATMENT
                        pass

                    count = 30
                    continue
            self._check_state(TerminalState.BUSY)

        # FIXME: CREO que deberia encerrarse entre
        #        gtk.gdk.threads_enter() y gtk.gdk.threads_leave()
        self.__mwindow.close_now()  # Cerramos la aplicacion.

    def wait_until_ready(self):
        """
            Espera hasta que 'Octave' este listo.
        """
        buff = self.__term.buff
        pattern = re.compile("(%s|%s)\Z" %(PS1, PS3))

        while True:
            text = buff.get_text(0, buff.get_char_count(), True)

            if re.search(pattern, text):
                break

            time.sleep(0.001)

    def _check_dir(self, p_curdir):
        """
            p_curdir: una cadena que representa el directorio actual del
                      usuario.

            Metodo auxiliar que verifica si se ha cambiado el directorio del
            usuario, en ese caso, se actualiza el 'CurrentDirectory' llamando
            el metodo 'CurrentDirectory.set_path' pasando a 'p_curdir' como
            parametro.
        """
        self.__predir = p_curdir  # FIXME: cuando se emita una sennal
                                  #        'curdir_changed', ver si
                                  #        poner esta linea despues del
                                  #        'emit'.

        if not p_curdir:
            return

        current_dir = self.__mwindow.get_cdirectory()

        if current_dir.get_path() != p_curdir:
            gtk.gdk.threads_enter()
            current_dir.set_path(p_curdir)
            gtk.gdk.threads_leave()

    def is_debug_mode(self):
        #FIXME: documentacion

        self.__term.feed_child("disp(isdebugmode());\n")
        self.wait_until_ready()

        lines = self.__term.buff.get_all().splitlines()
        is_debug_mode = False

        for line in lines:
            line = line.strip()
            if line == "1" or line == "0":
                is_debug_mode = bool(int(line))
                break

        return is_debug_mode

    def get_debug_on_event(self):
        #FIXME: documentacion

        self.__term.feed_child("printf('err ');disp(debug_on_error());"
                               "printf('war ');disp(debug_on_warning());"
                               "printf('int ');disp(debug_on_interrupt());\n")
        self.wait_until_ready()

        lines = self.__term.buff.get_all().splitlines()
        debug_on_event = {"err": False, "war": False, "int": False}

        for line in lines:
            if line.startswith("err") or line.startswith("war") or line.startswith("int"):
                key, val = line.split()
                debug_on_event[key] = bool(int(val))

        return debug_on_event

    def is_file_in_loadpath(self, p_file):
        filename = os.path.basename(p_file)
        real = self.file_in_loadpath("'%s'" %filename)
        return p_file == real

    def file_in_loadpath(self, p_filename):
        # p_filename es el nombre de un solo archivo, no puede ser ""

        code = "FILE = file_in_loadpath(NAME);" \
               "if FILE;" \
               "disp(['file ', FILE]);" \
               "endif;" \
               "clear FILE;\n"
        code = code.replace("FILE", VAR).replace("NAME", p_filename)

        self.__term.feed_child(code)
        self.wait_until_ready()

        lines = self.__term.buff.get_all().splitlines()
        length = len(lines)
        pos = 0

        file_ = None

        while pos < length:
            line = lines[pos]

            if line.startswith("file "):
                file_ = os.path.abspath(line[5:].strip())
                break

            pos += 1

        return file_

    def get_curdir(self):
        """
            Retorna: una cadena.

            Devuelve el directorio actual del usuario o la cadena
            vacia en caso de que no se halla podido determinar.
        """

        self.__term.feed_child("%s=pwd(),clear %s;\n" %(VAR, VAR))
        self.wait_until_ready()

        lines = self.__term.buff.get_all().splitlines()
        length = len(lines)
        pos = 0

        pattern = re.compile("^%s = .+$" %VAR)
        curdir = ""

        while pos < length:
            line = lines[pos]

            match = re.search(pattern, line)
            if match:
                curdir = os.path.abspath(line[len(VAR) + 3 : ])
                break

            pos += 1

        return curdir

    def dbwhere(self):
        #FIXME: documentacion

        self.__term.feed_child("dbwhere();\n")
        self.wait_until_ready()

        lines = self.__term.buff.get_all().splitlines()
        length = len(lines)
        pos = 0

        pattern = re.compile("^.+: (line \d+, column \d+)|(\(unknown line\))$")
        dbwhere = {}

        while pos < length:
            line = lines[pos]

            match = re.search(pattern, line)
            if match:
                parts = line.split(": ")

                file_ = parts[0].strip()
                if file_.endswith(".m"):
                    file_ = os.path.abspath(file_)

                # Es 'funcname' cuando la funcion es definida en el CommandWindow
                dbwhere["file"] = file_

                if parts[1][0] == "l":
                    parts = parts[1].split()
                    line = int(parts[1][:-1])
                    column = int(parts[3])
                else:
                    line = column = None

                dbwhere["line"] = line  # Puede ser None
                dbwhere["column"] = column  # Puede ser None

                break

            pos += 1

        return dbwhere

    def dbstack(self, p_omit=""):
        #FIXME: documentacion

        code = self.__dbstack_code %p_omit

        self.__term.feed_child(code)
        self.wait_until_ready()

        lines = self.__term.buff.get_all().splitlines()
        index_plus = lines.index("+++")

        dbstack = {}
        dbstack["current"] = int(lines[index_plus - 1].split()[1]) - 1

        lines = lines[index_plus + 1 : lines.index("---")]
        length = len(lines)
        pos = 0

        dbstack["frames"] = []

        while pos < length:
            frame = {}

            frame["function"] = lines[pos].split()[1]  # 'func>subfunc'
            pos += 1

            line = lines[pos]
            file_ = line[line.index(" ") + 1 : ].strip()
            if file_:
                file_ = os.path.abspath(file_)

            # Es "" cuando la funcion es definida en el CommandWindow
            frame["file"] = file_
            pos += 1

            frame["line"] = int(lines[pos].split()[1])
            pos += 1

            frame["column"] = int(lines[pos].split()[1])
            pos += 1

            dbstack["frames"].append(frame)

        return dbstack

    def dbstatus(self, p_funcname=""):
        #FIXME: documentacion

        code = self.__dbstatus_code %p_funcname

        self.__term.feed_child(code)
        self.wait_until_ready()

        lines = self.__term.buff.get_all().splitlines()
        lines = lines[lines.index("+++") + 1 : lines.index("---")]
        length = len(lines)
        pos = 0

        dbstatus = []

        while pos < length:
            data = {}

            data["function"] = lines[pos].split()[1]  # 'subfunc'
            pos += 1

            line = lines[pos]
            file_ = line[line.index(" ") + 1 : ].strip()
            if file_:
                file_ = os.path.abspath(file_)

            # Puede ser "" cuando es una sub-funcion o la
            # funcion esta definida en el CommandWindow
            data["file"] = file_
            pos += 1

            data["lines"] = []
            while pos < length:
                line = lines[pos]

                if line.startswith("function"):
                    break

                data["lines"].append(int(line.strip()))
                pos += 1

            dbstatus.append(data)

        return dbstatus

    def get_vars(self):
        """
            Retorna: una lista('list') de listas, donde cada sublista contiene
                     los datos de una variable determinada, los datos son:

                     - atributos
                     - nombre
                     - tamanno
                     - bytes
                     - clase

            Retorna los datos de todas las variables del usuario.
        """
        self.__term.feed_child("whos;\n")
        self.wait_until_ready()

        lines = self.__term.buff.get_all().splitlines()
        length = len(lines)
        pos = 0

        find_equal = True
        pattern = re.compile("Total is \d+ elements? using \d+ bytes?", re.IGNORECASE)

        vars_ = []
        while pos < length:
            line = lines[pos]

            if find_equal:
                if "=" in line:
                    find_equal = False

            else:  # find_vars
                if re.search(pattern, line):
                    break

                var = line.split()
                if var and var[-1].lower() != "unknown":
                    if len(var) == 4:
                        var.insert(0, "")
                    vars_.append(var)

            pos += 1
        return vars_

    def _check_state(self, p_curstate):
        if p_curstate != self.__prestate:
            self.__prestate = p_curstate
            self.emit_("state_changed", p_curstate)

    def _check_vars(self, p_vars):
        """
            p_vars: una lista de listas con los datos de todas las variables
                    existentes.

            Metodo auxiliar que verifica si se ha cambiado el estado de las
            variables del usuario, en ese caso, se actualiza el 'Workspace'
            llamando el metodo 'Workspace.update' pasando a 'p_vars' como
            parametro.
        """
        gtk.gdk.threads_enter()
        self.__mwindow.get_wspace().update(p_vars)
        gtk.gdk.threads_leave()

    def _check_dbstatus(self, p_curdbstatus):
        #FIXME: documentacion

        #OJO: Puede que cambien los breakpoints y no se emita la sennal.
        #     Esto no es problema, porque no tiene solucion en Octave_3.2.3.

        predbstatus = self.__predbstatus

        if p_curdbstatus != predbstatus:
            data = Data()
            data.set_data("breakpoints", p_curdbstatus)

            self.emit_("breakpoints_changed", data)

            self.__predbstatus = p_curdbstatus

    def _check_dbstack(self, p_curdbstack):
        #FIXME: documentacion

        predbstack = self.__predbstack

        if p_curdbstack != predbstack:
            data = Data()
            data.set_data("stack", p_curdbstack)

            self.emit_("stack_changed", data)

            self.__predbstack = p_curdbstack

    def _check_dbwhere(self, p_curdbwhere):
        #FIXME: documentacion

        predbwhere = self.__predbwhere

        if p_curdbwhere != predbwhere:
            data = Data()
            data.set_data("where", p_curdbwhere)

            self.emit_("where_changed", data)

            self.__predbwhere = p_curdbwhere

    def emit_(self, *p_args):
        #FIXME: documentacion

        gtk.gdk.threads_enter()
        self.emit(*p_args)
        gtk.gdk.threads_leave()

    def __on_changed(self, p_conn, p_data, p_flag, p_key):
        #FIXME: documentacion

        p_flag.set_data(p_key, True)

    def __on_stack_changed(self, p_conn, p_data, p_flag, p_key):
        #FIXME: documentacion

        if p_flag.get_data(p_key):
            frames = p_data.get_data("stack")["frames"]

            if frames:
                file_ = frames[0]["file"]  # Puede ser ""

                if file_:
                    predbstack = self.__predbstack  # Puede ser None.

                    if not predbstack or frames != predbstack["frames"]:
                        p_flag.set_data(p_key, False)
                        self.emit("stopped_in_file", file_)  # Ya se cerro el candado.

    def __on_where_changed(self, p_conn, p_data, p_flag, p_key):
        #FIXME: documentacion

        #FIXME: Cuando dbstack() de bien el line y column este metodo y
        #       __on_changed sobraran ya que sera suficiente con el metodo
        #       __on_stack_changed. Es decir que este metodo y __on_changed
        #       son un parche para Octave-3.2.3 que en el futuro no haran
        #       falta.

        if p_flag.get_data(p_key):
            where = p_data.get_data("where")

            if where:
                file_ = where["file"]

                if file_.endswith(".m"):
                    p_flag.set_data(p_key, False)
                    self.emit("stopped_in_file", file_)  # Ya se cerro el candado.

    def _print(self, p_text):
        """
            p_text: una cadena para mostrar en el 'CommandWindow'.

            Metodo auxiliar utilizado por el ciclo principal de la 'Connection'
            para mostrar la salida de 'Octave'('p_text') en el 'CommandWindow'.
        """
        cmdwindow = self.__mwindow.get_cmdwindow()
        buff = cmdwindow.get_buffer()

        replacer = lambda match: {PS1: cmdwindow.get_ps1(),
                                  PS2: cmdwindow.get_ps2(),
                                  PS3: cmdwindow.get_ps3()
                                 }[match.group()]

        pattern = re.compile("(%s|%s|%s)" %(PS1, PS2, PS3))
        p_text = re.sub(pattern, replacer, p_text)

        gtk.gdk.threads_enter()
        before = buff.get_char_count()
        buff.insert(buff.limit, p_text)
        buff.limit += buff.get_char_count() - before
        buff.check_scrollback_lines()
        buff.update_no_editable_zone()
        cmdwindow.scroll_to_mark(buff.end_mark, 0.0, True, 0.5, 0.5)
        gtk.gdk.threads_leave()
