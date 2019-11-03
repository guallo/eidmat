from cmd.command import Command


class NewVar(Command):
    """
        Comando para crear una nueva variable. Esta nueva variable se crea con
        valor '0'.
    """
    def __init__(self, p_prio=4):
        """
            p_prio:  un 'int'(entero) que es la prioridad del comando. Esta
                     prioridad determina cual es la posicion del comando en
                     la cola de comandos.

            Retorna: un nuevo 'NewVar'.

            Crea un nuevo 'NewVar' para ser ejecutado cuando 'Octave' este
            listo.
        """
        Command.__init__(self, p_prio)

        self.__num = 1
        self.__name = "unnamed"

    def _next_name(self, p_vars):
        """
            p_vars:  una 'list'(lista) con los nombres de todas las variables
                     definidas.

            Retorna: una cadena.

            Retorna un proximo nombre para variable que no exista. Este nombre
            es el que tendra la nueva variable.
        """
        name = self.__name + str(self.__num)
        self.__num += 1

        if name not in p_vars:
            return name
        return self._next_name(p_vars)

    def execute(self, p_conn):
        """
            p_conn: la 'Connection'.

            Crea una nueva variable con valor '0'.
        """
        tail = p_conn.get_tail_with_priority()
        term = p_conn.get_terminal()
        buff = term.buff
        vars_ = [var[1] for var in p_conn.get_vars()]
        new = []

        if self.__name in vars_:
            new.append(self._next_name(vars_))
        else:
            new.append(self.__name)

        for i in xrange(tail.count(self)):
            tail.extract()
            new.append(self._next_name(vars_))

        term.feed_child("=".join(new) + "=0;\n")
        p_conn.wait_until_ready()
        buff.delete(0, buff.get_char_count())
