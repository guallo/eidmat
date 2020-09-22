class TokenKind:
    (IDENTIFIER,
    DO,
    UNTIL,
    FOR,
    END,
    ENDFOR,
    ENDFUNCTION,
    IF,
    ENDIF,
    ELSEIF,
    ELSE,
    SWITCH,
    ENDSWITCH,
    CASE,
    OTHERWISE,
    TRY,
    CATCH,
    END_TRY_CATCH,
    UNWIND_PROTECT,
    END_UNWIND_PROTECT,
    UNWIND_PROTECT_CLEANUP,
    WHILE,
    ENDWHILE,
    FUNCTION,
    OPEN_BRACE,
    CLOSE_BRACE,
    COMMA,
    EQUAL,
    END_OF_INPUT,
    COMMENT,
    UNKNOWN) = range(31)


class KeyWords(dict):
    def __init__(self):
        dict.__init__(self)

        self["do"] = TokenKind.DO
        self["until"] = TokenKind.UNTIL
        self["for"] = TokenKind.FOR
        self["end"] = TokenKind.END
        self["endfor"] = TokenKind.ENDFOR
        self["endfunction"] = TokenKind.ENDFUNCTION
        self["if"] = TokenKind.IF
        self["endif"] = TokenKind.ENDIF
        self["elseif"] = TokenKind.ELSEIF
        self["else"] = TokenKind.ELSE
        self["switch"] = TokenKind.SWITCH
        self["endswitch"] = TokenKind.ENDSWITCH
        self["case"] = TokenKind.CASE
        self["otherwise"] = TokenKind.OTHERWISE
        self["try"] = TokenKind.TRY
        self["catch"] = TokenKind.CATCH
        self["end_try_catch"] = TokenKind.END_TRY_CATCH
        self["unwind_protect"] = TokenKind.UNWIND_PROTECT
        self["end_unwind_protect"] = TokenKind.END_UNWIND_PROTECT
        self["unwind_protect_cleanup"] = TokenKind.UNWIND_PROTECT_CLEANUP
        self["while"] = TokenKind.WHILE
        self["endwhile"] = TokenKind.ENDWHILE
        self["function"] = TokenKind.FUNCTION


class Token:
    def __init__(self, kind, lexema, position, entry=None):
        self.kind = kind
        self.lexema = lexema
        self.position = position
        self.entry = entry


class Position:
    def __init__(self, line, start, end):
        self.line = line
        self.start = start
        self.end = end
