from cmds.command import Command


class ManageCommandPro(Command):
    """
        Clase para enviar comandos asociados al trabajo con proyecto de forma 
        oculta a octave.
    """
    def __init__(self, p_command, p_prio=0):
        """
            p_command:  una cadena que representa un comando a enviar.
            p_prio:     un 'int'(entero) que es la prioridad del comando. Esta
                        prioridad determina cual es la posicion del comando en
                        la cola de comandos.

            Retorna:    un nuevo 'ManagePath'.

            Constructor de la clase ManagePath.
        """
        Command.__init__(self, p_prio)

        self.__command = p_command

    def get_path(self):
        """
            Retorna: una cadena.

            Retorna el path.
        """
        return self.__command

    def execute(self, p_conn):
        """
            p_conn: la 'Connection'.

            adiciona o elimina el path de octave.
        """
        term = p_conn.get_terminal()
        buff = term.buff
        term.feed_child(self.__command)
        p_conn.wait_until_ready()
        buff.delete(0, buff.get_char_count())
