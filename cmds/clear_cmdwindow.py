import gtk

from cmds.command import Command
from conn.terminal import TerminalState


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
        state = p_conn.get_terminal().state_
        cmdwindow = p_conn.get_mwindow().get_cmdwindow()
        buff = cmdwindow.get_buffer()

        for pos in xrange(len(tail) - 1, -1, -1):
            if tail[pos] == self:
                tail.extract(pos)

        if state == TerminalState.READY:
            prompt = cmdwindow.get_ps1()
        else:  # state == TerminalState.DEBUGGING
            prompt = cmdwindow.get_ps3()

        gtk.gdk.threads_enter()
        buff.delete(0, buff.limit - len(prompt))
        buff.limit = len(prompt)
        gtk.gdk.threads_leave()
