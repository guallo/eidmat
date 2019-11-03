import gtk


class SaveDialog(gtk.FileChooserDialog):
    """
        Clase base para los cuadros de dialogo guardar.
    """
    def __init__(self, p_title, p_parent, p_curdir, p_curname, p_filters,
                       p_curfilt=None):
        """
            p_title:   un cadena que es el titulo del dialogo.
            p_parent:  un 'gtk.Window' a tomar como padre del dialogo.
            p_curdir:  una cadena que representa el directorio que mostrara
                       inicialmente el dialogo.
            p_curname: una cadena que es el nombre por defecto del archivo a
                       guardar.
            p_filters: una 'list'(lista) de 'gtk.FileFilter'(filtros) que
                       mostara el dialogo.
            p_curfilt: un 'gtk.FileFilter'(filtro) que sera el filtro
                       predeterminado.

            Retorna:   un nuevo 'SaveDialog'.

            Crea un nuevo 'SaveDialog'.
        """
        gtk.FileChooserDialog.__init__(self, p_title, p_parent,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_SAVE, gtk.RESPONSE_OK,
                                       gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

        self.set_default_response(gtk.RESPONSE_OK)
        self.set_do_overwrite_confirmation(True)
        self.set_current_folder(p_curdir)
        self.set_current_name(p_curname)

        for filter_ in p_filters:
            self.add_filter(filter_)

        if p_curfilt:
            self.set_filter(p_curfilt)

    def run(self, p_block=False):
        """
            p_block: un 'boolean'.

            Retorna: la direccion del archivo donde se quiere guardar o 'False'
                     si se cancelo la accion.

            Muestra el dialogo de guardar('SaveDialog'). Si 'p_block' es 'True'
            el dialogo se muestra entre 'gtk.gdk.threads_enter()' y
            'gtk.gdk.threads_leave()'.
        """
        if p_block:
            gtk.gdk.threads_enter()

        result = False
        if gtk.Dialog.run(self) == gtk.RESPONSE_OK:
            result = self.get_filename()
        self.destroy()

        if p_block:
            gtk.gdk.threads_leave()

        return result
