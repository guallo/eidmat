import gtk

from cmd.command import Command


class ClearCMDWindow(Command):
    """
        Comando para limpiar el 'CommandWindow'.
    """
    def __init__(self, p_prio=0):
        """
            p_prio:  un 'int'(entero) que es la prioridad del comando. Esta
                     prioridad determina cual es la posicion del comando en
                     la cola de comandos.

            Retorna: un nuevo 'ClearCMDWindow'.

            Crea un nuevo 'ClearCMDWindow' para ser ejecutado cuando 'Octave'
            este listo.
        """
        Command.__init__(self, p_prio)

    def execute(self, p_conn):
        """
            p_conn: la 'Connection'.

            Limpia el 'CommandWindow'.
        """
        tail = p_conn.get_tail_with_priority()

        for pos in xrange(len(tail) - 1, -1, -1):
            if tail[pos] == self:
                tail.extract(pos)

        cmdwindow = p_conn.get_mwindow().get_cmdwindow()
        len_ps1 = len(cmdwindow.get_ps1())  # Warning: len(cmdwindow.get_ps1())
        buff = cmdwindow.get_buffer()

        gtk.gdk.threads_enter()
        buff.delete(0, buff.limit - len_ps1)
        buff.limit = len_ps1
        gtk.gdk.threads_leave()
