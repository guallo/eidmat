from edebugger.ocompiler.token import TokenKind, KeyWords, Token, Position
from edebugger.ocompiler.symbol_table import Symbol


class Scanner:
    keywors = KeyWords()

    def __init__(self, source, symtab):
        self.source = source
        self.symtab = symtab

        self.stack = []
        self.backslash = False

    def next_token(self):
        # FIXME: ESTO SE TIENE QUE HACER CON EXPRESIONES
        #        REGULARES PARA GANAR EN VELOCIDAD

        # FIXME: falto tener en cuenta '...' (es parecido a '\' pero no igual)
        #        (este no funciona igual en MATLAB y en OCTAVE)

        # FIXME: falto tener en cuenta que '%{' y '%}' se pueden anidar
        #        y solo son de mas de una linea si estan en una linea solos
        #        (ver ayuda de MATLAB)
        #        tambien se pueden ver como '#{' y '#}'

        # FIXME: falto tener en cuenta el transpose "hola"'
        #        (me confunde con el comienzo de un single coute string)

        source = self.source
        stack = self.stack
        lexema = ""
        state = 0

        while True:
            char = source.next_char()

            if state == 0:  # Start
                lexema += char

                if self.backslash and char not in " \t#%":
                    self.backslash = False

                if char.isalpha() or char == "_" or char == "$":
                    state = 1
                elif char == "'":
                    state = 2
                elif char == '"':
                    state = 7
                elif char == "\\":
                    state = 10
                elif char == ".":
                    state = 12
                elif char == "#":
                    comment_inline = True
                    state = 3
                elif char == "%":
                    state = 4
                elif char == "(" or char == "{":
                    stack.append(char)
                    kind = TokenKind.UNKNOWN
                    break
                elif char == ")" or char == "}":
                    if stack and stack[-1] + char in ("()", "{}"):
                        stack.pop()
                    kind = TokenKind.UNKNOWN
                    break
                elif char == "]":
                    kind = TokenKind.CLOSE_BRACE
                    break
                elif char == "[":
                    kind = TokenKind.OPEN_BRACE
                    break
                elif char == "=":
                    kind = TokenKind.EQUAL
                    break
                elif char == ",":
                    kind = TokenKind.COMMA
                    break
                elif char == "\0":
                    kind = TokenKind.END_OF_INPUT
                    break
                elif char in " \t\n\r\f\v":
                    lexema = lexema[:-1]
                else:
                    kind = TokenKind.UNKNOWN
                    break

            elif state == 1:  # Completing identifier
                if char.isalnum() or char == "_" or char == "$":
                    lexema += char
                else:
                    source.back()
                    kind = TokenKind.IDENTIFIER
                    break

            elif state == 2:  # Eating single coute string
                if char == "\n" or char == "\0":
                    source.back()
                    kind = TokenKind.UNKNOWN
                    break
                else:
                    if char == "'":
                        state = 6
                    lexema += char

            elif state == 3:  # Eating comment
                if char == "\0":
                    source.back()
                    kind = TokenKind.COMMENT
                    break
                elif comment_inline:
                    if char == "\n":
                        source.back()
                        kind = TokenKind.COMMENT
                        break
                    lexema += char
                elif char == "%":
                    state = 5
                    lexema += char
                else:
                    lexema += char

            elif state == 4:  # Begining comment with '%'
                if char == "\0" or char == "\n":
                    source.back()
                    kind = TokenKind.COMMENT
                    #self.backslash = False
                    break
                else:
                    comment_inline = self.backslash or char != "{"
                    state = 3
                    lexema += char
                    #self.backslash = False

            elif state == 5:  # Ending comment of multiple lines '}'
                if char == "}":
                    lexema += char
                    kind = TokenKind.COMMENT
                    break
                elif char == "\0":
                    source.back()
                    kind = TokenKind.COMMENT
                    break
                else:
                    state = 3
                    lexema += char

            elif state == 6:  # Ending single coute string
                if char == "'":
                    state = 2
                    lexema += char
                else:
                    source.back()
                    kind = TokenKind.UNKNOWN
                    break

            elif state == 7:  # Eating double coute string
                if char == '"':
                    lexema += char
                    state = 8
                elif char == "\\":
                    lexema += char
                    state = 9
                elif char == "\n" or char == "\0":
                    source.back()
                    kind = TokenKind.UNKNOWN
                    break
                else:
                    lexema += char

            elif state == 8:  # Ending double coute string
                if char == '"':
                    lexema += char
                    state = 7
                else:
                    source.back()
                    kind = TokenKind.UNKNOWN
                    break

            elif state == 9:  # Processing '\' in double coute string
                if char == "\0":
                    source.back()
                    kind = TokenKind.UNKNOWN
                    break
                elif char != " " and char != "\t":
                    lexema += char
                    state = 7
                else:
                    lexema += char
                    state = 11

            elif state == 10:  # Processing '\' out
                kind = TokenKind.UNKNOWN

                if char == "=":
                    lexema += char
                else:
                    source.back()
                    self.backslash = True

                break

            elif state == 11:  # Processing ' ' and '\t' in double coute string after '\'
                if char == "\n":
                    lexema += char
                    state = 7
                elif char != " " and char != "\t":
                    state = 7
                    source.back()
                else:
                    lexema += char

            elif state == 12:  # Processing '.'
                if char == "'":
                    lexema += char
                    kind = TokenKind.UNKNOWN
                    break
                elif char == "\\":
                    lexema += char
                    state = 13
                else:
                    source.back()
                    kind = TokenKind.UNKNOWN
                    break

            elif state == 13:  # Processing '\' after '.'
                kind = TokenKind.UNKNOWN

                if char == "=":
                    lexema += char
                else:
                    source.back()

                break

        start = source.cursor - len(lexema)
        line = source.get_line_no_at(start)
        end = source.cursor - 1
        position = Position(line, start, end)

        if kind == TokenKind.IDENTIFIER:
            if lexema in self.keywors:
                kind = self.keywors[lexema]

            symbol = Symbol(kind, lexema)
            entry = self.symtab.append(symbol)

            return Token(kind, lexema, position, entry)
        return Token(kind, lexema, position)
