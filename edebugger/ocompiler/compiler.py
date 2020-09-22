from edebugger.ocompiler.symbol_table import SymbolTable
from edebugger.ocompiler.scanner import Scanner
from edebugger.ocompiler.parser import Parser


class Compiler:
    def __init__(self, source):
        self.symtab = SymbolTable()
        self.scanner = Scanner(source, self.symtab)
        self.parser = Parser(self.scanner, self.symtab)

    def compile(self):
        return self.parser.parse()
