from edebugger.editor_folding_block import EditorFoldingBlock,\
                                            EditorFoldingBlockType,\
                                            EditorFoldingBlockHolder


class Visitor:
    def visit_program(self, program, *args):
        raise NotImplementedError()

    def visit_block(self, block, *args):
        raise NotImplementedError()

    def visit_function(self, function, *args):
        raise NotImplementedError()

    def visit_funcname(self, funcname, *args):
        raise NotImplementedError()


class FuncFileChecker(Visitor):
    def __init__(self, ast, symtab):
        self.ast = ast
        self.symtab = symtab
        self.functions = []
        self.curfunc = None

    def check(self):
        self.ast.visit(self)
        return self.functions

    def visit_program(self, program, *args):
        if program.is_script:
            return

        for block in program.blocks:
            block.visit(self)

        curfunc = self.curfunc

        if curfunc:
            curfunc["end"] = program.end_pos.line
            self.functions.append(curfunc)

    def visit_block(self, block, *args):
        for b in block.blocks:
            b.visit(self)

    def visit_function(self, function, *args):
        lexema = function.funcname.visit(self)

        if lexema:
            curfunc = self.curfunc
            line = function.start_pos.line

            if curfunc:

                # FIXME: curfunc["end"] = 'line' si el token anterior
                #        a 'function' esta en la misma 'line', sino
                #        curfunc["end"] = 'line - 1'
                curfunc["end"] = line

                self.functions.append(curfunc)

            self.curfunc = {"function": lexema,
                            "start": line}

        for block in function.blocks:
            block.visit(self)

    def visit_funcname(self, funcname, *args):
        return funcname.lexema


class FoldingBlockChecker(Visitor):
    def __init__(self, ast, symtab):
        self.ast = ast
        self.symtab = symtab
        self.holder = EditorFoldingBlockHolder()

    def check(self):
        self.ast.visit(self)
        return self.holder

    def visit_program(self, program, *args):
        for block in program.blocks:
            self.holder.append(block.visit(self))

    def visit_block(self, block, *args):
        folding = EditorFoldingBlock()
        if args:
            folding.set_type(args[0])
        else:
            folding.set_type(EditorFoldingBlockType.NORMAL)
        start_pos = block.start_pos
        end_pos = block.end_pos
        folding.set_offset1(start_pos.start)
        if start_pos.line == end_pos.line:
            folding.set_offset2(start_pos.end + 1)
        folding.set_offset3(end_pos.end + 1)
        childs = []
        for b in block.blocks:
            childs.append(b.visit(self))
        folding.set_blocks(childs)
        return folding

    def visit_function(self, function, *args):
        return self.visit_block(function, EditorFoldingBlockType.FUNCTION)
