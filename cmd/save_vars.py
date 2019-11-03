import os
import gtk

from cmd.command import Command
from util.message import Message
from util.confirm import Confirm
from wspace.workspace_save_dialog import WorkspaceSaveDialog


class SaveVars(Command):
    """
        Comando para salvar variables a fichero.
    """
    def __init__(self, p_names, p_path, p_prio=0):
        """
            p_names: una 'list'(lista) con los nombres de las variables que se
                     desean salvar al fichero especificado en 'p_path'.
            p_path:  una cadena que es la direccion del fichero al cual se van
                     a guardar las variables deseadas.
            p_prio:  un 'int'(entero) que es la prioridad del comando. Esta
                     prioridad determina cual es la posicion del comando en
                     la cola de comandos.

            Retorna: un nuevo 'SaveVars'.

            Crea un nuevo 'SaveVars' para ser ejecutado cuando 'Octave' este
            listo.
        """
        Command.__init__(self, p_prio)

        self.__names = p_names
        self.__path = p_path

    def get_names(self):
        """
            Retorna: una 'list'.

            Retorna una lista con los nombres de las variables que se desean
            guardar.
        """
        return self.__names

    def get_path(self):
        """
            Retorna: una cadena.

            Retorna la direccion del fichero al cual se quieren guardar las
            variables deseadas.
        """
        return self.__path

    def execute(self, p_conn):
        """
            p_conn: la 'Connection'.

            Guarda las variables deseadas en el fichero indicado.
        """
        tail = p_conn.get_tail_with_priority()
        names = self.__names
        path = self.__path

        for pos in xrange(len(tail) - 1, -1, -1):
            elem = tail[pos]

            if elem == self and len(elem.get_names()) == len(names) and\
               elem.get_path() == path:

                flag = True
                for name in elem.get_names():
                    if name not in names:
                        flag = False
                        break

                if flag:
                    tail.extract(pos)

        ########################## BEGIN ###############################
        main_win = p_conn.get_mwindow()
        parent = main_win.get_window()
        curdir = main_win.get_cdirectory().get_path()

        while True:
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
                break

            if not Confirm(stock, "%s\n\n%s" %(path, "\n".join(msg)),
                                  "Save to VAR-File:", parent).run(True):
                return

            path = WorkspaceSaveDialog(parent, curdir).run(True)

            if not path:
                return
        ########################## END #################################

        p_conn.get_terminal().feed_child("save -binary '%s' %s;\n"
                                         %(path, " ".join(names)))
        p_conn.wait_until_ready()
        lines = p_conn.get_terminal().buff.get_all().split("\n")

        pos = -2
        line = lines[pos]
        vars_ = []

        while line[0] == "w":
            vars_.insert(0, line[line.rfind("`") + 1: -1])
            pos -= 1
            line = lines[pos]

        if vars_:
            if len(vars_) == 1:
                msg = 'A variable named "%s"' %vars_[0]
            elif len(vars_) == 2:
                msg = 'Variables named "%s" and "%s"' %(vars_[0], vars_[1])
            else:
                msg = "Some variables"

            Message(gtk.STOCK_DIALOG_WARNING, "%s could not be saved." %msg,
                    "Saving Failed", parent).run(True)
