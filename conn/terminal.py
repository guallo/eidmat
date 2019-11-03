import gtk
import vte

from util.constants import PS1, PS2
from util.buffer_ import Buffer


class Terminal(vte.Terminal):
    """
        Es la terminal virtual donde se ejecuta 'Octave'.
    """
    def __init__(self, p_conn):
        """
            p_conn:  un 'Connection' que es la conexion con Octave.

            Retorna: una 'Terminal'.

            Retorna una nueva 'Terminal'.
        """
        vte.Terminal.__init__(self)

        self.__conn = p_conn

        # Estos atributos se dejaron publico
        # por cuestion de ganar en velocidad.
        self.buff = Buffer()
        self.state_ = None

        self.__col = 0
        self.__row = 0

        self.connect("contents-changed", self.on_contents_changed)
        self.connect("child-exited", self.on_child_exited)

        self.set_scrollback_lines(2172)  # 1.4 Mb
        self.fork_command("octave", ["", "--braindead", "-q", "--no-history"])

    def on_contents_changed(self, p_term):
        """
            p_term: la 'Terminal'.

            Se ejecuta cada vez que cambia la apariencia de la 'Terminal'.
            Almacena el nuevo texto(la salida de 'Octave') en el atributo
            'Terminal.buff'(un 'Buffer') con el objetivo de que 'Connection'
            lo pueda obtener despues y mostarlo en el 'CommandWindow'.
            Tambien guarda en el atributo 'Terminal.state_' si lo ultimo que
            esta en la 'Terminal' es el 'PS1'(prompt 1), 'PS2'(prompt 2), o
            ninguno de los dos.
        """
        col, row = self.get_cursor_position()
        if (row > self.__row) or (row == self.__row and col >= self.__col):
            text = self.get_text_range(self.__row, self.__col, row, col,
                                       lambda *args: True)[: -1]
        else:
            text = self.get_text_range(0, 0, row, col,
                                       lambda *args: True)[: -1]
        self.buff.insert_at_cursor(text)
        self.state_ = {PS1: PS1, PS2: PS2}.get(text[-len(PS1): ], None)
        self.__col, self.__row = col, row

    def on_child_exited(self, p_term):
        """
            p_term: la 'Terminal'.

            Se ejecuta cuando 'Octave' termina como consecuencia de haberle
            enviado anteriormente el comando "exit". Llama el metodo
            'Connection.stop'.
        """
        self.__conn.stop()

    def feed_child(self, p_text):
        """
            p_text: una cadena para enviarle a 'Octave'.

            Escribe 'p_text' en la 'Terminal' como si el usuario lo hubiera
            entrado por teclado.
        """
        gtk.gdk.threads_enter()
        vte.Terminal.feed_child(self, p_text)
        gtk.gdk.threads_leave()
