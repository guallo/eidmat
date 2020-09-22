import re
import gtk

from cmds.command import Command
from util.message import Message


class RenameVar(Command):
    """
        Comando para renombrar una variable determinada.
    """
    def __init__(self, p_new, p_old, p_attr, p_prio=2):
        """
            p_new:   una cadena que es el nuevo nombre a poner a la variable.
            p_old:   una cadena que es el nombre de la variable a renombrar.
            p_attr:  una cadena con los atributos de la variable a renombrar.
            p_prio:  un 'int'(entero) que es la prioridad del comando. Esta
                     prioridad determina cual es la posicion del comando en
                     la cola de comandos.

            Retorna: un nuevo 'RenameVar'.

            Crea un nuevo 'RenameVar' para ser ejecutado cuando 'Octave' este
            listo.
        """
        Command.__init__(self, p_prio)

        self.__new = p_new
        self.__old = p_old
        self.__attr = p_attr

    def get_new(self):
        """
            Retorna: una cadena.

            Retorna el nuevo nombre a poner a la variable que se quiere
            renombrar.
        """
        return self.__new

    def get_old(self):
        """
            Retorna: una cadena.

            Retorna el nombre de la variable que se quiere renombrar.
        """
        return self.__old

    def get_attr(self):
        """
            Retorna: una cadena.

            Retorna los atributos de la variable a renombrar.
        """
        return self.__attr

    def execute(self, p_conn):
        """
            p_conn: la 'Connection'.

            Renombra la variable deseada con el nuevo nombre.
        """
        tail = p_conn.get_tail_with_priority()
        found = False
        last = self

        for pos in xrange(tail.count(self) - 1, -1, -1):
            if tail[pos].get_old() == self.__old:
                if not found:
                    last = tail[pos]
                    found = True
                tail.extract(pos)

        new, old, attr = last.get_new(), last.get_old(), last.get_attr()
        if new != old:
            if re.search("^[_\$a-zA-Z][_\$a-zA-Z0-9]*\Z", new):

                cmd = "clear %s;" %new
                if "g" in attr:
                    cmd += "global %s;" %new
                if "p" in attr:
                    cmd += "persistent %s;" %new
                cmd += "%s=%s;clear %s;\n" %(new, old, old)

                p_conn.get_terminal().feed_child(cmd)
                p_conn.wait_until_ready()
                if p_conn.get_terminal().buff.get_all().rfind("^") == -1:
                    return

            msg = 'Could not rename the variable.\n\n'\
                  '"%s" is not a valid OCTAVE variable name.\n'\
                  'OCTAVE variable names must:\n'\
                  '- Begin with a letter, underscore or dollar\n'\
                  '- Contain only letters, underscores, dollars and digits\n'\
                  '- Not be a OCTAVE keyword' %new

            Message(gtk.STOCK_DIALOG_WARNING, msg, "Editing Failed",
                    p_conn.get_mwindow().get_window()).run(True)
