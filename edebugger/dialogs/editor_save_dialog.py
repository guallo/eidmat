import gtk

from util.save_dialog import SaveDialog


class EditorSaveDialog(SaveDialog):
    """
        Dialogo para salvar archivos.
    """

    def __init__(self, p_parent, p_curdir, p_curname):
        """
            p_parent:  un gtk.Window o None.
            p_curdir:  una cadena que representa el camino del directorio
                       que mostrara inicialmente el dialogo.
            p_curname: una cadena que representa el nombre por defecto del
                       archivo a guardar.

            Retorna:   un EditorSaveDialog.

            Crea un nuevo EditorSaveDialog.
        """
        assert (p_parent == None or isinstance(p_parent, gtk.Window))
        assert (type(p_curdir) == str)
        assert (type(p_curname) == str)

        filters = []

        filter_ = gtk.FileFilter()
        filter_.set_name("All Files")
        filter_.add_pattern("*")
        filters.append(filter_)

        filter_ = gtk.FileFilter()
        filter_.set_name("M-files (*.m)")
        filter_.add_pattern("*.m")
        filters.append(filter_)

        SaveDialog.__init__(self, "Save file as:", p_parent, p_curdir,
                                          p_curname, filters, filter_)
