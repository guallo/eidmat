import gtk
import gobject


class Command(gobject.GObject):
    """
        Clase base para los comandos que necesiten tener el control de la
        'Connection' para ejecutarse. Estos comandos tienen que tener un
        metodo llamado 'execute' que recibe como parametro a la 'Conection',
        este metodo es el que decide que hace el comando y como se ejecutara
        cuando 'Octave' este listo, es decir, que no este realizando ninguna
        otra operacion.
    """
    def __init__(self, p_prio):
        """
            p_prio:  un 'int'(entero) que es la prioridad del comando. Esta
                     prioridad determina cual es la posicion del comando en
                     la cola de comandos.

            Retorna: un nuevo 'Command'.

            Crea un nuevo 'Command' para ser ejecutado cuando 'Octave' este
            listo.
        """
        gobject.GObject.__init__(self)

        self.__prio = p_prio

    def get_priority(self):
        """
            Retorna: un 'int'.

            Retorna la prioridad del comando.
        """
        return self.__prio

    def __eq__(self, p_cmd):
        """
            p_cmd:   un 'Command'.

            Retorna: 'True' si 'p_cmd' es del mismo tipo que 'self',
                     'False' en otro caso.

            Este metodo es llamado cuando se comparan con el operador '=='
            a dos comandos('Command'), el mismo decide si son iguales o no
            en cuanto a tipo.
        """
        return p_cmd.__class__ == self.__class__

    def execute(self, p_conn):
        """
            p_conn: la 'Connection'.

            Este metodo es el que decide que hace el comando y como se
            ejecutara. Esta implementado en las clases hijas.
        """
        raise NotImplementedError()

    def emit_(self, *p_args):
        #FIXME: documentacion

        gtk.gdk.threads_enter()
        self.emit(*p_args)
        gtk.gdk.threads_leave()
