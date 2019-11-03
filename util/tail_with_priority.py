class TailWithPriority:
    """
        Clase que modela una cola con prioridad.
    """
    def __init__(self):
        """
            Retorna: un nuevo 'TailWithPriority'.

            Crea un nuevo 'TailWithPriority'.
        """
        self.__elems = []

    def append(self, p_elem):
        """
            p_elem: un objeto que tenga un metodo 'get_priority()' que devuelva
                    un 'int'(entero) que sea su prioridad.

            Adiciona a 'p_elem' en la cola segun su prioridad. Los elementos
            con menor valor en su prioridad pasan al inicio de la cola.
        """
        for pos, e in enumerate(self.__elems):
            if p_elem.get_priority() < e.get_priority():
                self.__elems.insert(pos, p_elem)
                return
        self.__elems.append(p_elem)

    def extract(self, p_pos=0):
        """
            p_pos:   un 'int'(entero) que indica una posicion en la cola.

            Retorna: el elemento que esta en la posicion 'p_pos' de la cola.

            Devuelve y elimina de la cola el elemento de la posicion 'p_pos'.
        """
        return self.__elems.pop(p_pos)

    def is_empty(self):
        """
            Retorna: 'True' si la cola esta vacia, 'False' en otro caso.

            Retorna 'True' o 'False' si la cola esta o no vacia.
        """
        return len(self.__elems) == 0

    def count(self, p_elem):
        """
            p_elem: un objeto.

            Retorna: un 'int'.

            Retorna la cantidad de veces que aparece 'p_elem' en la cola.
        """
        return self.__elems.count(p_elem)

    def __getitem__(self, p_pos):
        """
            p_pos:   un 'int'(entero) que indica una posicion en la cola.

            Retorna: un elemento de la cola.

            Retorna el elemento de la cola que esta en la posicion 'p_pos'.
        """
        return self.__elems[p_pos]

    def __len__(self):
        """
            Retorna: un 'int'.

            Devuelve la cantidad de elementos de la cola.
        """
        return len(self.__elems)
