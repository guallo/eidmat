import os
import gtk

from wspace.list_vars_menu import ListVarsMenu
from cmds.rename_var import RenameVar


class ListVars(gtk.TreeView):
    """
        El listado de variables del 'Workspace'.
    """
    def __init__(self, p_conn, p_wspace):
        """
            p_conn:   un 'Connection' que es la conexion con Octave.
            p_wspace: un 'Workspace'.

            Retorna:  un nuevo 'ListVars'.

            Crea un nuevo 'ListVars'.
        """
        gtk.TreeView.__init__(self)

        self.set_model(gtk.ListStore(gtk.gdk.Pixbuf, str, str, str, str, str))
        self.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

        self._create_column("Name", (("pixbuf", 0), ("text", 1)), True)
        self._create_column("Size", (("text", 2), ))
        self._create_column("Bytes", (("text", 3), ))
        self._create_column("Class", (("text", 4), ))
        self._create_column("Attributes", (("text", 5), ))

        self.get_selection().connect("changed", self.on_selection_changed)
        self.connect("button-press-event", self.on_button_press_event)
        self.connect("event-after", self.on_event_after)
        self.connect("key-press-event", self.on_key_press_event)
        self.connect("focus-in-event", self.on_focus_in_event)

        self.__conn = p_conn
        self.__wspace = p_wspace
        self.__menu = ListVarsMenu(p_wspace)
        self.__show_menu = True

    def _create_column(self, p_text, p_cells, p_edit=False):
        """
            p_text:  una cadena que representa el encabezado de la columna.
            p_cells: una tupla de tuplas donde cada subtupla representa una
                     celda en la columna, cada subtupla contiene como primer
                     elemento una cadena que representa el tipo de celda
                     ("pixbuf" o "text"), y como segundo elemento la posicion
                     en el modelo('gtk.ListStore') donde esta el dato a mostrar
                     por la celda.
            p_edit:  'True' si se quiere que alguna celda de tipo texto
                     ('gtk.CellRendererText') pueda ser editada por el usuario,
                     'False' en otro caso.

            Metodo auxiliar para crear las columnas del 'ListVars'.
        """
        col = gtk.TreeViewColumn(p_text)
        col.set_resizable(True)
        for t in p_cells:
            if t[0] == "text":
                cell = gtk.CellRendererText()
                if p_edit:
                    cell.set_property("editable", True)
                    cell.connect("edited", self.on_columnname_edited)
            else:
                cell = gtk.CellRendererPixbuf()
            col.pack_start(cell, False)
            col.add_attribute(cell, t[0], t[1])
        self.append_column(col)

    def get_menu(self):
        """
            Retorna: un 'ListVarsMenu' asociado al listado de variables.

            Retorna el menu emergente que se muestra cuando el usuario da
            click derecho sobre el 'ListVars'.
        """
        return self.__menu

    def on_selection_changed(self, p_selec):
        """
            p_selec: el 'gtk.TreeSelection' asociado al 'ListVars'.

            Se ejecuta cada vez que cambia la seleccion en el listado de
            variables. Llama el metodo 'Workspace.update_appearance'.
        """
        self.__wspace.update_appearance()

    def on_button_press_event(self, p_list, p_event):
        """
            p_list:  el 'ListVars'.
            p_event: el evento que desencadeno la sennal.

            Retorna: 'True' si se presiono click derecho sobre el 'ListVars'.
                     'True' causa que se detengan otros manejadores que se
                     invoquen para el evento.

            Se ejecuta cada vez que se presiona un boton del mouse sobre el
            'ListVars'. Chequea si ocurrio el click derecho, en ese caso lanza
            el menu emergente('ListVarsMenu') asociado al 'ListVars'.
        """
        flags = p_event.state

        if p_event.button == 3:
            self.__show_menu = True
            pos = self.get_path_at_pos(int(p_event.x), int(p_event.y))

            if pos and not int(gtk.gdk.CONTROL_MASK & flags) and\
                       not int(gtk.gdk.SHIFT_MASK & flags) and\
                       self.get_selection().path_is_selected(pos[0]):

                self.__menu.popup(None, None, None, 3, p_event.time)
                self.__show_menu = False
                return True

    def on_event_after(self, p_list, p_event):
        """
            p_list:  el 'ListVars'.
            p_event: el evento que desencadeno la sennal.

            Se ejecuta despues de que ocurra cualquier otro manejador de
            evento para 'ListVars'. Chequea si el evento que ocurrio fue
            el de presionar un boton del mouse, en es caso, verifica si fue
            click derecho y en ese caso si el atributo 'ListVars.__show_menu'
            tiene 'True' entonces se lanza el menu emergente('ListVarsMenu')
            asociado al 'ListVars'.
        """
        if p_event.type == gtk.gdk.BUTTON_PRESS and\
           p_event.button == 3 and self.__show_menu:

            self.__menu.popup(None, None, None, 3, p_event.time)

    def on_key_press_event(self, p_list, p_event):
        """
            p_list:  el 'ListVars'.
            p_event: el evento que desencadeno la sennal.

            Retorna: 'True' si se presiono la tecla equivalente al click
                     derecho, o si se presiono 'Ctrl+N'. Retornar 'True'
                     detiene otros manejadores que se invocan para el evento.

            Este metodo es llamado cuando se presiona una tecla sobre 'p_list'.

            Ctrl+S:              llama el metodo 'Workspace.save(True)'.
            Ctrl+C, Ctrl+Insert: llama el metodo 'Workspace.copy'.
            Ctrl+D:              llama el metodo 'Workspace.duplicate'.
            Delete:              llama el metodo 'Workspace.delete'.
            F2:                  llama el metodo 'Workspace.rename'.
            Ctrl+N:              llama el metodo 'Workspace.new_var'.
            Shift+F10:           muestra el 'ListVarsMenu'.
        """
        ascii = p_event.keyval
        flags = p_event.state
        count = self.get_selection().count_selected_rows()

        if ascii == 115 or ascii == 83:  # s, S
            if int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and\
               not int(gtk.gdk.MOD1_MASK & flags):

                self.__wspace.save()

        elif ascii in (67, 65379, 99):  # c, C, insert
            if int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and\
               not int(gtk.gdk.MOD1_MASK & flags) and count:

                self.__wspace.copy()

        elif ascii == 100 or ascii == 68:  # d, D
            if int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and\
               not int(gtk.gdk.MOD1_MASK & flags) and count:

                self.__wspace.duplicate()

        elif ascii == 65535:  # Delete
            if not int(gtk.gdk.MOD1_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and count:

                self.__wspace.delete()

        elif ascii == 65471:  # F2
            if not int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and\
               not int(gtk.gdk.MOD1_MASK & flags) and count == 1:

                self.__wspace.rename()

        elif ascii == 110 or ascii == 78:  # n, N
            if int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags) and\
               not int(gtk.gdk.MOD1_MASK & flags):

                self.__wspace.new_var()
                return True

        elif ascii == 65383:  # Equivalente al click derecho.
            if not int(gtk.gdk.MOD1_MASK & flags) and\
               not int(gtk.gdk.CONTROL_MASK & flags) and\
               not int(gtk.gdk.SHIFT_MASK & flags):

                self.__menu.popup(None, None, None, 3, p_event.time)
                return True

        elif ascii == 65479:  # F10 Equivalente al click derecho.
            if not int(gtk.gdk.MOD1_MASK & flags) and\
               not int(gtk.gdk.CONTROL_MASK & flags) and\
               int(gtk.gdk.SHIFT_MASK & flags):

                self.__menu.popup(None, None, None, 3, p_event.time)
                return True

    def on_focus_in_event(self, p_list, p_event):
        """
            p_list:  el 'ListVars' que recibio la sennal.
            p_event: el evento que desencadeno la sennal.

            Se ejecuta cada vez que el 'ListVars' recibe el foco. Llama el
            metodo 'Workspace.activate'.
        """
        self.__wspace.activate()

    def show_vars(self, p_vars):
        """
            p_vars: una lista('list') de listas, donde cada sublista contiene
                    los datos de una variable determinada, los datos son:

                    - atributos
                    - nombre
                    - tamanno
                    - bytes
                    - clase

            Muestra los datos de las variables contenidas en 'p_vars'.
        """
        model, paths = self.get_selection().get_selected_rows()
        selected_vars = [model[path][1] for path in paths]

        model.clear()
        images = {"double": "class_double.png",
                  "char"  : "class_char.png",
                  "struct": "class_struct.png",
                  "cell"  : "class_cell.png",
                  "sym"   : "class_sym.png"}
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

        for pos, var in enumerate(p_vars):
            img = images.get(var[4], "class_double.png")
            pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(root, "images",
                                                               img))
            model.append([pixbuf, var[1], var[2], var[3], var[4], var[0]])
            if var[1] in selected_vars:
                self.get_selection().select_path((pos, ))

    def on_columnname_edited(self, p_cell, p_path, p_new_text):
        """
            p_cell:     el 'gtk.CellRendererText' encargado de mostrar el
                        nombre de la variable a renombrar.
            p_path:     una cadena que representa un camino de arbol. Indica
                        la fila de la variable a renombrar.
            p_new_text: una cadena que es el nuevo nombre a poner a la variable
                        correspondiente.

            Es llamado cuando el usuario le cambia el nombre a una variable,
            es decir cuando se edita el campo nombre de alguna variable.
            Renombra la variable correspondiente y le pone 'p_new_text' como
            nombre.
        """
        row = self.get_model()[p_path]
        self.__conn.append_command(RenameVar(p_new_text, row[1], row[5]))
