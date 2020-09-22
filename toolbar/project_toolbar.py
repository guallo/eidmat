from toolbar.context_toolbar import ContextToolbar


class ProjectToolbar(ContextToolbar):
    """
        Barra de herramientas del 'ProjectTree'. Esta es la barra de
        herramientas que muestra la aplicacion cuando el 'ProjectTree'
        es el elemento activo.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'ProjectToolbar'.

            Crea un nuevo 'ProjectToolbar'.
        """
        ContextToolbar.__init__(self, p_mwindow)

        self._copy.set_sensitive(False)
        self._paste.set_sensitive(False)
        self._cut.set_sensitive(False)

        self.show_all()

    def on_copy_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            No esta implementado aun..
        """
        
    def on_paste_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            No esta implementado aun.
        """

    def on_cut_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            No esta implementado aun.
        """
