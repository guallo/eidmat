from toolbar.context_toolbar import ContextToolbar


class WSpaceToolbar(ContextToolbar):
    """
        Barra de herramientas del 'Workspace'. Esta es la barra de
        herramientas que muestra la aplicacion cuando el 'Workspace'
        es el elemento activo.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'WSpaceToolbar'.

            Crea un nuevo 'WSpaceToolbar'.
        """
        ContextToolbar.__init__(self, p_mwindow)

        self._cut.set_sensitive(False)
        self._paste.set_sensitive(False)

        self.show_all()

    def on_copy_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            Se ejecuta cuando el usuario da click en el boton 'Copy'.
            Llama el metodo 'Workspace.copy'.
        """
        self._mwindow.get_wspace().copy()

    def on_paste_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            No esta implementado aun.
        """
