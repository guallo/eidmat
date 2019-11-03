import gtk
from threading import Semaphore


class Buffer(gtk.TextBuffer):
    """
        Clase base para todos los buffers. Esta clase sincroniza el acceso a
        los metodos del 'Buffer' que lo modifican, para evitar que falle la
        aplicacion, e.g. cuando se hace uso de algun iterador invalido.
    """
    def __init__(self):
        """
            Retorna: un nuevo 'Buffer'.

            Crea un nuevo 'Buffer'.
        """
        gtk.TextBuffer.__init__(self)

        # El objetivo de este semaforo es sincronizar el acceso a los
        # metodos de 'Buffer' que lo modifican, para evitar que falle el
        # programa cuando se invaliden los iteradores.
        self.__sem = Semaphore()

    def get_semaphore(self):
        """
            Retorna: un 'threading.Semaphore'.

            Retorna el semaforo que sincroniza el acceso a los metodos del
            'Buffer' que lo modifican.
        """
        return self.__sem

    def insert(self, p_where, p_text):
        """
            p_where: un 'int'(entero) que representa un offset(posicion) en el
                     'Buffer'.
            p_text:  una cadena.

            Llama el metodo 'gtk.TextBuffer.insert' pasando como primer
            parametro un 'gtk.TextIter' correspondiente a 'p_where' y, pasa a
            'p_text' como segundo parametro.
        """
        self.__sem.acquire()
        gtk.TextBuffer.insert(self, self.get_iter_at_offset(p_where), p_text)
        self.__sem.release()

    def insert_at_cursor(self, p_text):
        """
            p_text: una cadena.

            Llama el metodo 'gtk.TextBuffer.insert_at_cursor' pasando como
            parametro a 'p_text'.
        """
        self.__sem.acquire()
        gtk.TextBuffer.insert_at_cursor(self, p_text)
        self.__sem.release()

    def get_text(self, p_start, p_end, p_hidden):
        """
            p_start:  un 'int'(entero) que representa un offset(posicion) en el
                      'Buffer'.
            p_end:    un 'int'(entero) que representa un offset(posicion) en el
                      'Buffer'.
            p_hidden: un 'boolean'.

            Retorna:  una cadena.

            Llama el metodo 'gtk.TextBuffer.get_text' pasando como primer
            parametro un 'gtk.TextIter' correspondiente a 'p_start'; pasa un
            'gtk.TextIter' correspondiente a 'p_end' como segundo parametro y,
            como ultimo parametro pasa a 'p_hidden'.
        """
        self.__sem.acquire()
        text = gtk.TextBuffer.get_text(self, self.get_iter_at_offset(p_start),
                                       self.get_iter_at_offset(p_end),
                                       p_hidden)
        self.__sem.release()
        return text

    def delete(self, p_start, p_end):
        """
            p_start: un 'int'(entero) que representa un offset(posicion) en el
                     'Buffer'.
            p_end:   un 'int'(entero) que representa un offset(posicion) en el
                     'Buffer'.

            Llama el metodo 'gtk.TextBuffer.delete' pasando como primer
            parametro un 'gtk.TextIter' correspondiente a 'p_start' y, pasa un
            'gtk.TextIter' correspondiente a 'p_end' como segundo parametro.
        """
        self.__sem.acquire()
        gtk.TextBuffer.delete(self, self.get_iter_at_offset(p_start),
                              self.get_iter_at_offset(p_end))
        self.__sem.release()

    def apply_tag(self, p_tag, p_start, p_end):
        """
            p_tag:   un 'gtk.TextTag'.
            p_start: un 'int'(entero) que representa un offset(posicion) en el
                     'Buffer'.
            p_end:   un 'int'(entero) que representa un offset(posicion) en el
                     'Buffer'.

            Llama el metodo 'gtk.TextBuffer.apply_tag' pasando como primer
            parametro a 'p_tag'; como segundo parametro pasa un 'gtk.TextIter'
            correspondiente a 'p_start' y, pasa un 'gtk.TextIter'
            correspondiente a 'p_end' como ultimo parametro.
        """
        self.__sem.acquire()
        gtk.TextBuffer.apply_tag(self, p_tag, self.get_iter_at_offset(p_start),
                                 self.get_iter_at_offset(p_end))
        self.__sem.release()

    def remove_tag(self, p_tag, p_start, p_end):
        """
            p_tag:   un 'gtk.TextTag'.
            p_start: un 'int'(entero) que representa un offset(posicion) en el
                     'Buffer'.
            p_end:   un 'int'(entero) que representa un offset(posicion) en el
                     'Buffer'.

            Llama el metodo 'gtk.TextBuffer.remove_tag' pasando como primer
            parametro a 'p_tag'; como segundo parametro pasa un 'gtk.TextIter'
            correspondiente a 'p_start' y, pasa un 'gtk.TextIter'
            correspondiente a 'p_end' como ultimo parametro.
        """
        self.__sem.acquire()
        gtk.TextBuffer.remove_tag(self, p_tag,
                                  self.get_iter_at_offset(p_start),
                                  self.get_iter_at_offset(p_end))
        self.__sem.release()

    def place_cursor(self, p_where):
        """
            p_where: un 'int'(entero) que representa un offset(posicion) en el
                     'Buffer'.

            Llama el metodo 'gtk.TextBuffer.place_cursor' pasando como
            parametro un 'gtk.TextIter' correspondiente a 'p_where'.
        """
        self.__sem.acquire()
        gtk.TextBuffer.place_cursor(self, self.get_iter_at_offset(p_where))
        self.__sem.release()

    def get_selection_bounds(self):
        """
            Retorna: una tupla('tuple') vacia si no hay seleccion en el
                     'Buffer', sino, retorna una tupla con dos enteros('int')
                     que representan la posicion(offset) inicial y final de la
                     seleccion respectivamente.

            Retorna una tupla('tuple') que indica el inicio y fin de la
            seleccion en el 'Buffer' si es que hay alguna.
        """
        self.__sem.acquire()
        selec = gtk.TextBuffer.get_selection_bounds(self)
        if selec:
            selec = (selec[0].get_offset(), selec[1].get_offset())
        self.__sem.release()
        return selec
    
    def move_mark(self, p_mark, p_where):
        """
            p_mark:  un 'gtk.TextMark'.
            p_where: un 'int'(entero) que representa un offset(posicion) en el
                     'Buffer'.

            Llama el metodo 'gtk.TextBuffer.move_mark' pasando como primer
            parametro a 'p_mark' y, pasa como segundo parametro un
            'gtk.TextIter' correspondiente a 'p_where'.
        """
        self.__sem.acquire()
        gtk.TextBuffer.move_mark(self, p_mark,
                                 self.get_iter_at_offset(p_where))
        self.__sem.release()

    def create_mark(self, p_mark_name, p_where, p_left_gravity):
        """
            p_mark_name:    una cadena.
            p_where:        un 'int'(entero) que representa un offset(posicion)
                            en el 'Buffer'.
            p_left_gravity: un 'boolean'.

            Retorna:        un 'gtk.TextMark'.

            Llama el metodo 'gtk.TextBuffer.create_mark' pasando como primer
            parametro a 'p_mark_name'; como segundo parametro pasa un
            'gtk.TextIter' correspondiente a 'p_where' y, como ultimo parametro
            pasa a 'p_left_gravity'.
            Este metodo retorna un 'gtk.TextMark' obtenido de la llamada al
            metodo 'gtk.TextBuffer.create_mark' explicada anteriormente.
        """
        self.__sem.acquire()
        mark = gtk.TextBuffer.create_mark(self, p_mark_name,
                                          self.get_iter_at_offset(p_where),
                                          p_left_gravity)
        self.__sem.release()
        return mark

    def get_all(self):
        """
            Retorna: una cadena.

            Devuelve y elimina todo el texto del 'Buffer'.
        """
        end = self.get_char_count()
        text = self.get_text(0, end, True)
        self.delete(0, end)
        return text

    def get_offset_at_line(self, p_line):
        """
            p_line:  un 'int'(entero) que indica una linea en el 'Buffer'. La
                     primera linea del 'Buffer' es la '0'.

            Retorna: un 'int'.

            Retorna la posicion(offset) del primer caracter de la linea
            'p_line'.
        """
        self.__sem.acquire()
        offset = self.get_iter_at_line(p_line).get_offset()
        self.__sem.release()
        return offset

    def get_offset_at_mark(self, p_mark):
        """
            p_mark:  un 'gtk.TextMark'.

            Retorna: un 'int'.

            Retorna la posicion(offset) de 'p_mark' en el 'Buffer'.
        """
        self.__sem.acquire()
        offset = gtk.TextBuffer.get_iter_at_mark(self, p_mark).get_offset()
        self.__sem.release()
        return offset
