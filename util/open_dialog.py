import gtk


class OpenDialog(gtk.FileChooserDialog):
    """
        Clase base para los cuadros de dialogo abrir.
    """
    def __init__(self, p_title, p_parent, p_curdir, p_filters, p_curfilt=None):
        """
            p_title:   un cadena que es el titulo del dialogo.
            p_parent:  un 'gtk.Window' a tomar como padre del dialogo.
            p_curdir:  una cadena que representa el directorio que mostrara
                       inicialmente el dialogo.
            p_filters: una 'list'(lista) de 'gtk.FileFilter'(filtros) que
                       mostara el dialogo.
            p_curfilt: un 'gtk.FileFilter'(filtro) que sera el filtro
                       predeterminado.

            Retorna:   un nuevo 'OpenDialog'.

            Crea un nuevo 'OpenDialog'.
        """
        gtk.FileChooserDialog.__init__(self, p_title, p_parent,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_OPEN, gtk.RESPONSE_OK,
                                       gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

        self.set_default_response(gtk.RESPONSE_OK)
        self.set_current_folder(p_curdir)

        for filter_ in p_filters:
            self.add_filter(filter_)

        if p_curfilt:
            self.set_filter(p_curfilt)

    def run(self, p_block=False):
        """
            p_block: un 'boolean'.

            Retorna: una lista('list') con la(s) direccion(es) del archivo(s)
                     que se quiere(n) abrir o 'False' si se cancelo la accion.

            Muestra el dialogo de abrir('OpenDialog'). Si 'p_block' es 'True'
            el dialogo se muestra entre 'gtk.gdk.threads_enter()' y
            'gtk.gdk.threads_leave()'.
        """
        if p_block:
            gtk.gdk.threads_enter()

        result = False
        if gtk.Dialog.run(self) == gtk.RESPONSE_OK:
            if self.get_select_multiple():
                result = self.get_filenames()
            else:
                result = self.get_filename()
        self.destroy()

        if p_block:
            gtk.gdk.threads_leave()

        return result
