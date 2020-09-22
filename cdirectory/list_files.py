import os
import stat
import time
import gtk


class ListFiles(gtk.TreeView):
    """
        El listado de archivos del 'CurrentDirectory'.
    """
    def __init__(self, p_cdirectory):
        """
            p_cdirectory: un 'CurrentDirectory'.

            Retorna:      un nuevo 'ListFiles'.

            Crea un nuevo 'ListFiles'.
        """
        gtk.TreeView.__init__(self)

        self.set_model(gtk.ListStore(gtk.gdk.Pixbuf,
                                     str, str, str, str, str, str))

        self._create_column("All Files", (("pixbuf", 0), ("text", 1)))
        self._create_column("File Type", (("text", 2), ))
        self._create_column("Size", (("text", 3), ))
        self._create_column("Last Modified", (("text", 4), ))
    
        self.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

        self.connect("key-press-event", self.on_key_press_event)
        self.connect('row-activated', self.on_row_activated)
        self.connect("focus-in-event", self.on_focus_in_event)
        self.get_selection().connect("changed", self.on_selection_changed)

        self.__cdirectory = p_cdirectory

    def _create_column(self, p_text, p_cells):
        """
            p_text:  una cadena que representa el encabezado de la columna.
            p_cells: una tupla de tuplas donde cada subtupla representa una
                     celda en la columna, cada subtupla contiene como primer
                     elemento una cadena que representa el tipo de celda
                     ("pixbuf" o "text"), y como segundo elemento la posicion
                     en el modelo('gtk.ListStore') donde esta el dato a mostrar
                     por la celda.

            Metodo auxiliar para crear las columnas del 'ListFiles'.
        """
        dict_ = {"text": gtk.CellRendererText,
                 "pixbuf": gtk.CellRendererPixbuf}
        col = gtk.TreeViewColumn(p_text)
        col.set_resizable(True)
        for t in p_cells:
            cell = dict_[t[0]]()
            col.pack_start(cell, False)
            col.add_attribute(cell, t[0], t[1])
        self.append_column(col)

    def on_key_press_event(self, p_list, p_event):
        """
            p_list:  el 'ListFiles' que recibio la sennal.
            p_event: el evento que desencadeno la sennal.

            Retorna:      'True' si se presiono la tecla 'Enter'. Retornar
                          'True' detiene otros manejadores que se invocan
                           para el evento.

                          'False' si se presiono la teclas Space+Ctrl. Retornar
                          'False' permite que se hagan otros manejadores que se
                           invocan para el evento.

            Si se presiona 'Enter', 'Return' o 'Space' se llama el metodo
            'ListFiles.on_row_activated'.
        """
        ascii = p_event.keyval
        flags = p_event.state
        
        if ascii in (65293, 65421, 32):  # enter izq, enter der, space
            if ascii == 32 and int(gtk.gdk.CONTROL_MASK & flags):
                return False

            self.on_row_activated(None, None, None)
            return True

    def on_row_activated(self, p_list, p_path, p_col):
        """
            p_list: el 'ListFiles' que recibio la sennal.
            p_path: un camino de arbol que apunta a la fila activada.
            p_col:  la columna en la fila activada.

            Llama el metodo 'CurrentDirectory.try_to_open' para cada
            fila seleccionada.
        """
        model, paths = self.get_selection().get_selected_rows()

        if paths:
            files = [path for path in paths if not os.path.isdir(model[path][6])]

            if files:
                for file_ in files:
                    self.__cdirectory.try_to_open(model[file_][6])

            elif len(paths) == 1:
                self.__cdirectory.try_to_open(model[paths[0]][6])

    def on_focus_in_event(self, p_list, p_event):
        """
            p_list:  el 'ListFiles' que recibio la sennal.
            p_event: el evento que desencadeno la sennal.

            Se ejecuta cada vez que el 'ListFiles' recibe el foco. Llama el
            metodo 'CurrentDirectory.activate'.
        """
        self.__cdirectory.activate()

    def on_selection_changed(self, p_selec):
        """
            p_selec: el 'gtk.TreeSelection' asociado al 'ListFiles'.

            Se ejecuta cada vez que cambia la seleccion en el listado de
            archivos. Llama el metodo 'CurrentDirectory.update_appearance'.
        """
        self.__cdirectory.update_appearance()

    def show_path(self, p_path):
        """
            p_path: una cadena que representa un camino a un directorio.

            Muestra los archivos y carpetas del directorio 'p_path'.
        """
        self.get_model().clear()
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        for name in os.listdir(p_path):
            file_ = os.path.join(p_path, name)
            if os.path.isdir(file_):
                type_ = "Folder"
                size = ""
                img = "directory.png"
            else:
                if name.endswith("~"):
                    type_ = "Editor Autosave File"
                    img = "file.png"
                elif name.endswith(".m"):
                    type_ = "M-file"
                    img = "m_file.png"
                elif "." not in name:
                    type_ = "File"
                    img = "file.png"
                else:
                    type_ = name[name.rfind(".") + 1:].upper() + " File"
                    if type_.lower() in ("html file", "htm file"):
                        img = "html_file.png"
                    else:
                        img = "file.png"
                try:
                    bytes = os.stat(file_)[stat.ST_SIZE]
                    size = bytes / 1024
                    if bytes % 1024:
                        size += 1
                    size = str(size) + " KB"
                except OSError:
                    size = "Unknown"
            pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(root, "images",
                                                               img))
            try:
                struct = time.localtime(os.stat(file_)[stat.ST_MTIME])
                modified = time.strftime("%b %d, %Y %I:%M:%S ", struct)
                modified += {True: "AM"}.get(0 <= struct[3] <= 11, "PM")
            except OSError:
                modified = "Unknown"
            description = ""
            self.get_model().append([pixbuf, name, type_, size, modified,
                                description, file_])
