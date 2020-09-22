import gobject


class EditorTextWindowController(gobject.GObject):
    def __init__(self, p_event_mask):
        gobject.GObject.__init__(self)

        self.__event_mask = p_event_mask

    def get_event_mask(self):
        return self.__event_mask

    def handle_event(self, p_event, p_win, p_view):
        pass
