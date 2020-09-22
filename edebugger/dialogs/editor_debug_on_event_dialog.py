import os
import gtk


class EditorDebugOnEventDialog(gtk.Dialog):
    def __init__(self, p_parent):
        gtk.Dialog.__init__(self, "Debug on Event", p_parent,
                                  gtk.DIALOG_MODAL | gtk.DIALOG_NO_SEPARATOR,
                                  (gtk.STOCK_OK, gtk.RESPONSE_OK,
                                   gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

        self.__message = None
        self.__replacer = None

        self.__body = gtk.VBox(False, 12)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)

        self.__checks = gtk.VBox(False, 5)
        self.__checks.set_border_width(5)

        check1 = gtk.CheckButton("Debug on _error", True)
        check2 = gtk.CheckButton("Debug on _warning", True)
        check3 = gtk.CheckButton("Debug on _interrupt", True)

        self.__checks.pack_start(check1, False, False, 0)
        self.__checks.pack_start(check2, False, False, 0)
        self.__checks.pack_start(check3, False, False, 0)

        frame.add(self.__checks)
        self.__body.pack_end(frame, False, False, 0)

        self.__body.show_all()

        child = self.get_child()
        child.set_spacing(5)
        child.pack_start(self.__body, False, False, 0)
        child.get_children()[-1].set_layout(gtk.BUTTONBOX_CENTER)

        self.set_border_width(10)
        self.set_size_request(300, -1)
        self.set_resizable(False)
        self.set_default_response(gtk.RESPONSE_OK)

    def set_active_buttons(self, *p_buttons):
        for (pos, check) in enumerate(self.__checks):
            check.set_active(p_buttons[pos])

    def get_active_buttons(self):
        return [check.get_active() for check in self.__checks]

    def set_spinner_visible(self, p_visible):
        if bool(self.__message) == p_visible:
            return

        if p_visible:
            message = gtk.EventBox()
            message.set_size_request(-1, 22)
            message.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#FFFFFF"))  #FCFCDC

            hbox = gtk.HBox(False, 5)

            label = gtk.Label("Waiting for Octave...")

            spinner = gtk.Image()
            root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
            file_ = os.path.join(root, "images", "spinner.gif")
            spinner.set_from_file(file_)

            hbox.pack_end(spinner, False, False, 0)
            hbox.pack_end(label, False, False, 0)

            message.add(hbox)

            self.__body.pack_start(message, False, False, 0)
            message.show_all()
            self.__message = message
        else:
            self.__message.get_parent().remove(self.__message)
            self.__message = None

    def set_replacer_visible(self, p_visible):
        if bool(self.__replacer) == p_visible:
            return

        if p_visible:
            replacer = gtk.EventBox()
            replacer.set_size_request(-1, 22)
            replacer.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#F5F4A2"))

            hbox = gtk.HBox(False, 5)

            img = gtk.Image()
            img.set_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_MENU)

            label = gtk.Label("Replace contents?")

            button_yes = gtk.Button(label="_Yes")
            button_no = gtk.Button(label="_No")

            hbox.pack_start(img, False, False, 0)
            hbox.pack_start(label, False, False, 0)
            hbox.pack_end(button_no, False, False, 0)
            hbox.pack_end(button_yes, False, False, 0)

            replacer.add(hbox)

            self.__body.pack_start(replacer, False, False, 0)
            replacer.show_all()
            self.__replacer = replacer
        else:
            self.__replacer.get_parent().remove(self.__replacer)
            self.__replacer = None

    def connect_replacer_callbacks(self, p_callback_yes=None, p_callback_no=None):
        dct = {}
        replacer = self.__replacer

        if replacer:
            button_yes, button_no = replacer.get_child().get_children()[-2:]

            if p_callback_yes:
                dct[button_yes] = button_yes.connect("clicked", p_callback_yes)
            if p_callback_no:
                dct[button_no] = button_no.connect("clicked", p_callback_no)

        return dct

    def run(self):
        resp = gtk.Dialog.run(self)
        result = self.get_active_buttons() if resp == gtk.RESPONSE_OK else None
        self.destroy()
        return result
