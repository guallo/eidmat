import gtk

from util.save_dialog import SaveDialog


class WorkspaceSaveDialog(SaveDialog):
    """
        Cuadro de dialogo que permite indicar el archivo en el cual guardar
        las variables del 'Workspace'.
    """
    def __init__(self, p_parent, p_curdir):
        """
            p_parent: un 'gtk.Window' que es la ventana principal.
            p_curdir: una cadena que representa el camino del directorio
                      actual del usuario.

            Retorna:  un 'WorkspaceSaveDialog'.

            Crea un nuevo 'WorkspaceSaveDialog'.
        """
        filters = []

        filter_ = gtk.FileFilter()
        filter_.set_name("All Files")
        filter_.add_pattern("*")
        filters.append(filter_)

        filter_ = gtk.FileFilter()
        filter_.set_name("VAR-files (*.var)")
        filter_.add_pattern("*.var")
        filters.append(filter_)

        SaveDialog.__init__(self, "Save to VAR-File:", p_parent, p_curdir,
                                  "eidmat.var", filters, filter_)
