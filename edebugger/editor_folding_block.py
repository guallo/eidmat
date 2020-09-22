import gtk


class EditorFoldingBlockType:
    (NORMAL,
    DO,
    FOR,
    FUNCTION,
    IF,
    ELSEIF,
    ELSE,
    SWITCH,
    CASE,
    OTHERWISE,
    TRY,
    CATCH,
    UNWIND_PROTECT,
    UNWIND_PROTECT_CLEANUP,
    WHILE,
    ) = xrange(15)


class EditorFoldingBlock:
    def __init__(self, p_doc=None, p_offset1=None, p_offset2=None,
                    p_offset3=None, p_blocks=None, p_type=None,
                    p_handler_ids=None):
        # Args
        self.__doc = p_doc
        self.__offset1 = p_offset1  # deleted after installed
        self.__offset2 = p_offset2  # deleted after installed
        self.__offset3 = p_offset3  # deleted after installed
        self.__blocks = p_blocks if p_blocks != None else []
        self.__type = p_type
        self.__mark1 = None
        self.__mark2 = None
        self.__mark3 = None
        self.__tag = gtk.TextTag()
        self.__tag.set_property("invisible-set", True)
        self.__anchor = None
        self.__handler_ids = p_handler_ids if p_handler_ids != None else []
        self.__pendings = []  # deleted after installed

        self.__installed = False

        def function():
            assert (not self.__installed)
            return (self.__offset1, self.__offset2, self.__offset3)

        self.get_initial_offsets = function  # deleted after installed
        del function

    def install(self):
        if self.__installed:
            return
        self.__installed = True

        doc = self.__doc
        offset1 = self.__offset1
        offset2 = self.__offset2
        offset3 = self.__offset3
        tag = self.__tag

        assert (0 <= offset1 <= offset2 <= offset3)

        iter1 = doc.get_iter_at_offset(offset1)
        iter2 = doc.get_iter_at_offset(offset2)
        iter3 = doc.get_iter_at_offset(offset3)

        self.__mark1 = doc.create_mark(None, iter1, False)
        self.__mark2 = doc.create_mark(None, iter2, False)
        self.__mark3 = doc.create_mark(None, iter3, False)

        doc.get_tag_table().add(tag)
        doc.apply_tag(tag, iter2, iter3)

        for function, args in self.__pendings:
            function(*args)

        del self.__offset1
        del self.__offset2
        del self.__offset3
        del self.get_initial_offsets
        del self.__pendings

    def set_doc(self, p_doc):
        self.__doc = p_doc

    def set_offset1(self, p_offset1):
        self.__offset1 = p_offset1

    def set_offset2(self, p_offset2):
        self.__offset2 = p_offset2

    def set_offset3(self, p_offset3):
        self.__offset3 = p_offset3

    def set_blocks(self, p_blocks):
        self.__blocks = p_blocks

    def set_type(self, p_type):
        self.__type = p_type

    def set_handler_ids(self, p_handler_ids):
        self.__handler_ids = p_handler_ids

    def get_doc(self):
        return self.__doc

    def get_iters(self):
        assert (self.__installed)
        doc = self.__doc
        iter1 = doc.get_iter_at_mark(self.__mark1)
        iter2 = doc.get_iter_at_mark(self.__mark2)
        iter3 = doc.get_iter_at_mark(self.__mark3)
        return (iter1, iter2, iter3)

    def get_offsets(self):
        assert (self.__installed)
        iter1, iter2, iter3 = self.get_iters()
        return (iter1.get_offset(), iter2.get_offset(), iter3.get_offset())

    def get_marks(self):
        return (self.__mark1, self.__mark2, self.__mark3)

    def get_blocks(self):
        return self.__blocks

    def get_type(self):
        return self.__type

    def get_tag(self):
        return self.__tag

    def get_anchor(self):
        return self.__anchor

    def get_handler_ids(self):
        return self.__handler_ids

    def collapse(self, p_set_higher_priority=True, p_show_label=True, p_rec=False):
        self.__tag.set_property("invisible", True)
        if p_set_higher_priority:
            if self.__installed:
                self.set_higher_priority()
            else:
                self.__pendings.append((self.set_higher_priority, ()))
        if p_show_label:
            if self.__installed:
                self.set_show_label(p_show_label)
            else:
                self.__pendings.append((self.set_show_label, (p_show_label, )))
        if p_rec:
            for block in self.__blocks:
                block.collapse(p_set_higher_priority, p_show_label, p_rec)

    def expand(self, p_set_lower_priority=True, p_rec=False):
        self.__tag.set_property("invisible", False)
        if p_set_lower_priority:
            if self.__installed:
                self.set_lower_priority()
            else:
                self.__pendings.append((self.set_lower_priority, ()))
        if self.__installed:
            self.set_show_label(False)
        else:
            self.__pendings.append((self.set_show_label, (False, )))
        if p_rec:
            for block in self.__blocks:
                block.expand(p_set_lower_priority, p_rec)

    def is_collapsed(self):
        return self.__tag.get_property("invisible")

    def set_higher_priority(self):
        assert (self.__installed)
        prio = self.__doc.get_tag_table().get_size() - 1
        self.__tag.set_priority(prio)

    def set_lower_priority(self):
        assert (self.__installed)
        self.__tag.set_priority(0)

    def set_show_label(self, p_show):
        anchor_is_visible = bool(self.__anchor and not self.__anchor.get_deleted())

        if p_show == anchor_is_visible:
            return

        doc = self.__doc

        def doc_set_handlers_blocked(p_block):
            for id_ in self.__handler_ids:
                if p_block:
                    doc.handler_block(id_)
                else:
                    doc.handler_unblock(id_)

        if p_show:
            assert (self.is_collapsed() and self.__installed)

        doc.begin_not_undoable_action()
        before = doc.get_modified()
        doc_set_handlers_blocked(True)

        if p_show:
            self.__anchor = doc.create_child_anchor(self.get_iters()[1])
        else:
            start = doc.get_iter_at_child_anchor(self.__anchor)
            end = doc.get_iter_at_offset(start.get_offset() + 1)
            doc.delete(start, end)
            self.__anchor = None

        doc_set_handlers_blocked(False)
        doc.set_modified(before)
        doc.end_not_undoable_action()

    def wrap_offset(self, p_offset):
        assert (self.__installed)
        offset1, offset2, offset3 = self.get_offsets()
        return offset1 <= p_offset < offset3

    def intersect_line(self, p_line):
        assert (self.__installed)
        line1, line3 = self.get_line_bounds()
        if line1 == None or line3 == None:
            return False
        return line1 <= p_line <= line3

    def get_line_bounds(self):
        assert (self.__installed)
        iter1, iter2, iter3 = self.get_iters()
        if iter1.compare(iter3) == -1:
            iter3.backward_char()
            return (iter1.get_line(), iter3.get_line())
        return (None, None)

    def uninstall(self, p_rec=False):
        if self.__installed:
            self.__installed = False
            doc = self.__doc
            for mark in self.get_marks():
                doc.delete_mark(mark)
            doc.remove_tag(self.__tag, *doc.get_bounds())
            doc.get_tag_table().remove(self.__tag)
            self.set_show_label(False)
        if p_rec:
            for block in self.__blocks:
                block.uninstall(p_rec)

    def pre_order(self):
        blocks = [self]
        for block in self.__blocks:
            blocks.extend(block.pre_order())
        return blocks

    def post_order(self):  # No se utiliza
        blocks = []
        for block in self.__blocks:
            blocks.extend(block.post_order())
        blocks.append(self)
        return blocks

    def bottom_up_across_order(self, p_left_to_right=True):
        blocks = [self]
        pos = -1
        while abs(pos) <= len(blocks):
            if p_left_to_right:
                blocks = blocks[pos].get_blocks() + blocks
            else:
                for block in blocks[pos].get_blocks():
                    blocks.insert(0, block)
            pos -= 1
        return blocks

    def get_leaves(self):  # No se utiliza
        blocks = []
        for block in self.__blocks:
            blocks.extend(block.get_leaves())
        if not self.__blocks:
            blocks.append(self)
        return blocks


class EditorFoldingBlockHolder(list):
    def __get_blocks_of_type(self, p_top_block, p_type=None, p_rec=True):
        blocks = []
        queue = [p_top_block]
        while queue:
            block = queue.pop(0)
            if p_type == None or block.get_type() == p_type:
                blocks.append(block)
                if not p_rec:
                    continue
            queue.extend(block.get_blocks())
        return blocks

    def get_blocks_of_type(self, p_type=None, p_rec=True):
        blocks = []
        for block in self:
            blocks.extend(self.__get_blocks_of_type(block, p_type, p_rec))
        return blocks

    def get_block_of_line(self, p_line, p_top_level=False, p_top_down=False):
        if p_top_level:
            blocks = self[:] if p_top_down else self[::-1]
        else:
            blocks = []
            if p_top_down:
                for block in self:
                    blocks.extend(block.bottom_up_across_order())
            else:
                for block in self[::-1]:
                    blocks.extend(block.bottom_up_across_order(False))
        for block in blocks:
            if block.intersect_line(p_line):
                return block
        return None

    def get_blocks_in_pre_order(self):
        blocks = []
        for block in self:
            blocks.extend(block.pre_order())
        return blocks

    def get_collapsed_blocks(self):
        pre_order = self.get_blocks_in_pre_order()
        blocks = [block for block in pre_order if block.is_collapsed()]
        return blocks

    def uninstall_all_blocks(self):
        for block in self:
            block.uninstall(True)


class EditorFoldingBlockLabel(gtk.Label):
    def __init__(self, p_text, p_view):
        gtk.Label.__init__(self, p_text)

        context = p_view.get_pango_context()
        desc = context.get_font_description()
        self.modify_font(desc)
        self.set_sensitive(False)

        self.connect("expose-event", self.__on_expose_event)
        #p_view.connect("style-set")  FIXME: hacer algo para cuando cambie el font_desc del view

    def __on_expose_event(self, p_label, p_event):
        window = p_event.window
        gc_fill = window.new_gc()
        withe = gc_fill.get_colormap().alloc_color("#FFFFFF")
        gc_fill.set_foreground(withe)
        gc_border = p_label.get_style().fg_gc[p_label.state]
        alloc = p_label.get_allocation()
        x = alloc.x
        y = alloc.y
        width = alloc.width
        height = alloc.height

        window.draw_rectangle(gc_fill, True, x, y, width, height)
        window.draw_rectangle(gc_border, False, x, y, width - 1, height - 1)
