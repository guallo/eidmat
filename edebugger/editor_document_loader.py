import os
import gtk

from util.message import Message


class EditorDocumentLoader:
    """
        Clase que permite cargar un documento.
    """

    def __init__(self, p_doc, p_create, p_window):
        """
            p_doc:    un EditorDocument a cargar.
            p_create: True si p_doc se cargara por primera vez,
                      False si se desea recargar su contenido.
            p_window: un gtk.Window o None.

            Retorna:  un EditorDocumentLoader.

            Crea un nuevo EditorDocumentLoader.
        """

        #assert (type(p_doc) == EditorDocument) FIXME: import loop
        assert (type(p_create) == bool)
        assert (p_window == None or isinstance(p_window, gtk.Window))

        self.__doc = p_doc
        self.__create = p_create
        self.__window = p_window
        self.__used = False

    def load(self):
        """
            Retorna: True si se cargo el documento, False en caso contrario.

            Trata de cargar el documento.
        """

        assert (not self.__used)

        self.__used = True

        doc = self.__doc
        path = doc.get_path()
        create = self.__create

        if not path:
            return True

        try:
            file_ = open(path, "r")

            doc.emit("loading", path)

            text = file_.read()
            file_.close()

        except IOError, error:
            title = ("Reverting Failed", "Opening Failed")[create]

            if not os.access(path, os.F_OK):
                if create:
                    msg = "could not be find.\nPlease check that you typed " \
                          "the location correctly and try again."
                else:
                    msg = "could not be revert.\nPerhaps it has recently "   \
                          "been deleted."

            elif not os.access(path, os.R_OK):
                if create:
                    msg = "could not be open.\nYou do not have the "         \
                          "permissions necessary to open the file."
                else:
                    msg = "could not be revert.\nPermission denied."

            else:
                if create:
                    msg = "unexpected error.\n" + str(error)
                else:
                    msg = "could not be revert.\n" + str(error)

            Message(gtk.STOCK_DIALOG_ERROR, "%s\n\n%s" %(path, msg),
                                         title, self.__window).run()
            return False

        doc.begin_not_undoable_action()
        doc.set_text(text)
        doc.set_modified(False)
        doc.end_not_undoable_action()

        doc.set_mtime(self.get_mtime())
        doc.place_cursor(doc.get_start_iter())

        doc.emit("loaded")

        return True

    def get_mtime(self):
        """
            Retorna: un entero.

            Devuelve el tiempo en segundos de la ultima
            modificacion en disco del documento.
        """

        try:
            return int(os.stat(self.__doc.get_path()).st_mtime)
        except:
            return 0
