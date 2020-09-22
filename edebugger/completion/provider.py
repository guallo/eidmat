import gtk
import gobject
import gtksourceview2

from edebugger.completion.proposal import Proposal


class Provider(gobject.GObject, gtksourceview2.CompletionProvider):
    __gtype_name__ = "Provider"

    def __init__(self, p_name, p_symbols):
        gobject.GObject.__init__(self)

        self.__name = p_name
        self.__symbols = p_symbols
        self.__info_widget = None

    def __build_info_widget(self):
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        label = gtk.Label()
        label.set_selectable(False)
        label.set_use_underline(False)
        label.set_use_markup(False)
        label.set_alignment(0.0, 0.0)
        scroll.add_with_viewport(label)
        return scroll

    def __get_word_at_iter(self, p_iter):
        if not p_iter.ends_word() or p_iter.get_char() == '_':
            return (None, None)

        start = p_iter.copy()

        while True:
            if start.starts_line():
                break

            start.backward_char()
            ch = start.get_char()

            if not (ch.isalnum() or ch == '_' or ch == ':'):
                start.forward_char()
                break

        if start.equal(p_iter):
            return (None, None)

        while (not start.equal(p_iter)) and start.get_char().isdigit():
            start.forward_char()

        if start.equal(p_iter):
            return (None, None)

        # Analizar este "get_text" para cuando hay algun "anchor" en el buffer.
        return (start, start.get_text(p_iter))

    def __get_proposals_for_word(self, p_word):
        proposals = []
        for symbol in self.__symbols:
            lexema = symbol.get_lexema()
            if lexema.startswith(p_word):
                proposal = Proposal(lexema, symbol.get_info())
                proposals.append(proposal)
        return proposals

    def do_get_name(self):
        return self.__name

    def do_populate(self, p_context):
        start, word = self.__get_word_at_iter(p_context.get_iter())
        proposals = self.__get_proposals_for_word(word) if word else []
        p_context.add_proposals(self, proposals, True)

    def do_get_activation(self):
        return (gtksourceview2.COMPLETION_ACTIVATION_USER_REQUESTED |
                gtksourceview2.COMPLETION_ACTIVATION_INTERACTIVE)

    def do_match(self, p_context):
        # if (no estoy en un contexto en el que yo pudiera proveer):  # un comentario, etc
        #     return False
        return True

    def do_get_info_widget(self, p_proposal):
        self.__info_widget = self.__build_info_widget()
        return self.__info_widget

    def do_update_info(self, p_proposal, p_info_win):
        text = p_proposal.get_info()
        scroll = self.__info_widget
        label = scroll.get_child().get_child()
        label.set_label(text)
        scroll.set_size_request(310, 192)
        scroll.show_all()
