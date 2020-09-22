import os
import gtk

from edebugger.editor_tab import EditorTab  # Solo para tipo.


class EditorTabLabel(gtk.HBox):
    """
        Etiqueta o pestanna de un EditorTab.
    """

    def __init__(self, p_tab):
        """
            p_tab:   un EditorTab.

            Retorna: un EditorTabLabel.

            Crea un nuevo EditorTabLabel.
        """

        assert (type(p_tab) == EditorTab)

        gtk.HBox.__init__(self, False, 4)

        self.__tab = p_tab

        # Caja de eventos.
        ebox = gtk.EventBox()
        ebox.set_visible_window(False)
        self.pack_start(ebox, True, True, 0)

        # Boton Cerrar.
        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        button.set_focus_on_click(False)
        button.set_name("editor-close-button")
        button.set_size_request(18, 18)
        button.set_tooltip_text("Close document")

        path = os.path.abspath(os.path.join(
             __file__, os.pardir, os.pardir, "images", "close_tab.png"))

        button.add(gtk.image_new_from_file(path))
        button.connect("clicked", self.on_close_button_clicked, p_tab)
        self.pack_start(button, False, False, 0)

        # gtk.HBox que contiene el Icono y el Nombre del documento.
        hbox = gtk.HBox(False, 4)
        ebox.add(hbox)

        # Icono.
        icon = gtk.Image()
        hbox.pack_start(icon, False, False, 0)

        # Etiqueta con el nombre del documento.
        label = gtk.Label()
        label.set_alignment(0.0, 0.5)
        label.set_padding(0, 0)
        hbox.pack_start(label, False, False, 0)

        # Etiqueta vacia.
        hbox.pack_start(gtk.Label(), True, True, 0)

        ebox.show_all()
        button.show_all()

        self.__ebox = ebox
        self.__button = button
        self.__icon = icon
        self.__label = label

        self.sync()

    def sync(self):
        """
            Sincroniza o actualiza el EditorTabLabel
            con la informacion del EditorTab asociado.
        """

        tab = self.__tab
        doc = tab.get_doc()

        name = doc.get_name()
        if doc.get_modified():
            name = "*" + name

        self.__label.set_text(name)

    def get_tab(self):
        """
            Retorna: un EditorTab.

            Devuelve el EditorTab asociado.
        """

        return self.__tab

    def on_close_button_clicked(self, p_button, p_tab):
        """
            p_button: un gtk.Button.
            p_tab:    un EditorTab.

            Se emite la sennal "tab_close_request" de
            EditorNotebook pasando a p_tab como parametro.
        """

        assert (p_button == self.__button)
        assert (p_tab == self.__tab)

        notebook = p_tab.get_parent()

        assert (notebook and notebook.__class__.__name__ == "EditorNotebook")

        notebook.emit("tab_close_request", p_tab)
