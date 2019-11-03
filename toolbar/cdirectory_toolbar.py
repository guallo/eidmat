from toolbar.context_toolbar import ContextToolbar


class CDirectoryToolbar(ContextToolbar):
    """
        Barra de herramientas del 'CurrentDirectory'. Esta es la barra de
        herramientas que muestra la aplicacion cuando el 'CurrentDirectory'
        es el elemento activo.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un 'CDirectoryToolbar'.

            Crea un nuevo 'CDirectoryToolbar'.
        """
        ContextToolbar.__init__(self, p_mwindow)

        self.show_all()

    def on_cut_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            No esta implementado aun.
        """

    def on_copy_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            No esta implementado aun.
        """

    def on_paste_clicked(self, p_butt):
        """
            p_butt: el 'gtk.ToolButton' que recibio la sennal.

            No esta implementado aun.
        """
