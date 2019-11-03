import gtk

from util.open_dialog import OpenDialog


class WorkspaceImportDialog(OpenDialog):
    """
        Cuadro de dialogo que permite la seleccion de un archivo a importar
        hacia el 'Workspace'.
    """
    def __init__(self, p_parent, p_curdir):
        """
            p_parent: un 'gtk.Window' que es la ventana principal.
            p_curdir: una cadena que representa el camino del directorio
                      actual del usuario.

            Retorna:  un 'WorkspaceImportDialog'.

            Crea un nuevo 'WorkspaceImportDialog'.
        """
        filters = []

        filter_ = gtk.FileFilter()
        filter_.set_name("All Files")
        filter_.add_pattern("*")
        filters.append(filter_)

        filter_ = gtk.FileFilter()
        filter_.set_name("Recognized Data Files")
        filter_.add_pattern("*.var")
        filter_.add_pattern("*.mat")
        filters.append(filter_)

        filter_ = gtk.FileFilter()
        filter_.set_name("EIDMAT Data File (*.var)")
        filter_.add_pattern("*.var")
        filters.append(filter_)

        filter_ = gtk.FileFilter()
        filter_.set_name("MATLAB Data File (*.mat)")
        filter_.add_pattern("*.mat")
        filters.append(filter_)

        OpenDialog.__init__(self, "Import Data", p_parent, p_curdir, filters,
                                                           filters[1])
