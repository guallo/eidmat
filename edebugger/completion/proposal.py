import gobject
import gtksourceview2


class Proposal(gobject.GObject, gtksourceview2.CompletionProposal):
    __gtype_name__ = "Proposal"

    def __init__(self, p_label, p_info):
        gobject.GObject.__init__(self)

        self.__label = p_label
        self.__info = p_info

    def do_get_label(self):
        return self.__label

    def do_get_text(self):
        return self.__label

    def do_get_info(self):
        return self.__info
