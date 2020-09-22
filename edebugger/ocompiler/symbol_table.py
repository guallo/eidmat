class Symbol:
    def __init__(self, kind, lexema):
        self.kind = kind
        self.lexema = lexema

    def __cmp__(self, symbol):
        return cmp(self.lexema, symbol.lexema)


class SymbolTable(list):
    def append(self, symbol):
        if symbol not in self:
            list.append(self, symbol)
        return self.index(symbol)
