import gtk

from cmd.command import Command
from util.message import Message


class RenameVar(Command):
    """
        Comando para renombrar una variable determinada.
    """
    def __init__(self, p_new, p_old, p_global, p_prio=2):
        """
            p_new:    una cadena que es el nuevo nombre a poner a la variable.
            p_old:    una cadena que es el nombre de la variable a renombrar.
            p_global: un 'boolean' que dice si la variable a renombrar es
                      global o no.
            p_prio:   un 'int'(entero) que es la prioridad del comando. Esta
                      prioridad determina cual es la posicion del comando en
                      la cola de comandos.

            Retorna:  un nuevo 'RenameVar'.

            Crea un nuevo 'RenameVar' para ser ejecutado cuando 'Octave' este
            listo.
        """
        Command.__init__(self, p_prio)

        self.__new = p_new
        self.__old = p_old
        self.__global = p_global

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

    def get_global(self):
        """
            Retorna: un 'boolean'.

            Retorna 'True' si la variable a renombrar es global, 'False'
            en otro caso.
        """
        return self.__global

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

        new, old, is_global = last.get_new(), last.get_old(), last.get_global()
        if new != old:
            rep = new.replace("_", "")
            if new and not new[0].isdigit() and (not rep or rep.isalnum()):
                cmd = "clear %s;%s%s=%s;clear %s;\n"\
                      %(new, ("", "global %s;" %new)[is_global], new, old, old)
                p_conn.get_terminal().feed_child(cmd)
                p_conn.wait_until_ready()
                if p_conn.get_terminal().buff.get_all().rfind("^") == -1:
                    return

            msg = 'Could not rename the variable.\n\n'\
                  '"%s" is not a valid OCTAVE variable name.\n'\
                  'OCTAVE variable names must:\n'\
                  '- Begin with a letter or underscore\n'\
                  '- Contain only alphanumeric characters and underscores\n'\
                  '- Not be a OCTAVE keyword' %new

            Message(gtk.STOCK_DIALOG_WARNING, msg, "Editing Failed",
                    p_conn.get_mwindow().get_window()).run(True)
