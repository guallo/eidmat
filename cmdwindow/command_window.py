import gtk
import pango
import gobject

from cmdwindow.command_window_menu import CommandWindowMenu
from cmdwindow.command_window_buffer import CommandWindowBuffer
from menubar.cmdwindow_menu_bar import CMDWindowMenuBar
from toolbar.cmdwindow_toolbar import CMDWindowToolbar
from cmd.clear_cmdwindow import ClearCMDWindow
from util.confirm import Confirm


class CommandWindow(gtk.TextView):
    """
        La ventana de comandos de la aplicacion. Es a traves de esta que el
        usuario envia los comandos a 'Octave' y recibe informacion del mismo.
    """
    def __init__(self, p_mwindow, p_parent, p_conn, p_cmdhistory):
        """
            p_mwindow:    un 'MainWindow'.
            p_parent:     un 'gtk.Window' que es la ventana principal.
            p_conn:       un 'Connection' que es la conexion con Octave.
            p_cmdhistory: un 'CommandHistory'.

            Retorna:      un 'CommandWindow'.

            Retorna un nuevo 'CommandWindow'.
        """
        self.__buff = CommandWindowBuffer()
        gtk.TextView.__init__(self, self.__buff)

        self.__mwindow = p_mwindow
        self.__parent = p_parent
        self.__conn = p_conn
        self.__history = p_cmdhistory
        self.__ps1 = ">> "
        self.__ps2 = ""
        self.__confirmed_clear = False
        self.__mbar = CMDWindowMenuBar(p_mwindow)
        self.__tbar = CMDWindowToolbar(p_mwindow)

        self.modify_font(pango.FontDescription("monospace Expanded 10"))
        self.set_left_margin(3)

        self.connect("key-press-event", self.key_press_event)
        self.connect("button-press-event", self.button_press_event)
        self.connect("focus-in-event", lambda p_cmdwindow, p_event:
                                              self.activate())
        self.connect_after("realize", self.on_realize)

        gobject.timeout_add(200, lambda: not self.update_appearance())

    def get_ps1(self):
        """
            Retorna: una cadena que es el 'prompt 1' de 'Octave'.

            Retorna la cadena que representa el 'prompt 1' de 'Octave'. Este
            prompt es el que muestra 'Octave' cuando esta listo y esperando por
            nuevos comandos.
        """
        return self.__ps1

    def get_ps2(self):
        """
            Retorna: una cadena que es el 'prompt 2' de 'Octave'.

            Retorna la cadena que representa el 'prompt 2' de 'Octave'. Este
            prompt es el que muestra 'Octave' cuando esta esperando que se
            complete una sentencia determinada.
        """
        return self.__ps2

    def key_press_event(self, p_cmdwindow, p_event):
        """
            p_cmdwindow:  el 'CommandWindow'.
            p_event:      el evento que desencadeno la sennal.

            Este metodo es llamado cuando se presiona una tecla sobre
            'p_cmdwindow'. Una de sus funcionalidades es evitar que se
            modifique la zona no editable del 'CommandWindow'.

            Ctrl+X:      llama el metodo 'CommandWindow.cut'.
            Ctrl+C:      llama el metodo 'CommandWindow.copy(True)'.
            Ctrl+Insert: llama el metodo 'CommandWindow.copy'.
            Ctrl+L:      llama el metodo 'CommandWindow.clear'.
            Up:          llama el metodo 'CommandWindow.up'.
            Down:        llama el metodo 'CommandWindow.down'.
            Escape:      llama el metodo 'CommandWindow.escape'.
            Enter:       llama el metodo 'CommandWindow.enter'.
            F9:          llama el metodo 'CommandWindow.evaluate'.
            Shift+F10    Muestra el menu emergente 'CommandWindowMenu'.
        """
        ascii = p_event.keyval
        flags = p_event.state

        if ascii in (88, 120, 65379, 108, 76):  # x, X, insert, l, L
            if int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and\
               not int(gtk.gdk.MOD1_MASK & flags):

                return {88: self.cut, 120: self.cut, 65379: self.copy,
                        108: self.clear, 76: self.clear}[ascii]()

        elif ascii == 99 or ascii == 67:  # c, C
            if int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and\
               not int(gtk.gdk.MOD1_MASK & flags):

                return self.copy(True)

        # up izq, down izq, up der, down der, Esc, F9
        elif ascii in (65362, 65364, 65431, 65433, 65307, 65478):
            if not int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and\
               not int(gtk.gdk.MOD1_MASK & flags):

                {65362: self.up, 65364: self.down, 65431: self.up,
                 65433: self.down, 65307: self.escape,
                 65478: self.evaluate}[ascii]()
                return True

        elif ascii == 65293 or ascii == 65421:  # Enter der, Enter izq
            self.enter()
            return True

        elif ascii == 65383:  # Equivalente al click derecho.
            if not int(gtk.gdk.MOD1_MASK & flags) and\
               not int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags):

                CommandWindowMenu(self, p_event)
                return True

        elif ascii == 65479:  # F10 Equivalente al click derecho.
            if not int(gtk.gdk.MOD1_MASK & flags) and\
               not int(gtk.gdk.CONTROL_MASK & flags) and\
               int(gtk.gdk.SHIFT_MASK & flags):

                CommandWindowMenu(self, p_event)
                return True

        elif ascii == 65288:  # Backspace.
            if not int(gtk.gdk.MOD1_MASK & flags):

                selection = self.__buff.get_selection_bounds()
                if selection:
                    zone = self.get_selection_zone(selection)
                    if zone == -1:
                        self.__buff.place_cursor(self.__buff.limit)
                    elif zone == 0:
                        self.move_mark_at_limit()

                elif self.get_cursor_zone() == -1:
                    self.__buff.place_cursor(self.__buff.limit)

                self.scroll_to_mark(self.__buff.get_insert(),
                                    0.0, True, 1.0, 0.5)

        elif ascii == 65535:  # Delete.
            if not int(gtk.gdk.MOD1_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags):

                selection = self.__buff.get_selection_bounds()
                if selection:
                    zone = self.get_selection_zone(selection)
                    if zone == -1:
                        self.__buff.place_cursor(self.__buff.limit)
                        self.scroll_to_mark(self.__buff.get_insert(),
                                            0.0, False)
                        return True
                    elif zone == 0:
                        self.move_mark_at_limit()

                elif self.get_cursor_zone() == -1:
                    self.__buff.place_cursor(self.__buff.limit)
                    self.scroll_to_mark(self.__buff.get_insert(), 0.0, False)
                    return True

                self.scroll_to_mark(self.__buff.get_insert(), 0.0, False)

        elif ascii == 65360 or ascii == 65367:  # Home, End
            if not int(gtk.gdk.MOD1_MASK & flags) and\
               not int(gtk.gdk.CONTROL_MASK & flags) and\
               self.get_cursor_zone() == 1:

                pos = {65360: self.__buff.limit,
                       65367: self.__buff.get_char_count()}[ascii]

                if int(gtk.gdk.SHIFT_MASK & flags):
                    self.__buff.move_mark(self.__buff.get_insert(), pos)
                else:
                    self.__buff.place_cursor(pos)

                self.scroll_to_mark(self.__buff.get_insert(),
                                    0.0, True, 0.9, 0.5)
                return True

        # Si la tecla presionada no es ninguna de las que se chequean
        # anteriormente y ademas, esto provoca la insercion de texto en el
        # command window, entonces se verifica que dicha insercion no
        # ocurra en la zona no editable de command window.
        if len(p_event.string):
            selection = self.__buff.get_selection_bounds()
            if selection:
                zone = self.get_selection_zone(selection)
                if zone == -1:
                    self.__buff.place_cursor(self.__buff.get_char_count())
                elif zone == 0:
                    self.move_mark_at_limit()

            elif self.get_cursor_zone() == -1:
                self.__buff.place_cursor(self.__buff.get_char_count())

    def button_press_event(self, p_cmdwindow, p_event):
        """
            p_cmdwindow: el 'CommandWindow'.
            p_event:     el evento que desencadeno la sennal.

            Retorna: 'True' si se presiono click derecho sobre el
                     'CommandWindow'. 'True' causa que se detengan otros
                     manejadores que se invoquen para el evento.

            Se ejecuta cada vez que se presiona un boton del mouse sobre el
            'CommandWindow'. Chequea si ocurrio el click derecho, en ese caso
            lanza el menu emergente('CommandWindowMenu') asociado al
            'CommandWindow'.
        """
        if p_event.button == 3:  # Click derecho.
            CommandWindowMenu(self, p_event)
            return True

    def on_realize(self, p_cmdwindow):
        """
            p_cmdwindow: el 'CommandWindow'.

            Se ejecuta cuando se muestra el 'CommandWindow' al inicio de la
            aplicacion. Establece el metodo 'CommandWindow.update_paste' como
            manejador de la senal 'ownwer-change' del 'gtk.Clipboard'.
        """
        self.update_paste()

        clip = self.get_clipboard("CLIPBOARD")
        clip.connect("owner-change", lambda p_clip, p_event:
                                            self.update_paste())

    def get_selection_zone(self, p_selection):
        """
            p_selection: una tupla('tuple') con dos enteros('int') que
                         representan el inicio y fin de una seleccion en el
                         'CommandWindow'.

            Retorna:     un entero('int') que puede ser:

                         '-1' si la seleccion esta completamente en la parte no
                              editable del 'CommandWindow'.
                          '0' si la seleccion cubre parte de la zona no
                              editable y parte de la zona editable del
                              'CommandWindow'.
                          '1' si la seleccion esta completamente en la parte
                              editable del 'CommandWindow'.

            Retorna un entero('int') que indica la zona en la que se encuentra
            la seleccion comprendida en 'p_selection'.
        """
        if p_selection[0] < self.__buff.limit:
            if p_selection[1] <= self.__buff.limit:
                return -1
            return 0
        return 1

    def get_cursor_zone(self):
        """
            Retorna: un entero('int') que puede ser:

                     '-1' si el cursor esta en la parte no editable del
                          'CommandWindow'.
                      '1' si el cursor esta en la parte editable del
                          'CommandWindow'.

            Retorna un entero('int') que indica la zona en la que se encuentra
            el cursor.
        """
        cursor = self.__buff.get_offset_at_mark(self.__buff.get_insert())
        if cursor < self.__buff.limit:
            return -1
        return 1

    def move_mark_at_limit(self):
        """
            Si una seleccion cubre parte de la zona no editable y parte de la
            editable del 'CommandWindow', enonces dicha seleccion se corre lo
            necesario para que cubra solamente la zona editable que cubria.
        """
        mark1 = self.__buff.get_insert()
        mark2 = self.__buff.get_selection_bound()
        offset1 = self.__buff.get_offset_at_mark(mark1)
        offset2 = self.__buff.get_offset_at_mark(mark2)

        if offset1 < offset2:
            self.__buff.move_mark(mark1, self.__buff.limit)
        else:
            self.__buff.move_mark(mark2, self.__buff.limit)

    def copy(self, p_break=False):
        """
            p_break: un 'boolean'.

            Retorna: 'True' si hay seleccion en el 'CommandWindow'.

            Si hay seleccion en el 'CommandWindow', entonces se copia al
            'gtk.Clipboard' el texto comprendido en la misma, sino, si
            'p_break' es 'True' se interrumpe la tarea actual que este
            haciendo 'Octave'.
        """
        selection = self.__buff.get_selection_bounds()

        if selection:
            text = self.__buff.get_text(selection[0], selection[1], True)
            self.get_clipboard("CLIPBOARD").set_text(text)
            return True

        if p_break:
            self.__buff.limit = self.__buff.get_char_count()
            self.__buff.place_cursor(self.__buff.limit)
            self.__conn.write("\x03")

    def cut(self):
        """
            Retorna: 'True' si hay seleccion.

            Corta el texto comprendido en la parte editable de la seleccion.
        """
        selection = self.__buff.get_selection_bounds()
        if selection:
            zone = self.get_selection_zone(selection)
            if zone == -1:
                return True
            if zone == 0:
                self.move_mark_at_limit()
                selection = (self.__buff.limit, selection[1])

            text = self.__buff.get_text(selection[0], selection[1], True)
            self.get_clipboard("CLIPBOARD").set_text(text)
            self.__buff.delete(selection[0], selection[1])
            self.scroll_to_mark(self.__buff.get_insert(), 0.0, False)
            return True

    def paste(self):
        """
            Pega el contenido del 'gtk.Clipboard' en el 'CommandWindow'.
        """
        text = self.get_clipboard("CLIPBOARD").wait_for_text()
        if text is None:
            return

        buff = self.__buff
        selection = buff.get_selection_bounds()

        if selection:
            zone = self.get_selection_zone(selection)

            if zone == -1:
                buff.place_cursor(buff.get_char_count())
            elif zone == 0:
                self.move_mark_at_limit()
                buff.delete(buff.limit, selection[1])
            else:
                buff.delete(selection[0], selection[1])

        elif self.get_cursor_zone() == -1:
            buff.place_cursor(buff.get_char_count())

        buff.insert_at_cursor(text)
        self.scroll_to_mark(buff.get_insert(), 0.0, False)

    def delete_selection(self):
        """
            Borra el texto comprendido en la parte editable de la seleccion.
        """
        buff = self.__buff
        selection = buff.get_selection_bounds()

        if selection:
            zone = self.get_selection_zone(selection)

            if zone == -1:
                buff.place_cursor(buff.limit)
            elif zone == 0:
                self.move_mark_at_limit()
                buff.delete(buff.limit, selection[1])
            else:
                buff.delete(selection[0], selection[1])

            self.scroll_to_mark(buff.get_insert(), 0.0, False)

    def select_all(self):
        """
            Selecciona todo el texto del 'CommandWindow'.
        """
        buff = self.__buff
        buff.move_mark(buff.get_insert(), 0)
        buff.move_mark(buff.get_selection_bound(), buff.get_char_count())

    def enter(self):
        """
            Envia a 'Octave' el comando actual escrito en el 'CommandWindow'.
        """
        end = self.__buff.get_char_count()
        self.__buff.place_cursor(end)
        text = self.__buff.get_text(self.__buff.limit, end, True) + "\n"
        self.__buff.delete(self.__buff.limit, end)
        self.__conn.write(text)
        self.__history.append(text)

    def escape(self):
        """
            Borra el comando actual escrito en el 'CommandWindow'.
        """
        self.__buff.delete(self.__buff.limit, self.__buff.get_char_count())
        self.__buff.place_cursor(self.__buff.limit)
        self.scroll_to_mark(self.__buff.get_insert(), 0.0, True, 1.0, 0.5)

    def evaluate(self, p_cmd=None):
        """
            p_cmd: una cadena a evaluar.

            Si se especifica 'p_cmd', entonces se evalua, es decir se
            le envia a 'Octave', sino, se evalua el texto comprendido
            en la seleccion que halla en el 'CommandWindow'.
        """
        buff = self.__buff

        if p_cmd:
            buff.place_cursor(buff.limit)
            self.__conn.write(p_cmd)
            self.__history.append(p_cmd)
            return

        selection = buff.get_selection_bounds()
        if selection:
            buff.place_cursor(buff.limit)
            text = buff.get_text(selection[0], selection[1], True) + "\n"
            self.__conn.write(text)
            self.__history.append(text)

    def up(self):
        """
            Busca arriba en el 'CommandHistory' el primer comando que comience
            con lo escrito hasta el momento y lo muestra en el 'CommandWindow'.
        """
        buff = self.__buff
        end = buff.get_char_count()
        text = buff.get_text(buff.limit, end, True)
        buff.delete(buff.limit, end)
        buff.insert(buff.limit, self.__history.look_up(text))

    def down(self):
        """
            Busca abajo en el 'CommandHistory' el primer comando que comience
            con lo escrito hasta el momento y lo muestra en el 'CommandWindow'.
        """
        buff = self.__buff
        end = buff.get_char_count()
        text = buff.get_text(buff.limit, end, True)
        buff.delete(buff.limit, end)
        buff.insert(buff.limit, self.__history.look_down(text))

    def clear(self):
        """
            Limpia el 'CommandWindow', es decir, borra todo el texto del mismo.
        """
        if not self.__confirmed_clear:
            resp = Confirm(gtk.STOCK_DIALOG_WARNING,
                           "All text will be cleared from the command window.",
                           "EIDMAT", self.__parent,
                           "Do not show this prompt again.").run()
            if not resp:
                return
            self.__confirmed_clear = resp[0]

        self.__conn.append_command(ClearCMDWindow())

    def update_appearance(self):
        """
            Actualiza la apariencia de los menus y barra de herramientas
            correspondientes al 'CommandWindow', decidiendo cuales de estos
            se mostraran activos o no en dependencia de las acciones que
            se puedan realizar.
        """
        edit_menu = self.__mbar.get_edit()
        tbar = self.__tbar
        selec = self.get_buffer().get_selection_bounds()

        if not selec:
            edit_menu.get_cut().set_sensitive(False)
            edit_menu.get_delete().set_sensitive(False)
            edit_menu.get_copy().set_sensitive(False)

            tbar.get_cut().set_sensitive(False)
            tbar.get_copy().set_sensitive(False)
        else:
            edit_menu.get_copy().set_sensitive(True)

            tbar.get_copy().set_sensitive(True)

            if self.get_selection_zone(selec) == -1:
                edit_menu.get_cut().set_sensitive(False)
                edit_menu.get_delete().set_sensitive(False)

                tbar.get_cut().set_sensitive(False)
            else:
                edit_menu.get_cut().set_sensitive(True)
                edit_menu.get_delete().set_sensitive(True)

                tbar.get_cut().set_sensitive(True)

    def update_paste(self):
        """
            Determina si se activan o no los elementos de menu 'Paste' y el
            boton 'Paste' de la barra de herramientas del 'CommandWindow' en
            dependencia de si hay algo o no en el 'gtk.Clipboard' para pegar.
        """
        edit_menu = self.__mbar.get_edit()
        tbar = self.__tbar

        if not self.has_screen():
            return

        if self.get_clipboard("CLIPBOARD").wait_for_text() is None:
            edit_menu.get_paste().set_sensitive(False)

            tbar.get_paste().set_sensitive(False)
        else:
            edit_menu.get_paste().set_sensitive(True)

            tbar.get_paste().set_sensitive(True)

    def activate(self):
        """
            Resalta el 'CommandWindow' en azul y muestra su barra de menus y
            de herramientas.
        """
        self.__mwindow.set_menu_bar(self.__mbar, self.__tbar, 0)
