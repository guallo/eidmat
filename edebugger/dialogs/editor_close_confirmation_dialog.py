import gtk

from edebugger.editor_tab import EditorTab


class EditorCloseConfirmationDialog(gtk.Dialog):
    """
        Dialogo de confirmacion del cierre de los documentos.
    """

    def __init__(self, p_tabs, p_parent):
        """
            p_tabs:   una lista de objetos EditorTab.
            p_parent: None o un gtk.Window.

            Retorna:  un EditorCloseConfirmationDialog.

            Crea un nuevo EditorCloseConfirmationDialog.
        """

        assert (type(p_tabs) == list and p_tabs)
        assert (p_parent == None or isinstance(p_parent, gtk.Window))

        gtk.Dialog.__init__(self, "EIDMAT Editor", p_parent,
                                  gtk.DIALOG_MODAL | gtk.DIALOG_NO_SEPARATOR,
                                  ("Close _without Saving", gtk.RESPONSE_NO,
                                   gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                   gtk.STOCK_SAVE, gtk.RESPONSE_YES))

        self.__tabs = p_tabs
        self.__model = None

        hbox = gtk.HBox(False, 12)
        hbox.set_border_width(5)

        # Adicionamos el icono.
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_DIALOG)
        img.set_alignment(0.5, 0.0)
        hbox.pack_start(img, False, False, 0)

        vbox = gtk.VBox(False, 12)

        if len(p_tabs) == 1:
            self.build_single_doc_dialog(vbox)
        else:
            self.build_multiple_docs_dialog(vbox)

        hbox.pack_start(vbox, False, False, 0)
        hbox.show_all()

        child = self.get_child()
        child.pack_start(hbox, False, False, 0)
        child.get_children()[-1].set_layout(gtk.BUTTONBOX_CENTER)

        self.set_resizable(False)
        self.set_default_response(gtk.RESPONSE_YES)

    def build_single_doc_dialog(self, p_vbox):
        """
            p_vbox: un gtk.VBox.

            Adiciona dentro de p_vbox mensajes para cuando
            se pida confirmacion de un solo documento.
        """

        assert (isinstance(p_vbox, gtk.VBox))
        assert (type(self.__tabs[0]) == EditorTab)

        name = self.__tabs[0].get_doc().get_name()

        # Mensaje primario
        msg = 'Save changes to document "%s" before closing?' %name
        label = gtk.Label()
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_use_markup(True)
        label.set_markup('<span weight="bold" size="larger">%s</span>' %msg)
        p_vbox.pack_start(label, False, False, 0)

        # Mensaje secundario
        msg = "If you don't save, changes will be permanently lost."
        label = gtk.Label(msg)
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        p_vbox.pack_start(label, False, False, 0)

    def build_multiple_docs_dialog(self, p_vbox):
        """
            p_vbox: un gtk.VBox.

            Adiciona dentro de p_vbox mensajes y un listado para
            cuando se pida confirmacion de varios documentos.
        """

        assert (isinstance(p_vbox, gtk.VBox))

        # Mensaje primario
        msg = "There are %d documents with unsaved changes. " \
              "Save changes before closing?" %len(self.__tabs)
        label = gtk.Label()
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_use_markup(True)
        label.set_markup('<span weight="bold" size="larger">%s</span>' %msg)
        p_vbox.pack_start(label, False, False, 0)

        vbox2 = gtk.VBox(False, 8)
        p_vbox.pack_start(vbox2, False, False, 0)

        # Mensaje para seleccion
        msg = "Select the documents you want to save:"
        label = gtk.Label(msg)
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        vbox2.pack_start(label, False, False, 0)

        # TreeView
        scroll = gtk.ScrolledWindow(None, None)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.add(self.create_treeview())
        vbox2.pack_start(scroll, False, False, 0)

        # Mensaje secundario
        msg = "If you don't save, all your changes will be permanently lost."
        label = gtk.Label(msg)
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        vbox2.pack_start(label, False, False, 0)

    def create_treeview(self):
        """
            Retorna: un gtk.TreeView.

            Crea un listado con los documentos a confirmar.
        """

        # Modelo
        model = gtk.ListStore("gboolean", str, EditorTab)
        for tab in self.__tabs:
            assert (type(tab) == EditorTab)

            model.append((True, tab.get_doc().get_name(), tab))
        self.__model = model

        # TreeView
        treeview = gtk.TreeView(model)
        treeview.set_size_request(260, 120)
        treeview.set_headers_visible(False)

        # Columna Save?
        renderer = gtk.CellRendererToggle()
        renderer.connect("toggled", self.on_save_toogled, model)
        column = gtk.TreeViewColumn("Save?", renderer, active=0)
        treeview.append_column(column)

        # Columna Name
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Name", renderer, text=1)
        treeview.append_column(column)

        return treeview

    def on_save_toogled(self, p_renderer, p_path, p_model):
        """
            p_renderer: un gtk.CellRendererToggle.
            p_path:     una cadena que representa un camino.
            p_model:    un gtk.ListStore.

            Selecciona o deselecciona a p_renderer indicando
            si se desea salvar el documento correspondiente.
        """

        assert (type(p_renderer) == gtk.CellRendererToggle)
        assert (type(p_path) == str and p_path)
        assert (type(p_model) == gtk.ListStore)

        p_model[p_path][0] = not p_model[p_path][0]

    def run(self, p_block=False):
        """
            p_block: un boolean.

            Retorna: False o una lista de objetos EditorTab.

            Muestra el dialogo de confirmacion.
            Devuelve una lista de los objetos EditorTab que
            contienen a los documentos que se desean salvar
            o devuelve False si se cancela la accion.
        """

        assert (type(p_block) == bool)

        if p_block:
            gtk.gdk.threads_enter()

        response = gtk.Dialog.run(self)

        if response == gtk.RESPONSE_YES:
            if self.__model:
                result = [row[2] for row in self.__model if row[0]]
            else:
                result = self.__tabs

        elif response == gtk.RESPONSE_NO:
            result = []

        else:
            result = False

        self.destroy()

        if p_block:
            gtk.gdk.threads_leave()

        return result
