import os
import gtk

from util.menu import Menu


class CommandWindowMenu(Menu):
    """
        Representa el menu emergente asociado al 'CommandWindow'.
        Es el menu que se muestra cuando se presiona click derecho
        sobre el 'CommandWindow'.
    """
    def __init__(self, p_cmdwindow, p_event):
        """
            p_cmdwindow: el 'CommandWindow'.
            p_event:     el evento que provoco que se muestre el
                         'CommandWindowMenu'.

            Retorna:     un 'CommandWindowMenu'.

            Crea un nuevo 'CommandWindowMenu'.
        """
        Menu.__init__(self)

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

        self.__command_win = p_cmdwindow
        self.__event = p_event
        selection = p_cmdwindow.get_buffer().get_selection_bounds()

        # Evaluate Selection
        eval_item = self.create_item("normal", "_Evaluate Selection",
                                     p_accel="F9")
        eval_item.connect("activate", self.on_eval_activate)

        # Separator
        self.create_item("separator")

        # Cut
        img = os.path.join(root, "images", "cut.png")
        cut_item = self.create_item("image", "Cu_t", img, "Ctrl+X")
        cut_item.connect("activate", self.on_cut_activate)

        # Copy
        img = os.path.join(root, "images", "copy.png")
        copy_item = self.create_item("image", "_Copy", img, "Ctrl+C")
        copy_item.connect("activate", self.on_copy_activate)

        # Paste
        img = os.path.join(root, "images", "paste.png")
        paste_item = self.create_item("image", "_Paste", img, "Ctrl+V")
        paste_item.connect("activate", self.on_paste_activate)

        # Delete
        delete_item = self.create_item("image", "_Delete", gtk.STOCK_DELETE)
        delete_item.connect("activate", self.on_delete_activate)

        # Separator
        self.create_item("separator")

        # Select All
        select_item = self.create_item("normal", "Select _All",
                                       p_accel="Ctrl+A")
        select_item.connect("activate", self.on_select_activate)

        # Separator
        self.create_item("separator")

        # Clear Command Window
        clear_item = self.create_item("normal", "Clear Command _Window",
                                      p_accel="Ctrl+L")
        clear_item.connect("activate", self.on_clear_activate)

        if self.get_clipboard("CLIPBOARD").wait_for_text() is None:
            paste_item.set_sensitive(False)

        if not selection:
            eval_item.set_sensitive(False)
            cut_item.set_sensitive(False)
            copy_item.set_sensitive(False)
            delete_item.set_sensitive(False)

        elif p_cmdwindow.get_selection_zone(selection) == -1:
            cut_item.set_sensitive(False)
            delete_item.set_sensitive(False)

        if p_event.type == gtk.gdk.BUTTON_PRESS:
            self.popup(None, None, None, 3, p_event.time)
        else:
            self.popup(None, None, self._func, 3, p_event.time)

    def _func(self, p_menu):
        """
            p_menu:  el 'CommandWindowMenu'.

            Retorna: una tupla('tuple') en la cual sus dos primeros elementos
                     son las coordenas 'x' e 'y' donde se mostrara 'p_menu' y,
                     como tercer elemento tiene 'True' lo que provoca que
                     'p_menu' se muestre completamente dentro de la pantalla.

            Cuando 'CommandWindowMenu' es invocado por el teclado, este metodo
            determina la posicion donde debe mostrarse el mismo. En caso de
            que el cursor se vea el menu saldra en dicha posicion, sino, se
            mostrara en el centro del 'CommandWindow'.
        """
        command_win = self.__command_win
        buff = command_win.get_buffer()

        x1, y1 = self.__event.window.get_root_origin()  # Coords de la ventana.

        # Coords del commandwindow.
        rect1 = command_win.get_allocation()
        x2, y2 = rect1.x, rect1.y

        # Coords en buffer del cursor.
        buff.get_semaphore().acquire()
        cursor = buff.get_iter_at_mark(buff.get_insert())
        rect2 = command_win.get_iter_location(cursor)
        buff.get_semaphore().release()
        xr2, yr2 = rect2.x, rect2.y

        # Coords en window del cursor.
        x3, y3 = command_win.buffer_to_window_coords(gtk.TEXT_WINDOW_WIDGET,
                                                     xr2, yr2)

        # Coordenadas en buffer del area visible del commandwindow.
        rect3 = command_win.get_visible_rect()
        xr3, yr3 = rect3.x, rect3.y
        wr3, hr3 = rect3.width, rect3.height

        # if (el cursor no se ve):
        if not (xr3 <= xr2 <= (xr3 + wr3) and yr3 <= yr2 <= (yr3 + hr3)):
            return (x1 + x2 + (rect1.width / 2) - 33,
                    y1 + y2 + (rect1.height / 2) - 41, True)
        return (x1 + x2 + x3 + 5, y1 + y2 + y3 + 42, True)

    def create_item(self, p_type, p_text=None, p_stock=None, p_accel=None):
        """
            p_type:  una cadena que representa el tipo de elemento de menu a
                     crear. 'p_type' puede ser "normal", "image", "check",
                     "radio" o "separator".
            p_text:  una cadena a mostrar por el elemento de menu.
            p_stock: una cadena que represente un 'stock de gtk' o una
                     direccion de una imagen a mostrar por el elemento de menu.
            p_accel: una cadena que representa la combinacion de teclas que
                     activa a dicho elemento de menu. 'p_accel' es lo ultimo
                     que se muestra en el elemento de menu.

            Retorna: un 'gtk.MenuItem' en dependencia de los parametros dados.

            Crea, adiciona y retorna un elemento de menu segun los parametros
            dados.
        """
        item = Menu.create_item(self, p_type, p_text, p_stock, p_accel)
        item.show_all()
        self.append(item)
        return item

    def on_eval_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Evaluate Selection'. Llama el metodo 'CommandWindow.evaluate'.
        """
        self.__command_win.evaluate()

    def on_cut_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Cut'.
            Llama el metodo 'CommandWindow.cut'.
        """
        self.__command_win.cut()

    def on_copy_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Copy'.
            Llama el metodo 'CommandWindow.copy'.
        """
        self.__command_win.copy()

    def on_paste_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Paste'.
            Llama el metodo 'CommandWindow.paste'.
        """
        self.__command_win.paste()

    def on_delete_activate(self, p_item):
        """
            p_item: el 'gtk.ImageMenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu 'Delete'.
            Llama el metodo 'CommandWindow.delete_selection'.
        """
        self.__command_win.delete_selection()

    def on_select_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Select All'. Llama el metodo 'CommandWindow.select_all'.
        """
        self.__command_win.select_all()

    def on_clear_activate(self, p_item):
        """
            p_item: el 'gtk.MenuItem' que recibio la sennal.

            Se ejecuta cuando el usuario activa el elemento de menu
            'Clear Command Window'. Llama el metodo 'CommandWindow.clear'.
        """
        self.__command_win.clear()
