import gtk


class EditorLoadPathDialog(gtk.MessageDialog):
    def __init__(self, p_parent, p_file, p_secondary_text):
        primary_text = "File %s is not found in the current " \
                       "directory or on the Octave path." %p_file

        gtk.MessageDialog.__init__(self,
                                   parent=p_parent,
                                   flags=gtk.DIALOG_MODAL,
                                   message_format=primary_text)

        self.format_secondary_text("%s, you can either change the Octave " \
                                   "current directory or add its directory " \
                                   "to the Octave path." %p_secondary_text)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
        img.set_alignment(0.5, 0.0)
        img.show()
        self.set_image(img)

        self.add_buttons("Change _Directory", 0,
                         "_Add to Path", 1,
                         "_Cancel", 2)
        self.child.get_children()[-1].set_layout(gtk.BUTTONBOX_CENTER)

        self.set_default_response(0)

    def run(self):
        response = gtk.MessageDialog.run(self)

        self.destroy()

        return response if response in (0, 1, 2) else 2
