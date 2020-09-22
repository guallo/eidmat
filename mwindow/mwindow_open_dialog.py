import gtk

from util.open_dialog import OpenDialog


class MWindowOpenDialog(OpenDialog):
    """
        Cuadro de dialogo que permite seleccionar los archivos a abrir.
    """
    def __init__(self, p_parent, p_curdir):
        """
            p_parent: un 'gtk.Window' que es la ventana principal.
            p_curdir: una cadena que representa el camino del directorio
                      actual del usuario.

            Retorna:  un 'MWindowOpenDialog'.

            Crea un nuevo 'MWindowOpenDialog'.
        """
        filters = []

        filter_ = gtk.FileFilter()
        filter_.set_name("All Files")
        filter_.add_pattern("*")
        filters.append(filter_)

        filter_ = gtk.FileFilter()
        filter_.set_name("EIDMAT files")
        filter_.add_pattern("*.m")
        filter_.add_pattern("*.var")
        filter_.add_pattern("*.mat")
        filter_.add_pattern("*.eidmat")
        filters.append(filter_)

        filter_ = gtk.FileFilter()
        filter_.set_name("M-files (*.m)")
        filter_.add_pattern("*.m")
        filters.append(filter_)

        filter_ = gtk.FileFilter()
        filter_.set_name("EIDMAT Data File (*.var)")
        filter_.add_pattern("*.var")
        filters.append(filter_)

        filter_ = gtk.FileFilter()
        filter_.set_name("MATLAB Data File (*.mat)")
        filter_.add_pattern("*.mat")
        filters.append(filter_)

        filter_ = gtk.FileFilter()
        filter_.set_name("Deployment projects (*.eidmat)")
        filter_.add_pattern("*.eidmat")
        filters.append(filter_)

        OpenDialog.__init__(self, "Open", p_parent, p_curdir, filters,
                                                           filters[1])
        self.set_select_multiple(True)
