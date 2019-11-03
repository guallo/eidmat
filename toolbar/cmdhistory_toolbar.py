from toolbar.context_toolbar import ContextToolbar


class CMDHistoryToolbar(ContextToolbar):
    """
        Barra de herramientas del 'CommandHistory'. Esta es la barra de
        herramientas que muestra la aplicacion cuando el 'CommandHistory'
        es el elemento activo.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDHistoryToolbar'.

            Crea un nuevo 'CMDHistoryToolbar'.
        """
        ContextToolbar.__init__(self, p_mwindow)

        self._paste.set_sensitive(False)

        self.show_all()

    def on_cut_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando el usuario da click en el boton 'Cut'.
            Llama el metodo 'CommandHistory.cut'.
        """
        self._mwindow.get_cmdhistory().cut()

    def on_copy_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando el usuario da click en el boton 'Copy'.
            Llama el metodo 'CommandHistory.copy'.
        """
        self._mwindow.get_cmdhistory().copy()
