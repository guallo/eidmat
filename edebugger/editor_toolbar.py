import os
import gtk


class EditorToolbar(gtk.Toolbar):
    """
        Barra de herramientas del EditorDebugger.
    """

    def __init__(self, p_editor):
        """
            p_editor: un EditorDebugger.

            Retorna:  un EditorToolbar.

            Crea un nuevo EditorToolbar.
        """

        #assert (type(p_editor) == EditorDebugger) FIXME: import loop

        gtk.Toolbar.__init__(self)

        self.__editor = p_editor

        self.set_style(gtk.TOOLBAR_ICONS)

        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
		
		# Boton para mostrar una nueva pestanna.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "file.png"))
        file_ = gtk.ToolButton(img, "New")
        file_.set_tooltip_text("New M-File")
        file_.connect("clicked", self.on_file_clicked)
        self.insert(file_, -1)
        self.__file = file_

        # Boton abrir.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "open.png"))
        open_ = gtk.ToolButton(img, "Open")
        open_.set_tooltip_text("Open file")
        open_.connect("clicked", self.on_open_clicked)
        self.insert(open_, -1)
        self.__open = open_

        # Boton guardar.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "save.png"))
        save = gtk.ToolButton(img, "Save")
        save.set_tooltip_text("Save")
        save.connect("clicked", self.on_save_clicked)
        self.insert(save, -1)
        self.__save = save

        # Separador.
        self.insert(gtk.SeparatorToolItem(), -1)

        # Boton cortar.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "cut.png"))
        cut = gtk.ToolButton(img, "Cut")
        cut.set_tooltip_text("Cut")
        cut.connect("clicked", self.on_cut_clicked)
        self.insert(cut, -1)
        self.__cut = cut

        # Boton copiar.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "copy.png"))
        copy = gtk.ToolButton(img, "Copy")
        copy.set_tooltip_text("Copy")
        copy.connect("clicked", self.on_copy_clicked)
        self.insert(copy, -1)
        self.__copy = copy

        # Boton pegar.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "paste.png"))
        paste = gtk.ToolButton(img, "Paste")
        paste.set_tooltip_text("Paste")
        paste.connect("clicked", self.on_paste_clicked)
        self.insert(paste, -1)
        self.__paste = paste

        # Boton undo.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "undo.png"))
        undo = gtk.ToolButton(img, "Undo")
        undo.set_tooltip_text("Undo")
        undo.connect("clicked", self.on_undo_clicked)
        self.insert(undo, -1)
        self.__undo = undo

        # Boton redo.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "redo.png"))
        redo = gtk.ToolButton(img, "Redo")
        redo.set_tooltip_text("Redo")
        redo.connect("clicked", self.on_redo_clicked)
        self.insert(redo, -1)
        self.__redo = redo

        # Separador.
        self.insert(gtk.SeparatorToolItem(), -1)

        # Boton Set/Clear breakpoint.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "set_clear_breakpoint.png"))
        set_clear = gtk.ToolButton(img, "Set/Clear breakpoint")
        set_clear.set_tooltip_text("Set/clear breakpoint")
        self.insert(set_clear, -1)
        self.__set_clear = set_clear

        # Boton Clear Breakpoints in Opened Files.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "clear_opened_files.png"))
        clear_opened = gtk.ToolButton(img, "Clear Breakpoints in Opened Files")
        clear_opened.set_tooltip_text("Clear breakpoints in opened files")
        self.insert(clear_opened, -1)
        self.__clear_opened = clear_opened

        # Separador.
        self.insert(gtk.SeparatorToolItem(), -1)

        # Boton Step.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "step.png"))
        step = gtk.ToolButton(img, "Step")
        step.set_tooltip_text("Step")
        self.insert(step, -1)
        self.__step = step

        # Boton Step In.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "step_in.png"))
        step_in = gtk.ToolButton(img, "Step In")
        step_in.set_tooltip_text("Step in")
        self.insert(step_in, -1)
        self.__step_in = step_in

        # Boton Step Out.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "step_out.png"))
        step_out = gtk.ToolButton(img, "Step Out")
        step_out.set_tooltip_text("Step out")
        self.insert(step_out, -1)
        self.__step_out = step_out

        # Boton Continue.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "continue.png"))
        continue_ = gtk.ToolButton(img, "Continue")
        continue_.set_tooltip_text("Continue")
        self.insert(continue_, -1)
        self.__continue_ = continue_

        # Boton Run.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "run.png"))
        run = gtk.ToolButton(img, "Run")
        run.set_tooltip_text("Run")
        self.insert(run, -1)
        self.__run = run

        # Boton Exit Debug Mode.
        img = gtk.Image()
        img.set_from_file(os.path.join(root, "images", "exit_debug_mode.png"))
        exit_debug = gtk.ToolButton(img, "Exit Debug Mode")
        exit_debug.set_tooltip_text("Exit debug mode")
        self.insert(exit_debug, -1)
        self.__exit_debug = exit_debug

    def on_file_clicked(self, p_butt):
        """
            p_butt: un gtk.ToolButton.

            Llama el metodo EditorDebugger.new_document.
        """

        assert (p_butt == self.__file)

        self.__editor.new_document()

    def on_open_clicked(self, p_butt):
        """
            p_butt: un gtk.ToolButton.

            Llama el metodo EditorDebugger.open_document.
        """

        assert (p_butt == self.__open)

        self.__editor.open_document()

    def on_save_clicked(self, p_butt):
        """
            p_butt: un gtk.ToolButton.

            Llama el metodo EditorDebugger.save.
        """

        assert (p_butt == self.__save)

        self.__editor.save()

    def on_undo_clicked(self, p_butt):
        """
            p_butt: un gtk.ToolButton.

            Llama el metodo EditorDebbuger.undo.
        """

        assert (p_butt == self.__undo)

        self.__editor.undo()

    def on_redo_clicked(self, p_butt):
        """
            p_butt: un gtk.ToolButton.

            Llama el metodo EditorDebbuger.redo.
        """

        assert (p_butt == self.__redo)

        self.__editor.redo()

    def on_cut_clicked(self, p_butt):
        """
            p_butt: un gtk.ToolButton.

            Llama el metodo EditorDebbuger.cut.
        """

        assert (p_butt == self.__cut)

        self.__editor.cut()

    def on_copy_clicked(self, p_butt):
        """
            p_butt: un gtk.ToolButton.

            Llama el metodo EditorDebbuger.copy.
        """

        assert (p_butt == self.__copy)

        self.__editor.copy()

    def on_paste_clicked(self, p_butt):
        """
            p_butt: un gtk.ToolButton.

            Llama el metodo EditorDebbuger.paste.
        """

        assert (p_butt == self.__paste)

        self.__editor.paste()

    def get_save(self):
        """
            Retorna: un gtk.ToolButton.

            Devuelve el boton Save.
        """

        return self.__save

    def get_undo(self):
        """
            Retorna: un gtk.ToolButton.

            Devuelve el boton Undo.
        """

        return self.__undo

    def get_redo(self):
        """
            Retorna: un gtk.ToolButton.

            Devuelve el boton Redo.
        """

        return self.__redo

    def get_cut(self):
        """
            Retorna: un gtk.ToolButton.

            Devuelve el boton Cut.
        """

        return self.__cut

    def get_copy(self):
        """
            Retorna: un gtk.ToolButton.

            Devuelve el boton Copy.
        """

        return self.__copy

    def get_paste(self):
        """
            Retorna: un gtk.ToolButton.

            Devuelve el boton Paste.
        """

        return self.__paste

    def get_set_clear(self):
        return self.__set_clear

    def get_clear_opened(self):
        return self.__clear_opened

    def get_step(self):
        return self.__step

    def get_step_in(self):
        return self.__step_in

    def get_step_out(self):
        return self.__step_out

    def get_continue_(self):
        return self.__continue_

    def get_run(self):
        return self.__run

    def get_exit_debug(self):
        return self.__exit_debug
