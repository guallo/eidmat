import gtk


class ContextMenuBar(gtk.MenuBar):
    """
        Clase base para todas las barras de menu contextuales de la
        aplicacion, es decir, que todas las barras de menu principales
        de la aplicacion heredan de 'ContextMenuBar'.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'ContextMenuBar'.

            Crea un nuevo 'ContextMenuBar'.
        """
        gtk.MenuBar.__init__(self)

        self._mwindow = p_mwindow

        self.connect("button-press-event", self.on_button_press_event)

    def append_item(self, p_text, p_submenu):
        """
            p_text:    una cadena a mostrar por un 'gtk.MenuItem'.
            p_submenu: un 'Menu' a poner como submenu de un 'gtk.MenuItem'.

            Crea y adiciona al 'ContextMenuBar'(barra de menu contextual) un
            'gtk.MenuItem'(elemento de menu) con el texto 'p_text' y que tenga
            como submenu a 'p_submenu'.
        """
        item = gtk.MenuItem(p_text)
        item.set_submenu(p_submenu)
        self.append(item)

    def on_button_press_event(self, p_mbar, p_event):
        """
            p_mbar:  el 'ContextMenuBar' que recibio la sennal.
            p_event: el evento que desencadeno la sennal.

            Retorna: 'True' si se presiono click derecho. Retornar 'True'
                     causa que se detengan otros manejadores que se invoquen
                     para el evento.

            Se ejecuta cada vez que se presiona un boton del mouse sobre
            'p_mbar'. Chequea si ocurrio el click derecho, en ese caso lanza
            el menu emergente 'PopupMenu'.
        """
        if p_event.button == 3:
            self._mwindow.get_popup_menu().popup3(p_event)
            return True
