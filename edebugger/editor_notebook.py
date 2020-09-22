import gtk
import gobject

from edebugger.editor_tab import EditorTab  # Solo para tipo.
from edebugger.editor_tab_label import EditorTabLabel


class MetaClassEditorNotebook(type(gtk.Notebook)):
    """
        Metaclase para la clase EditorNotebook.
    """

    def __init__(cls, name, bases, dct):
        """
            Le da estilo al boton cerrar de los tabs.
        """

        type(gtk.Notebook).__init__(cls, name, bases, dct)

        gtk.rc_parse_string(
        """
        style "editor-close-button-style"
        {
          GtkWidget::focus-padding = 0
          GtkWidget::focus-line-width = 0
          xthickness = 0
          ythickness = 0
        }
        widget "*.editor-close-button" style "editor-close-button-style"
        """
        )


class EditorNotebook(gtk.Notebook):
    """
        Notebook del EditorDebugger.
    """

    __metaclass__ = MetaClassEditorNotebook
    __gsignals__ = {"tab_close_request": (gobject.SIGNAL_RUN_LAST,
                                          gobject.TYPE_NONE,
                                          (EditorTab, ))
                    }

    def __init__(self):
        """
            Retorna: un EditorNotebook.

            Crea un nuevo EditorNotebook.
        """

        gtk.Notebook.__init__(self)

        self.__focused_tabs = []

        self.set_tab_pos(gtk.POS_TOP)
        self.set_scrollable(True)

        self.connect_after("switch-page", self.on_switch_page)

    def on_switch_page(self, p_notebook, p_gpointer, p_num):
        """
            p_notebook: un EditorNotebook.
            p_gpointer: un GPointer.
            p_num:      un entero que representa el indice
                        de la nueva pagina actual.

            Pone al EditorTab con indice p_num al final de
            la lista __focused_tabs.
        """

        assert (p_notebook == self)
        assert (type(p_num) in (long, int))

        tab = p_notebook.get_nth_page(p_num)

        assert (tab)

        focused_tabs = self.__focused_tabs

        if tab in focused_tabs:
            focused_tabs.remove(tab)

        focused_tabs.append(tab)
        # give focus to the view ?

    def on_tab_tab_label_sync_request(self, p_tab):
        """
            p_tab: un EditorTab.

            Se ejecuta cuando se solicita sincronizar
            al EditorTabLabel correspondiente a p_tab.
            Llama el metodo EditorTabLabel.sync().
        """

        assert (type(p_tab) == EditorTab and p_tab.get_parent() == self)

        tab_label = self.get_tab_label(p_tab)

        assert (type(tab_label) == EditorTabLabel and
                tab_label.get_tab() == p_tab)

        tab_label.sync()

    def add_tab(self, p_tab, p_pos, p_jump_to):
        """
            p_tab:     un EditorTab.
            p_pos:     un entero.
            p_jump_to: un boolean.

            Inserta a p_tab en una pagina en la posicion p_pos.
            Si p_jump_to es True se pone a p_tab como la pagina
            activa.
        """

        assert (type(p_tab) == EditorTab and not p_tab.get_parent())
        assert (type(p_pos) in (int, long))
        assert (type(p_jump_to) == bool)

        self.insert_page(p_tab, EditorTabLabel(p_tab), p_pos)

        if p_jump_to:
            self.set_current_page(p_pos)
            p_tab.get_view().grab_focus()

        p_tab.set_data("jump_to", p_jump_to)
        p_tab.connect("tab_label_sync_request",
                      self.on_tab_tab_label_sync_request)

    def remove_tab(self, p_tab):
        """
            p_tab: un EditorTab.

            Elimina la pagina que contiene a p_tab.
        """

        assert (type(p_tab) == EditorTab and p_tab.get_parent() == self)

        focused_tabs = self.__focused_tabs

        if p_tab in focused_tabs:
            focused_tabs.remove(p_tab)

        num = self.page_num(p_tab)

        if num == self.get_current_page():
            self.__smart_tab_switching_on_closure(p_tab)

        self.remove_page(num)

    def remove_all_tabs(self):
        """
            Llama para cada uno de los tabs el
            metodo EditorNotebook.remove_tab(tab).
        """

        self.foreach(self.remove_tab)

    def __smart_tab_switching_on_closure(self, p_tab):
        """
            p_tab: un EditorTab.

            Se ejecuta en caso de que se vaya a cerrar a
            p_tab y este sea el que esta activo.
            Se decide cual sera la nueva pagina activa.
        """

        focused_tabs = self.__focused_tabs

        assert (type(p_tab) == EditorTab and p_tab.get_parent() == self and
                p_tab not in focused_tabs)

        jump_to = p_tab.get_data("jump_to")

        assert (type(jump_to) == bool)

        if jump_to and focused_tabs:
            num = self.page_num(focused_tabs[-1])
            self.set_current_page(num)
        else:
            self.next_page()

    def find_doc_with_path(self, p_path):
        """
            p_path:  una cadena que representa la direccion
                     de un EditorDocument.

            Retorna: un entero.

            Devuelve el indice de la pagina que contiene
            al documento que su direccion es igual a p_path.
            Si no hay ningun documento con esa direccion se
            devuelve -1.
        """

        assert (type(p_path) == str)

        for num, tab in enumerate(self.get_children()):
            assert (type(tab) == EditorTab)

            if tab.get_doc().get_path() == p_path:
                return num
        return -1

    def get_tabs_of_unsaved_docs(self):
        """
            Retorna: una lista de objetos EditorTab.

            Devuelve una lista con los tabs cuyos
            documentos no estan salvados.
        """

        unsaved = []

        for tab in self.get_children():
            assert (type(tab) == EditorTab)

            if not tab.can_close():
                unsaved.append(tab)

        return unsaved
