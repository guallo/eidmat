from cmds.command import Command


class DuplicateVar(Command):
    """
        Comando para duplicar una variable. Crea una nueva variable con el
        mismo valor de la variable determinada.
    """
    def __init__(self, p_name, p_attr, p_prio=1):
        """
            p_name:  una cadena que es el nombre de la variable a duplicar.
            p_attr:  una cadena con los atributos de la variable a duplicar.
            p_prio:  un 'int'(entero) que es la prioridad del comando. Esta
                     prioridad determina cual es la posicion del comando en
                     la cola de comandos.

            Retorna: un nuevo 'DuplicateVar'.

            Crea un nuevo 'DuplicateVar' para ser ejecutado cuando 'Octave'
            este listo.
        """
        Command.__init__(self, p_prio)

        self.__name = p_name
        self.__attr = p_attr
        self.__dup = None
        self.__num = None

    def get_name(self):
        """
            Retorna: una cadena.

            Retorna el nombre de la variable a duplicar.
        """
        return self.__name

    def get_attr(self):
        """
            Retorna: una cadena.

            Retorna los atributos de la variable a duplicar.
        """
        return self.__attr

    def _next_name(self, p_vars):
        """
            p_vars:  una 'list'(lista) con los nombres de todas las variables
                     definidas.

            Retorna: una cadena.

            Retorna un proximo nombre para variable que no exista. Este nombre
            es el que tendra la nueva variable.
        """
        dup = self.__dup + str(self.__num)
        self.__num += 1

        if dup not in p_vars:
            return dup
        return self._next_name(p_vars)

    def execute(self, p_conn):
        """
            p_conn: la 'Connection'.

            Duplica la variable deseada.
        """
        tail = p_conn.get_tail_with_priority()
        term = p_conn.get_terminal()
        buff = term.buff
        vars_ = [var[1] for var in p_conn.get_vars()]
        names = {self.__name: [1, self.__attr]}
        cmd = ""

        for i in xrange(tail.count(self)):
            elem = tail.extract()
            name = elem.get_name()
            if name in names:
                names[name][0] += 1
            else:
                names[name] = [1, elem.get_attr()]

        for name in names:
            self.__dup = dup = "%sCopy" %name
            self.__num = 1
            new = []

            if dup in vars_:
                new.append(self._next_name(vars_))
            else:
                new.append(dup)

            for i in xrange(names[name][0] - 1):
                new.append(self._next_name(vars_))

            if "g" in names[name][1]:
                cmd += "global %s;" %(" ".join(new))
            if "p" in names[name][1]:
                cmd += "persistent %s;" %(" ".join(new))
            cmd += "%s=%s;" %("=".join(new), name)

        term.feed_child(cmd + "\n")
        p_conn.wait_until_ready()
        buff.delete(0, buff.get_char_count())
