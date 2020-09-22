import os

from cmds.command import Command


class ChangeDirectory(Command):
    """
        Comando para cambiar de directorio actual.
    """
    def __init__(self, p_dir, p_prio=0):
        """
            p_dir :  una cadena que representa el directorio al cual se desea
                     cambiar.
            p_prio:  un 'int'(entero) que es la prioridad del comando. Esta
                     prioridad determina cual es la posicion del comando en
                     la cola de comandos.

            Retorna: un nuevo 'ChangeDirectory'.

            Crea un nuevo 'ChangeDirectory' para ser ejecutado cuando 'Octave'
            este listo.
        """
        Command.__init__(self, p_prio)

        self.__dir = os.path.abspath(p_dir)

    def get_dir(self):
        """
            Retorna: una cadena.

            Devuelve el directorio al cual se desea cambiar.
        """
        return self.__dir

    def execute(self, p_conn):
        """
            p_conn: la 'Connection'.

            Cambia al directorio deseado.
        """
        tail = p_conn.get_tail_with_priority()
        term = p_conn.get_terminal()
        buff = term.buff

        curdir = self.__dir

        while len(tail) and tail[0] == self:
            curdir = tail.extract().get_dir()

        term.feed_child("cd '%s';\n" %curdir)
        p_conn.wait_until_ready()
        buff.delete(0, buff.get_char_count())
