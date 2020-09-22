import gtk

from util.open_dialog import OpenDialog


class EditorOpenDialog(OpenDialog):
    """
        Dialogo de seleccion de archivos.
    """

    def __init__(self, p_parent, p_curdir):
        """
            p_parent: un gtk.Window o None.
            p_curdir: una cadena que representa el camino del directorio
                      que mostrara inicialmente el dialogo.

            Retorna:  un EditorOpenDialog.

            Crea un nuevo EditorOpenDialog.
        """

        assert (p_parent == None or isinstance(p_parent, gtk.Window))
        assert (type(p_curdir) == str)

        filters = []

        filter_ = gtk.FileFilter()
        filter_.set_name("All Files")
        filter_.add_pattern("*")
        filters.append(filter_)

        filter_ = gtk.FileFilter()
        filter_.set_name("M-files (*.m)")
        filter_.add_pattern("*.m")
        filters.append(filter_)

        OpenDialog.__init__(self, "Open File", p_parent, p_curdir, filters,
                                                                   filter_)
        self.set_select_multiple(True)
