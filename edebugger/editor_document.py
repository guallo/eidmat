import os
import gtk  # Solo para tipo.
import gobject
import gtksourceview2

from edebugger.editor_document_loader import EditorDocumentLoader
from edebugger.editor_document_saver import EditorDocumentSaver


class EditorDocument(gtksourceview2.Buffer):
    """
        Clase que representa un documento.
    """

    __gsignals__ = {"name_changed": (gobject.SIGNAL_RUN_LAST,
                                     gobject.TYPE_NONE,
                                     (bool, )),
                    "saving":       (gobject.SIGNAL_RUN_LAST,
                                     gobject.TYPE_NONE,
                                     (str, )),
                    "loading":      (gobject.SIGNAL_RUN_LAST,
                                     gobject.TYPE_NONE,
                                     (str, )),
                    "saved":        (gobject.SIGNAL_RUN_LAST,
                                     gobject.TYPE_NONE,
                                     ()),
                    "loaded":       (gobject.SIGNAL_RUN_LAST,
                                     gobject.TYPE_NONE,
                                     ())
                    }

    def __init__(self, p_name, p_path=None):
        """
            p_name:  una cadena que representa el nombre del documento.
            p_path:  una cadena que representa la direccion del documento
                     o None si es un documento vacio.

            Retorna: un EditorDocument.

            Crea un nuevo EditorDocument.
        """

        assert (type(p_name) == str and p_name)
        assert ((p_path == None) or
                (type(p_path) == str and os.path.isabs(p_path)))

        gtksourceview2.Buffer.__init__(self)

        self.__name = p_name
        self.__path = p_path
        self.__mtime = 0
        self.__ask = True  # Si se preguntara que hacer cuando el documento sea modificado externamente.

        self.set_max_undo_levels(-1)

    def get_name(self):
        """
            Retorna: una cadena.

            Devuelve el nombre del documento.
        """

        return self.__name

    def get_path(self):
        """
            Retorna: una cadena o None.

            Devuelve la direccion del documento si es que tiene,
            None en caso contrario.
        """

        return self.__path

    def get_ask(self):
        """
            Retorna: un boolean.

            Devuelve True si se tiene que notificar al usuario cuando
            el documento sea modificado externamente, False en caso
            contrario.
        """

        return self.__ask

    def set_name(self, p_name):
        """
            p_name: una cadena.

            Establece a p_name como nombre del documento.
            Se emite la sennal "name_changed" de EditorDocument,
            pasando como parametro si la extension de p_name es
            ".m" o no.
        """

        assert (type(p_name) == str and p_name)

        self.__name = p_name

        is_m = os.path.splitext(p_name)[1] == ".m"
        self.emit("name_changed", is_m)

    def set_path(self, p_path):
        """
            p_path: una cadena.

            Establece a p_path como direccion del documento.
        """

        assert (type(p_path) == str and os.path.isabs(p_path))

        self.__path = p_path

    def set_mtime(self, p_mtime):
        """
            p_mtime: un entero que representa la fecha en segundos
                     de la ultima modificacion.

            Establece a p_mtime como fecha de la ultima modificacion
            del documento.
        """

        assert ((type(p_mtime) in (long, int)) and
                (p_mtime >= self.__mtime or not p_mtime))

        self.__mtime = p_mtime

    def set_ask(self, p_ask):
        """
            p_ask: un boolean.

            Si p_ask es True se le notificara al usuario
            cuando el documento sea modificado externamente,
            sino, no se le avisara.
        """

        assert (type(p_ask) == bool)

        self.__ask = p_ask

    def get_all_text(self):
        """
            Retorna: una cadena.

            Devuelve todo el texto del documento.
        """

        start, end = self.get_bounds()

        return self.get_text(start, end, include_hidden_chars=True)

    def get_all_slice(self):
        """
            Retorna: una cadena.

            Devuelve todo el contenido del documento.
        """

        start, end = self.get_bounds()

        return self.get_slice(start, end, include_hidden_chars=True)

    def was_externally_modified(self):
        """
            Retorna: un boolean.

            Devuelve True si el documento fue modificado externamente,
            es decir, que la modificacion no fue mediante el EditorDebugger,
            devuelve False en caso contrario.
        """

        path = self.__path

        if not path:
            return False

        try:
            mtime = os.stat(path).st_mtime
            if type(mtime) not in (float, long, int):
                return False
            return int(mtime) > self.__mtime

        except:
            return False

    def was_deleted(self):
        """
            Retorna: un boolean.

            Devuelve True si el documento fue borrado
            del disco duro, False en caso contrario.
        """

        return (self.__path and not os.access(self.__path, os.F_OK))

    def is_unsaved(self):
        """
            Retorna: un boolean.

            Devuelve True si el documento esta modificado
            o fue modificado externamente o fue eliminado
            del disco duro, False en caso contrario.
        """

        return (self.get_modified() or
                self.was_externally_modified() or
                self.was_deleted())

    def load(self, p_create, p_window):
        """
            p_create: un boolean que indica si el documento
                      se va a cargar por primera vez.
            p_window: un gtk.Window o None.

            Retorna:  True si el documento se cargo,
                      False en caso contrario.

            Trata de cargar el documento llamando el
            metodo EditorDocumentLoader.load().
        """

        assert (type(p_create) == bool)
        assert (p_window == None or isinstance(p_window, gtk.Window))

        return EditorDocumentLoader(self, p_create, p_window).load()

    def save(self, p_path, p_window):
        """
            p_path:   una cadena que representa la direccion
                      donde salvar el documento.
            p_window: un gtk.Window o None.

            Retorna:  True si el documento se salvo,
                      False en caso contrario.

            Trata de salvar el documento llamando
            el metodo EditorDocumentSaver.save().
        """

        assert (type(p_path) == str and os.path.isabs(p_path))
        assert (p_window == None or isinstance(p_window, gtk.Window))

        return EditorDocumentSaver(self, p_path, p_window).save()
