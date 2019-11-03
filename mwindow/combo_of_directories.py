import os
import gtk


class ComboOfDirectories(gtk.ComboBoxEntry):
    """
        Una caja combo que muestra la direccion del directorio actual y
        ademas almacena todos los directorios visitados por el usuario.
    """
    def __init__(self, p_mwindow):
        """
            p_mwindow: un 'MainWindow'.

            Retorna:   un nuevo 'ComboOfDirectories'.

            Crea un nuevo 'ComboOfDirectories' el cual muestra el camino del
            directorio actual del usuario. Ademas en el se van guardando
            todos los directorios que va visitando el usuario.
        """
        gtk.ComboBoxEntry.__init__(self, gtk.ListStore(str), 0)

        self.load(os.path.join(os.environ["HOME"], "cwdhistory.m"))

        self.connect("changed", self.changed)
        self.connect("key-press-event", self.key_press_event)
        self.connect("scroll-event", lambda p_combo, p_event: True)

        self.child.connect("activate", self.activate)
        self.child.connect("key-press-event", self.key_press_event)
        self.child.connect("focus-out-event",
                            lambda p_entry, p_event: self.set_active(0))

        self.__mwindow = p_mwindow

    def changed(self, p_combo):
        """
            p_combo: un 'ComboOfDirectories'.

            Este metodo es llamado cada vez que el usuario cambia el texto
            del combo de directorios. Si lo que ocurrio fue que el usuario
            selecciono del listado del combo un nuevo directorio, entonces
            se cambia el directorio actual segun el seleccionado.
        """
        if self.get_active() > 0:
            self.__mwindow.get_cdirectory().try_to_open(self.get_active_text())

            self.child.grab_focus()
            self.child.select_region(-1, -1)

    def activate(self, p_entry):
        """
            p_entry: el 'gtk.Entry' asociado al 'ComboOfDirectories'.

            Se ejecuta cuando el usuario presiona la tecla 'Enter' sobre
            'p_entry'. Cambia el directorio actual segun el seleccionado.
        """
        current_dir = self.__mwindow.get_cdirectory()
        path = os.path.abspath(self.get_active_text())

        if path != current_dir.get_path():
            current_dir.try_to_open(path)
        else:
            self.set_active(0)

    def key_press_event(self, p_entry, p_event):
        """
            p_entry: el 'gtk.Entry' asociado al 'ComboOfDirectories'.
            p_event: el evento que desencadeno la sennal.

            Retorna: 'True' si se presiono la tecla 'Arriba' o 'Abajo'.
                     Retornar 'True' detiene otros manejadores que se
                     invocan para el evento.

            Este metodo es llamado cuando se presiona una tecla sobre
            'p_entry'.

            Si se presiona la tecla 'Abajo' se muestra el listado de
            directorios del combo.
            Si se presiona la tecla 'Arriba' no se hace nada.
        """
        ascii = p_event.keyval
        flags = p_event.state

        if ascii == 65364 or ascii == 65433:
            if not int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and\
               not int(gtk.gdk.MOD1_MASK & flags):

                self.popup()
                return True

        elif ascii == 65362 or ascii == 65431:
            if not int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and\
               not int(gtk.gdk.MOD1_MASK & flags):

                return True

    def _open_file(self, p_mode):
        """
            p_mode:  el modo de abrir el fichero donde se guardan los
                     caminos de los directorios almacenados en el combo.
                     'p_mode' puede ser "r" si lo que se quiere es leer,
                     o "w" para escribir en el fichero.

            Retorna: un 'file' que es la instancia del fichero abierto.

            Metodo auxiliar que retorna una instancia del fichero utilizado
            para guardar los directorios del listado del 'ComboOfDirectories'.
            Antes que todo se chequea si existe el fichero, de no ser asi, se
            crea uno nuevo.
        """
        if p_mode == "r":
            f = open(self.__path, "a")
            f.close()
        return open(self.__path, p_mode)

    def load(self, p_path):
        """
            p_path: una cadena que representa el camino del fichero que guarda
                    los directorios del listado del 'ComboOfDirectories'.

            Carga el listado del 'ComboOfDirectories' con los directorios que
            se encuentran almacenados en el fichero indicado por 'p_path'.
        """
        self.__path = p_path

        self.get_model().clear()
        file_ = self._open_file("r")
        for line in file_:
            self.append_text(line.rstrip("\n"))
        file_.close()

    def _save(self):
        """
            Metodo auxiliar que salva todos los directorios almacenados en el
            'ComboOfDirectories' a fichero.
        """
        file_ = self._open_file("w")
        for row in self.get_model():
            file_.write(row[0] + "\n")
        file_.close()

    def show_path(self, p_path):
        """
            p_path: una cadena que representa el camino hacia un directorio.

            Muestra 'p_path' en la entrada de texto del 'ComboOfDirectories'.
            Este metodo es llamado cada vez que el usuario cambia de directorio
            para mostrar el camino de ese nuevo directorio.
        """
        model = self.get_model()
        for pos in xrange(len(model)):
            if model[pos][0] == p_path:
                self.remove_text(pos)
                break
        self.insert_text(0, p_path)
        self.set_active(0)
        self._save()
