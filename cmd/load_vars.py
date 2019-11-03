import os
import gtk

from cmd.command import Command
from util.message import Message


class LoadVars(Command):
    """
        Comando para cargar variables de un fichero.
    """
    def __init__(self, p_names, p_path, p_prio=79):
        """
            p_names: una 'list'(lista) con los nombres de las variables que se
                     desean cargar del fichero especificado en 'p_path'.
            p_path:  una cadena que es la direccion del fichero del cual se van
                     a extraer las variables deseadas.
            p_prio:  un 'int'(entero) que es la prioridad del comando. Esta
                     prioridad determina cual es la posicion del comando en
                     la cola de comandos.

            Retorna: un nuevo 'LoadVars'.

            Crea un nuevo 'LoadVars' para ser ejecutado cuando 'Octave' este
            listo.
        """
        Command.__init__(self, p_prio)

        self.__names = p_names
        self.__path = p_path

    def get_names(self):
        """
            Retorna: una 'list'.

            Retorna una lista con los nombres de las variables que se desean
            cargar.
        """
        return self.__names

    def get_path(self):
        """
            Retorna: una cadena.

            Retorna la direccion del fichero del cual se quieren cargar las
            variables deseadas.
        """
        return self.__path

    def execute(self, p_conn):
        """
            p_conn: la 'Connection'.

            Carga las variables deseadas del fichero indicado.
        """
        tail = p_conn.get_tail_with_priority()
        names = self.__names
        path = self.__path
        all_cmds = [names]

        for pos in xrange(len(tail) - 1, -1, -1):
            elem = tail[pos]

            if elem == self and elem.get_path() == path:
                all_cmds.append(elem.get_names())
                tail.extract(pos)

        if [] in all_cmds:
            names = []
        else:
            del all_cmds[0]
            for cmd in all_cmds:
                for name in cmd:
                    if name not in names:
                        names.append(name)

        # if (No existe el archivo):
        if not os.access(path, os.F_OK):
            msg = "could not be found."

        # elif (No se puede leeer):
        elif not os.access(path, os.R_OK):
            msg = "could not be readed."

        else:
            p_conn.get_terminal().feed_child("load -force '%s' %s;\n"
                                             %(path, " ".join(names)))
            p_conn.wait_until_ready()
            if p_conn.get_terminal().buff.get_all().split("\n")[-2][0] != "e":
                return
            else:
                msg = "could not be read matrix."

        Message(gtk.STOCK_DIALOG_WARNING, "%s\n\n%s" %(path, msg),
                "Loading Failed", p_conn.get_mwindow().get_window()).run(True)
