import os
import re
import gtk
import pango

from util.terminal import Terminal
from util.constants import VAR, VALUE
from util.confirm import Confirm
from cmds.load_vars import LoadVars


class ImportWizard(gtk.Window):
    """
        Asistente para importar variables al 'Workspace'.
    """
    def __init__(self, p_path, p_conn, p_wspace, p_parent, p_lvars_model):
        """
            p_path:         una cadena que indica la direccion del fichero
                            que contiene las variables.
            p_conn:         un 'Connection' que es la conexion con Octave.
            p_wspace:       un 'Workspace'.
            p_parent:       un 'gtk.Window' que es la ventana principal.
            p_lvars_model:  el 'gtk.ListStore' asociado al 'ListVars'.

            Retorna:        un nuevo 'ImportWizard'.

            Crea un nuevo 'ImportWizard'.
        """
        gtk.Window.__init__(self)

        self.__path = p_path
        self.__conn = p_conn
        self.__workspace = p_wspace
        self.__lvars_model = p_lvars_model

        self.set_title("Import Wizard")
        self.set_border_width(5)
        self.set_size_request(692, 406)
        self.set_transient_for(p_parent)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

        vbox = gtk.VBox(False, 5)
        self.add(vbox)

        # Direccion del archivo a importar.
        label = gtk.Label()
        label.set_alignment(0.0, 0.5)
        text = "Variables in %s" % self.__path
        label.set_markup('<span foreground="#316AC4"><b>%s</b></span>' %text)
        vbox.pack_start(label, False)

        # Horizontal paned.
        hpaned = gtk.HPaned()
        hpaned.set_position(346)
        vbox.pack_start(hpaned)

        # Listado de variables.
        self.__model = gtk.ListStore("gboolean", gtk.gdk.Pixbuf, str, str, str, str, str)
        tree = gtk.TreeView(self.__model)
        self.__selec = tree.get_selection()
        self.__selec.connect("changed", self.on_selection_changed)

        # Columna Import.
        cell = gtk.CellRendererToggle()
        cell.set_property("activatable", True)
        cell.connect("toggled", self.on_import_toggled)
        col = gtk.TreeViewColumn("Import", cell, active=0)
        col.set_resizable(True)
        tree.append_column(col)

        # Columna Name.
        col = gtk.TreeViewColumn("Name")
        col.set_resizable(True)
        cell = gtk.CellRendererPixbuf()
        col.pack_start(cell, False)
        col.add_attribute(cell, "pixbuf", 1)
        cell = gtk.CellRendererText()
        col.pack_start(cell, False)
        col.add_attribute(cell, "text", 2)
        tree.append_column(col)

        # Columnas Size, Bytes, Class, Attributes.
        for pos, name in enumerate(["Size", "Bytes", "Class", "Attributes"]):
            cell = gtk.CellRendererText()
            col = gtk.TreeViewColumn(name, cell, text=pos+3)
            col.set_resizable(True)
            tree.append_column(col)

        scroll = gtk.ScrolledWindow()
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(tree)
        hpaned.add1(scroll)

        # Vista previa.
        self.__textview = gtk.TextView()
        self.__textview.set_editable(False)
        self.__textview.set_cursor_visible(False)
        self.__textview.modify_font(
                                pango.FontDescription("monospace Expanded 10"))
        self.__textview.set_left_margin(3)
        self.__textview.get_buffer().set_text("Loading...")
        scroll = gtk.ScrolledWindow()
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(self.__textview)
        hpaned.add2(scroll)

        # Caja de botones.
        buttonbox = gtk.HButtonBox()
        buttonbox.set_layout(gtk.BUTTONBOX_END)
        buttonbox.set_spacing(5)
        vbox.pack_start(buttonbox, False)

        # Boton aplicar.
        self.__apply_butt = gtk.Button(stock=gtk.STOCK_APPLY)
        self.__apply_butt.set_sensitive(False)
        self.__apply_butt.connect("clicked", self.on_apply_clicked)
        buttonbox.pack_start(self.__apply_butt)

        # Boton cancelar.
        self.__cancel_butt = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.__cancel_butt.connect("clicked", lambda p_butt: self.cancel())
        buttonbox.pack_start(self.__cancel_butt)

        # Terminal de la cual vamos a sacar los
        # datos para mostrarselos al usuario.
        self.__term = Terminal()
        self.__term.feed_child(self._get_cmds(), self.extract_names)

        self.__wait = False
        self.__update = False

        self.connect("delete-event", lambda p_wiz, p_event: self.cancel())
        self.show_all()

    def on_import_toggled(self, p_cell, p_path):
        """
            p_cell: el 'gtk.CellRendererToggle' que recibio la sennal.
            p_path: una cadena que representa un camino de arbol. Indica la
                    fila de 'p_cell'.

            Se ejecuta cuando el usuario da click en los checkboxes de la
            columna 'Import'. Cambia el estado del checkbox correspondiente.
        """
        self.__model[p_path][0] = not self.__model[p_path][0]

    def _get_cmds(self):
        """
            Retorna: una cadena.

            Metodo auxiliar que retorna codigo Octave que permite determinar
            los nombres de las variables que estan en el archivo del cual se
            quiere importar.
        """
        path = os.path.join(os.path.dirname(__file__), "disp_names.m")

        file_ = open(path, "r")
        code = file_.read().strip()
        file_.close()

        replacer = lambda match: {"var": VAR,
                                  "index": VAR + "1",
                                  "value": VALUE,
                                  "path": self.__path,
                                  "\n": ""
                                 }[match.group()]

        pattern = re.compile("(var|index|value|path|\n)")
        code = re.sub(pattern, replacer, code)

        return code + "\n"

    def extract_names(self, p_text):
        """
            p_text: una cadena devuelta por 'Octave' la cual contiene los
                    nombres de las variables contenidas en el archivo a
                    importar.

            Extrae de 'p_text' los nombres de las variables.
        """
        lines = p_text.split("\n")
        names = []

        pos = -2
        while lines[pos] != "***":
            names.insert(0, lines[pos])
            pos -= 1

        if names:
            self.__term.feed_child("whos;\n", self.show_vars, [names])
        else:
            self.__textview.get_buffer().set_text("Could not import any variable.")

    def _get_vars(self, p_text):
        """
            p_text:  una cadena que es la salida del comando 'whos;'
                     enviado anteriormente a 'Octave'.

            Retorna: una lista('list') de listas, donde cada sublista contiene
                     los datos de una variable determinada, los datos son:

                     - atributos
                     - nombre
                     - tamanno
                     - bytes
                     - clase

            Metodo auxiliar que retorna los datos de las variables extraidas
            de 'p_text'.
        """
        lines = p_text.splitlines()
        length = len(lines)
        pos = 0

        find_equal = True
        pattern = re.compile("Total is \d+ elements? using \d+ bytes?", re.IGNORECASE)

        vars_ = []
        while pos < length:
            line = lines[pos]

            if find_equal:
                if "=" in line:
                    find_equal = False

            else:  # find_vars
                if re.search(pattern, line):
                    break

                var = line.split()
                if var:
                    if len(var) == 4:
                        var.insert(0, "")
                    vars_.append(var)

            pos += 1
        return vars_

    def show_vars(self, p_text, p_names):
        """
            p_text:  una cadena que es la salida del comando 'whos;'
                     enviado anteriormente a 'Octave'.
            p_names: una lista('list') que contiene los nombres de las
                     variables contenidas en el archivo a importar.

            Muestra en un listado las variables contenidas en el archivo a
            importar. De cada variable se expone su nombre, tamanno, bytes,
            clase y atributos.
        """
        vars_ = self._get_vars(p_text)
        model = self.__model
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        images = {"double": "class_double.png",
                  "char"  : "class_char.png",
                  "struct": "class_struct.png",
                  "cell"  : "class_cell.png",
                  "sym"   : "class_sym.png"}

        for var in vars_:
            if var[1] in p_names:
                img = images.get(var[4], "class_double.png")
                pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(root,
                                                                "images", img))
                model.append([True, pixbuf, var[1], var[2], var[3], var[4], var[0]])

        self.__apply_butt.set_sensitive(True)
        self.__textview.get_buffer().set_text("No variable selected for preview.")

    def on_selection_changed(self, p_selec):
        """
            p_selec: el 'gtk.TreeSelection' asociado al listado de variables
                     del 'ImportWizard'.

            Se ejecuta cuando cambia la seleccion en el listado de variables
            del 'ImportWizard'. Si hay alguna fila seleccionada entonces se
            obtiene el valor de la variable correspondiente y se llama el
            metodo 'ImportWizard.show_preview' pasandole como parametro dicho
            valor.
        """
        if self.__wait:
            self.__update = True
            return

        model, iter_ = p_selec.get_selected()

        if iter_:
            size = 1
            for dim in model.get_value(iter_, 3).split("x"):
                size *= int(dim)

            if size <= 2000:
                self.__term.feed_child("disp(%s);\n" %model.get_value(iter_, 2)
                                       , self.show_preview)
                self.__wait = True
            else:
                self.__textview.get_buffer().set_text("Preview too large to be displayed properly.")

        else:
            self.__textview.get_buffer().set_text("No variable selected for preview.")

    def show_preview(self, p_text):
        """
            p_text: una cadena que es el valor de la variable seleccionada
                    en el 'ImportWizard'.

            Muestra 'p_text' en la vista de texto del 'ImportWizard'.
        """
        self.__textview.get_buffer().set_text(p_text[p_text.index("\n") + 1:
                                                     p_text.rindex("\n")])
        self.__wait = False
        if self.__update:
            self.on_selection_changed(self.__selec)
            self.__update = False

    def cancel(self):
        """
            Cancela la importacion y cierra el asistente.
        """
        self.__term.feed_child("exit\n")
        self.destroy()
        self.__workspace.import_wiz_closed()

    def on_apply_clicked(self, p_butt):
        """
            p_butt: el 'gtk.Button' que recibio la sennal.

            Se ejecuta cuando el usuario da click en el boton 'Aplicar'.
            Chequea si alguna de las variables a importar ya existe en el
            'Workspace', en dicho caso se le informa al usuario. Si el usuario
            confirma todo, entonces se importan hacia el 'Workspace' las
            variables marcadas en los checkboxes.
        """
        new_names = [row[2] for row in self.__model if row[0]]

        if not new_names:
            self.cancel()
            return

        old_names = [row[1] for row in self.__lvars_model]
        equals = []
        for new in new_names:
            if new in old_names:
                equals.append(new)
                if len(equals) == 3:
                    break

        if equals:
            if len(equals) == 1:
                msg = "A variable named\n%s\n" \
                      "already exist in the EIDMAT Workspace." %equals[0]
            elif len(equals) == 2:
                msg = "Variables named\n%s and %s\n" \
                      "already exist in the EIDMAT Workspace." %tuple(equals)
            else:
                msg = "Variables with some of these names already exist\n" \
                      "in the EIDMAT Workspace."
            msg += "\n\nAre you sure that you want to overwrite them?"

            if not Confirm(gtk.STOCK_DIALOG_QUESTION, msg, "Import Wizard",
                                                            self).run():
                return

        if len(new_names) == len(self.__model):
            self.__conn.append_command(LoadVars([], self.__path))
        else:
            self.__conn.append_command(LoadVars(new_names, self.__path))

        self.cancel()
