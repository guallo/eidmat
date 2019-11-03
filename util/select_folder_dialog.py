import gtk


class SelectFolderDialog(gtk.FileChooserDialog):
    """
        Clase base para los cuadros de dialogo de seleccion de carpetas.
    """
    def __init__(self, p_title, p_parent, p_curdir):
        """
            p_title:   un cadena que es el titulo del dialogo.
            p_parent:  un 'gtk.Window' a tomar como padre del dialogo.
            p_curdir:  una cadena que representa el directorio que mostrara
                       inicialmente el dialogo.

            Retorna:   un nuevo 'SelectFolderDialog'.

            Crea un nuevo 'SelectFolderDialog'.
        """
        gtk.FileChooserDialog.__init__(self, p_title, p_parent,
                                       gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                       (gtk.STOCK_OK, gtk.RESPONSE_OK,
                                        gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

        self.set_default_response(gtk.RESPONSE_OK)
        self.set_current_folder(p_curdir)

    def run(self, p_block=False):
        """
            p_block: un 'boolean'.

            Retorna: la direccion de la carpeta seleccionada o 'False' si se
                     cancelo la accion.

            Muestra el dialogo de seleccion de carpetas('SelectFolderDialog').
            Si 'p_block' es 'True' el dialogo se muestra entre
            'gtk.gdk.threads_enter()' y 'gtk.gdk.threads_leave()'.
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
