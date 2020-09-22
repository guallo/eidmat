from cmds.command import Command


class DeleteVar(Command):
    """
        Comando para eliminar una variable determinada.
    """
    def __init__(self, p_name, p_prio=3):
        """
            p_name:  una cadena que es el nombre de la variable a eliminar.
            p_prio:  un 'int'(entero) que es la prioridad del comando. Esta
                     prioridad determina cual es la posicion del comando en
                     la cola de comandos.

            Retorna: un nuevo 'DeleteVar'.

            Crea un nuevo 'DeleteVar' para ser ejecutado cuando 'Octave'
            este listo.
        """
        Command.__init__(self, p_prio)

        self.__name = p_name

    def get_name(self):
        """
            Retorna: una cadena.

            Retorna el nombre de la variable a eliminar.
        """
        return self.__name

    def execute(self, p_conn):
        """
            p_conn: la 'Connection'.

            Elimina la variable deseada.
        """
        tail = p_conn.get_tail_with_priority()
        term = p_conn.get_terminal()
        buff = term.buff
        names = [self.__name]

        for i in xrange(tail.count(self)):
            names.append(tail.extract().get_name())

        term.feed_child("clear %s;\n" %" ".join(names))
        p_conn.wait_until_ready()
        buff.delete(0, buff.get_char_count())
