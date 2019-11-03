import vte

from util.buffer_ import Buffer
from util.constants import PS1


class Terminal(vte.Terminal):
    """
        Terminal auxiliar para pedir datos a 'Octave'.
    """
    def __init__(self):
        """
            Retorna: una 'Terminal'.

            Crea una nueva 'Terminal'.
        """
        vte.Terminal.__init__(self)

        self.__buff = Buffer()
        self.__func = self.__args = None
        self.__col = self.__row = 0

        self.connect("contents-changed", self.on_contents_changed)

        self.set_scrollback_lines(2172)  # 1.4 Mb
        self.fork_command("octave",
                         ["", "--braindead", "-q", "--no-history", "-f"])

        self.feed_child("if(exist('OCTAVE_VERSION')==5);PS1('%s');else;\
                         PS1='%s';endif;" %(PS1, PS1))

    def on_contents_changed(self, p_term):
        """
            p_term: la 'Terminal'.

            Se ejecuta cada vez que cambia la apariencia de la 'Terminal'.
            Almacena el nuevo texto(la salida de 'Octave') en el atributo
            'Terminal.__buff'(un 'Buffer') con el objetivo de poder obtenerlo
            despues.
            Si 'Octave' esta listo y el usuario indico previamente alguna
            funcion o metodo con argumentos a ser llamado cuando ocurriera
            esto, entonces se llama dicha funcion o metodo pasando como
            primer argumento todo el texto contenido en el atributo
            'Terminal.__buff'(un 'Buffer') y despues se pasan los argumentos
            especificados previamente por el usuario.
        """
        buff = self.__buff

        col, row = self.get_cursor_position()
        buff.insert_at_cursor(self.get_text_range(self.__row, self.__col,
                                                  row, col, lambda *args: True
                                                 )[: -1])
        self.__col, self.__row = col, row

        end = buff.get_char_count()
        if buff.get_text(end - len(PS1) - 1, end, True) == "\n%s" %PS1:
            text = buff.get_all()
            if self.__func:
                if self.__args:
                    self.__func(text, self.__args[0])
                else:
                    self.__func(text)

    def feed_child(self, p_text, p_func=None, p_args=None):
        """
            p_text: una cadena para enviarle a 'Octave'.
            p_func: una funcion o metodo a llamar cuando 'Octave' termine de
                    procesar 'p_text'.
            p_args: una 'list'(lista) que contiene un elemento que sera el
                    argumento a pasar cuando se llame a 'p_func'.

            Escribe 'p_text' en la 'Terminal' como si el usuario lo hubiera
            entrado por teclado.
        """
        self.__func = p_func
        self.__args = p_args
        vte.Terminal.feed_child(self, p_text)
