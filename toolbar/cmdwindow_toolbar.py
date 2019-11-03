from toolbar.context_toolbar import ContextToolbar


class CMDWindowToolbar(ContextToolbar):
    """
        Barra de herramientas del 'CommandWindow'. Esta es la barra de
        herramientas que muestra la aplicacion cuando el 'CommandWindow'
        es el elemento activo.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CMDWindowToolbar'.

            Crea un nuevo 'CMDWindowToolbar'.
        """
        ContextToolbar.__init__(self, p_mwindow)

        self.show_all()

    def on_cut_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando el usuario da click en el boton 'Cut'.
            Llama el metodo 'CommandWindow.cut'.
        """
        self._mwindow.get_cmdwindow().cut()

    def on_copy_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando el usuario da click en el boton 'Copy'.
            Llama el metodo 'CommandWindow.copy'.
        """
        self._mwindow.get_cmdwindow().copy()

    def on_paste_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando el usuario da click en el boton 'Paste'.
            Llama el metodo 'CommandWindow.paste'.
        """
        self._mwindow.get_cmdwindow().paste()
