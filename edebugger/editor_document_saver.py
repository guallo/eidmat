import os
import gtk

from util.message import Message


class EditorDocumentSaver:
    """
        Clase que permite salvar un documento.
    """

    def __init__(self, p_doc, p_path, p_window):
        """
            p_doc:    un EditorDocument a salvar.
            p_path:   una cadena que representa la
                      direccion donde salvar a p_doc.
            p_window: un gtk.Window o None.

            Retorna:  un EditorDocumentSaver.

            Crea un nuevo EditorDocumentSaver.
        """

        #assert (type(p_doc) == EditorDocument) FIXME: import loop
        assert (type(p_path) == str and os.path.isabs(p_path))
        assert (p_window == None or isinstance(p_window, gtk.Window))

        self.__doc = p_doc
        self.__path = p_path
        self.__window = p_window
        self.__used = False

    def save(self):
        """
            Retorna: True si se salvo el documento, False en caso contrario.

            Trata de salvar el documento.
        """

        assert (not self.__used)

        self.__used = True

        doc = self.__doc
        path = self.__path

        try:
            file_ = open(path, "w")

            doc.emit("saving", path)

            file_.write(doc.get_all_text())
            file_.close()

        except IOError, error:
            if os.access(path, os.F_OK):
                msg = "could not be saved.\nYou do not have the permissions " \
                      "necessary to save the file.\nPlease check that you "   \
                      "typed the location correctly and try again."

            elif not os.access(os.path.dirname(path), os.W_OK):
                msg = "could not be saved to this location.\nYou do not have "\
                      "the permissions necessary to create the file in that " \
                      "directory.\nPlease check that you typed the location " \
                      "correctly and try again."

            else:
                msg = str(error) + "\nPlease check that you typed the "       \
                                   "location correctly and try again."

            Message(gtk.STOCK_DIALOG_ERROR, "%s\n\n%s" %(path, msg),
                               "Saving Failed", self.__window).run()
            return False

        if path != doc.get_path():
            doc.set_name(os.path.basename(path))
            doc.set_path(path)

        doc.set_mtime(self.get_mtime())
        doc.set_modified(False)
        doc.set_ask(True)

        doc.emit("saved")

        return True

    def get_mtime(self):
        """
            Retorna: un entero.

            Devuelve el tiempo en segundos de la ultima
            modificacion en disco del documento.
        """

        try:
            return int(os.stat(self.__path).st_mtime)
        except:
            return 0
