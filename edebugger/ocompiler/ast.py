class AST:
    def __init__(self, start_pos):
        self.start_pos = start_pos

    def visit(self, visitor, *args):
        raise NotImplementedError()


class ASTBlock(AST):
    def __init__(self, start_pos, end_pos, blocks):
        AST.__init__(self, start_pos)
        self.end_pos = end_pos
        self.blocks = blocks

    def visit(self, visitor, *args):
        return visitor.visit_block(self, *args)


class ASTProgram(ASTBlock):
    def __init__(self, start_pos, end_pos, blocks, is_script):
        ASTBlock.__init__(self, start_pos, end_pos, blocks)
        self.is_script = is_script

    def visit(self, visitor, *args):
        return visitor.visit_program(self, *args)


class ASTFunction(ASTBlock):
    def __init__(self, start_pos, end_pos, blocks, funcname):
        ASTBlock.__init__(self, start_pos, end_pos, blocks)
        self.funcname = funcname

    def visit(self, visitor, *args):
        return visitor.visit_function(self, *args)


class ASTFuncName(AST):
    def __init__(self, start_pos, lexema, entry):
        AST.__init__(self, start_pos)
        self.lexema = lexema
        self.entry = entry

    def visit(self, visitor, *args):
        return visitor.visit_funcname(self, *args)
