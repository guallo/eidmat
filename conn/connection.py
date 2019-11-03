import os
import re
import gtk
import time
import threading

from util.tail_with_priority import TailWithPriority
from util.constants import PS1, PS2, VAR
from conn.terminal import Terminal


class Connection(threading.Thread):
    """
        Establece la conexion con 'Octave'. Es a traves de esta clase que nos
        podemos comunicar con 'Octave'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   una 'Connection'.

            Crea una nueva 'Connection'.
        """
        threading.Thread.__init__(self)

        self.__mwindow = p_mwindow
        self.__continue = True
        self.__term = Terminal(self)

        # Aqui se almacenan los comandos
        # que envia el usuario a octave.
        self.__tail = []

        # Cuando el usuario da doble click sobre el CurrentDirectory
        # esta variable almacena el directorio al cual se quiere cambiar.
        self.__change_dir = None

        # Aqui se almacenan los comandos que se
        # ejecutaran cuando el octave este listo.
        self.__tail_prio = TailWithPriority()

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

        term.feed_child("addpath (genpath ('%s'), '-begin');\n\
                         if (exist ('OCTAVE_VERSION') == 5)\n\
                         PS1 ('%s');\n\
                         PS2 ('%s');\n\
                         else\n\
                         PS1 = '%s';\n\
                         PS2 = '%s';\n\
                         endif\n" %(m, PS1, PS2, PS1, PS2))

        while True:
            if term.state_ == PS1:
                end = buff.get_char_count() - len(PS1)
                if buff.get_text(end - 1, end, True) != "'":
                    buff.delete(0, end)
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

    def set_change_dir(self, p_dir):
        """
            p_dir: una cadena que representa la direccion de una carpeta.

            Establece el atributo 'Connection.__change_dir' igual a 'p_dir'.
            Esto causa que 'p_dir' se establezca como directorio actual del
            usuario. Este metodo es llamado cuando el usuario trata de cambiar
            de directorio usuando las funcionalidades del 'CurrentDirectory',
            por ejemplo, cuando se da doble click sobre alguna carpeta en el
            listado de archivos('ListFiles') del 'CurrentDirectory'.
        """
        self.__change_dir = p_dir

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
        sent = True

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

            if term.state_ == PS1 and pass_ and not buff.get_char_count():
                count += 1
                if count > 9:
                    if self.__change_dir:
                        self._update_cdirectory()
                    elif sent:
                        self._check_dir()
                    flag = False
                    while not tail_prio.is_empty():
                        tail_prio.extract().execute(self)
                        flag = True
                    if sent or flag:
                        self._check_vars()
                        sent = False
                    count = 10

        self.__mwindow.close_now()  # Cerramos la aplicacion.

    def wait_until_ready(self):
        """
            Espera hasta que 'Octave' este listo.
        """
        buff = self.__term.buff
        len_ = len(PS1)

        while True:
            count = buff.get_char_count()
            if count and buff.get_text(count - len_, count, True) == PS1:
                break
            time.sleep(0.001)

    def _update_cdirectory(self):
        """
            Metodo auxiliar que establece la direccion contenida en el
            atributo 'Connection.__change_dir' como directorio actual del
            usuario. Actualiza el 'CurrentDirectory' con las carpetas y
            archivos contenidos en el directorio 'Connection.__change_dir'.
        """
        term = self.__term
        buff = term.buff
        dir_ = self.__change_dir

        term.feed_child("cd '%s';\n" %(dir_, ))
        self.wait_until_ready()
        buff.delete(0, buff.get_char_count())
        gtk.gdk.threads_enter()
        self.__mwindow.get_cdirectory().set_path(dir_)
        gtk.gdk.threads_leave()
        self.__change_dir = None

    def _check_dir(self):
        """
            Metodo auxiliar que verifica si se ha cambiado el directorio del
            usuario, en ese caso, se actualiza el 'CurrentDirectory' llamando
            el metodo 'CurrentDirectory.set_path' pasando como parametro la
            direccion del nuevo directorio.
        """
        current_dir = self.__mwindow.get_cdirectory()

        self.__term.feed_child("%s=pwd,clear %s;\n" %(VAR, VAR))
        self.wait_until_ready()
        dir_ = self.__term.buff.get_all().split("\n")[-2][len(VAR) + 3: ]
        if current_dir.get_path() != dir_:
            gtk.gdk.threads_enter()
            current_dir.set_path(dir_)
            gtk.gdk.threads_leave()

    def get_vars(self):
        """
            Retorna: una lista('list') de listas, donde cada sublista contiene
                     los datos de una variable determinada, los datos son el
                     nombre, tamanno, bytes, clase y si es global o no.

            Retorna los datos de todas las variables del usuario.
        """
        self.__term.feed_child("whos -variables;\n")
        self.wait_until_ready()

        lines = self.__term.buff.get_all().splitlines()
        pos, length = 0, len(lines)

        pattern1 = re.compile("^\s*\*+", re.IGNORECASE)
        pattern2 = re.compile("global", re.IGNORECASE)

        find_aster = True
        find_equal = find_vars = False

        vars_ = []
        while pos < length:
            line = lines[pos]

            if find_aster and re.search(pattern1, line):
                if re.search(pattern2, line):
                    is_global = True
                else:
                    is_global = False
                find_equal = True
                find_aster = find_vars = False

            elif find_equal and "=" in line:
                find_vars = True
                find_aster = find_equal = False

            elif find_vars:
                if line:
                    var = line.split()
                    var.append(is_global)
                    vars_.append(var)
                else:
                    find_aster = True
                    find_equal = find_vars = False

            pos += 1
        return vars_

    def _check_vars(self):
        """
            Metodo auxiliar que verifica si se ha cambiado el estado de las
            variables del usuario, en ese caso, se actualiza el 'Workspace'
            llamando el metodo 'Workspace.update' pasando como parametro un
            listado con los datos de todas las variables existentes.
        """
        vars_ = self.get_vars()
        gtk.gdk.threads_enter()
        self.__mwindow.get_wspace().update(vars_)
        gtk.gdk.threads_leave()

    def _print(self, p_text):
        """
            p_text: una cadena para mostrar en el 'CommandWindow'.

            Metodo auxiliar utilizado por el ciclo principal de la 'Connection'
            para mostrar la salida de 'Octave'('p_text') en el 'CommandWindow'.
        """
        cmdwindow = self.__mwindow.get_cmdwindow()
        buff = cmdwindow.get_buffer()

        p_text = p_text.replace(PS1, cmdwindow.get_ps1())
        p_text = p_text.replace(PS2, cmdwindow.get_ps2())

        gtk.gdk.threads_enter()
        before = buff.get_char_count()
        buff.insert(buff.limit, p_text)
        buff.limit += buff.get_char_count() - before
        buff.check_scrollback_lines()
        buff.update_no_editable_zone()
        cmdwindow.scroll_to_mark(buff.end_mark, 0.0, True, 0.5, 0.5)
        gtk.gdk.threads_leave()
