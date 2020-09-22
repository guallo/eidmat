from edebugger.ocompiler.token import TokenKind
from edebugger.ocompiler.ast import ASTProgram, ASTBlock, ASTFunction, ASTFuncName


class Parser:
    begin_tokens = (TokenKind.DO, TokenKind.FOR,
                   TokenKind.FUNCTION, TokenKind.IF,
                   TokenKind.ELSEIF, TokenKind.ELSE,
                   TokenKind.SWITCH, TokenKind.CASE,
                   TokenKind.OTHERWISE, TokenKind.TRY,
                   TokenKind.CATCH, TokenKind.UNWIND_PROTECT,
                   TokenKind.UNWIND_PROTECT_CLEANUP,
                   TokenKind.WHILE)

    end_tokens = (TokenKind.UNTIL, TokenKind.END,
                   TokenKind.ENDFOR, TokenKind.ENDFUNCTION,
                   TokenKind.ENDIF, TokenKind.ELSEIF,
                   TokenKind.ELSE, TokenKind.ENDSWITCH,
                   TokenKind.CASE, TokenKind.OTHERWISE,
                   TokenKind.CATCH, TokenKind.END_TRY_CATCH,
                   TokenKind.UNWIND_PROTECT_CLEANUP,
                   TokenKind.END_UNWIND_PROTECT,
                   TokenKind.ENDWHILE)

    couples = {TokenKind.DO: (TokenKind.UNTIL, ),
            TokenKind.FOR: (TokenKind.END, TokenKind.ENDFOR),
            TokenKind.FUNCTION: (TokenKind.END, TokenKind.ENDFUNCTION),
            TokenKind.IF: (TokenKind.END, TokenKind.ENDIF,
                            TokenKind.ELSEIF, TokenKind.ELSE),
            TokenKind.ELSEIF: (TokenKind.END, TokenKind.ENDIF,
                                TokenKind.ELSEIF, TokenKind.ELSE),
            TokenKind.ELSE: (TokenKind.END, TokenKind.ENDIF),
            TokenKind.SWITCH: (TokenKind.END, TokenKind.ENDSWITCH),
            TokenKind.CASE: (TokenKind.END, TokenKind.ENDSWITCH,
                            TokenKind.CASE, TokenKind.OTHERWISE),
            TokenKind.OTHERWISE: (TokenKind.END, TokenKind.ENDSWITCH),
            TokenKind.TRY: (TokenKind.END, TokenKind.END_TRY_CATCH,
                            TokenKind.CATCH),
            TokenKind.CATCH: (TokenKind.END, TokenKind.END_TRY_CATCH),
            TokenKind.UNWIND_PROTECT: (TokenKind.END,
                                        TokenKind.END_UNWIND_PROTECT,
                                        TokenKind.UNWIND_PROTECT_CLEANUP),
            TokenKind.UNWIND_PROTECT_CLEANUP: (TokenKind.END,
                                                TokenKind.END_UNWIND_PROTECT),
            TokenKind.WHILE: (TokenKind.END, TokenKind.ENDWHILE)}

    def __init__(self, scanner, symtab):
        self.scanner = scanner
        self.symtab = symtab
        self.curtoken = None

        self.tokens = []

    def next_token(self):
        scanner = self.scanner
        tokens = self.tokens

        while True:
            token = scanner.next_token()
            tokens.append(token)
            kind = token.kind

            if (kind == TokenKind.END_OF_INPUT) or (not scanner.stack and \
                kind not in (TokenKind.UNKNOWN, TokenKind.COMMENT)):
                return token

    def next_begin_token(self):
        while True:
            token = self.next_token()

            if self.is_begin_token(token) or \
                token.kind == TokenKind.END_OF_INPUT:

                return token

    def next_begin_or_end_token(self):
        while True:
            token = self.next_token()

            if self.is_begin_or_end_token(token) or \
                token.kind == TokenKind.END_OF_INPUT:

                return token

    def is_begin_token(self, token):
        return token.kind in self.begin_tokens

    def is_end_token(self, token):
        return token.kind in self.end_tokens

    def is_begin_or_end_token(self, token):
        return self.is_begin_token(token) or self.is_end_token(token)

    def match(self, start_kind, end_kind):
        return end_kind in self.couples[start_kind]

    def parse(self):
        self.curtoken = self.next_begin_token()
        return self.program()

    def program(self):
        # program : blocks END_OF_INPUT

        tokens = self.tokens
        is_script = True

        for token in tokens:
            if token.kind != TokenKind.COMMENT:
                if token.kind == TokenKind.FUNCTION:
                    is_script = False
                break

        blocks = self.blocks(None)

        tokens = tokens[:-1]

        if tokens:
            start_pos = tokens[0].position
            end_pos = tokens[-1].position
        else:
            start_pos = end_pos = None

        return ASTProgram(start_pos, end_pos, blocks, is_script)

    def blocks(self, start_kind=None):
        # blocks : //empty | block blocks

        blocks = []
        change = False

        while self.curtoken.kind != TokenKind.END_OF_INPUT:
            if change or not self.is_end_token(self.curtoken):
                block, change = self.block()
                blocks.append(block)
            elif start_kind != None and \
                self.match(start_kind, self.curtoken.kind):
                break
            else:
                self.curtoken = self.next_begin_or_end_token()

        return blocks

    def block(self):
        # block : do_block
        #       | for_block
        #       | function_block
        #       | if_block
        #       | elseif_block
        #       | else_block
        #       | switch_block
        #       | case_block
        #       | otherwise_block
        #       | try_block
        #       | catch_block
        #       | unwind_protect_block
        #       | unwind_protect_cleanup_block
        #       | while_block

        kind = self.curtoken.kind
        change = False

        if kind == TokenKind.FUNCTION:
            return self.function_block(), change

        start_pos = self.curtoken.position
        self.curtoken = self.next_begin_or_end_token()
        blocks = self.blocks(kind)
        end_pos = self.curtoken.position

        curkind = self.curtoken.kind

        if curkind != TokenKind.END_OF_INPUT:
            if kind == TokenKind.IF:
                if curkind in (TokenKind.ELSEIF, TokenKind.ELSE):
                    change = True
            elif kind == TokenKind.ELSEIF:
                if curkind in (TokenKind.ELSEIF, TokenKind.ELSE):
                    change = True
            elif kind == TokenKind.CASE:
                if curkind in (TokenKind.CASE, TokenKind.OTHERWISE):
                    change = True
            elif kind == TokenKind.TRY:
                if curkind in (TokenKind.CATCH, ):
                    change = True
            elif kind == TokenKind.UNWIND_PROTECT:
                if curkind in (TokenKind.UNWIND_PROTECT_CLEANUP, ):
                    change = True

            if not change:
                self.curtoken = self.next_begin_or_end_token()

        return ASTBlock(start_pos, end_pos, blocks), change

    def function_block(self):
        # function_block : function_header blocks ENDFUNCTION

        start_pos = self.curtoken.position
        funcname = self.function_header()
        blocks = self.blocks(TokenKind.FUNCTION)
        end_pos = self.curtoken.position

        if self.curtoken.kind != TokenKind.END_OF_INPUT:
            self.curtoken = self.next_begin_or_end_token()

        return ASTFunction(start_pos, end_pos, blocks, funcname)

    def function_header(self):
        # function_header : FUNCTION function_header1

        self.curtoken = self.next_token()
        funcname = self.function_header1()

        if not funcname:
            funcname = ASTFuncName(None, None, None)

        return funcname

    def function_header1(self):
        # function_header1 : IDENTIFIER function_header2
        #                  | '[' return_list_cont '=' IDENTIFIER

        if self.curtoken.kind == TokenKind.IDENTIFIER:
            curtoken = self.curtoken
            self.curtoken = self.next_token()

            if self.curtoken.kind in (TokenKind.EQUAL, TokenKind.COMMA):
                return self.function_header2()
            if not self.is_begin_or_end_token(self.curtoken) and \
                self.curtoken.kind != TokenKind.END_OF_INPUT:
                self.curtoken = self.next_begin_or_end_token()
            return ASTFuncName(curtoken.position, curtoken.lexema,
                                                        curtoken.entry)

        if self.curtoken.kind == TokenKind.OPEN_BRACE:
            self.curtoken = self.next_token()

            if self.return_list_cont():
                if self.curtoken.kind == TokenKind.EQUAL:
                    self.curtoken = self.next_token()

                    if self.curtoken.kind == TokenKind.IDENTIFIER:
                        curtoken = self.curtoken
                        self.curtoken = self.next_begin_or_end_token()
                        return ASTFuncName(curtoken.position,
                                        curtoken.lexema, curtoken.entry)
            if not self.is_begin_or_end_token(self.curtoken) and \
                self.curtoken.kind != TokenKind.END_OF_INPUT:
                self.curtoken = self.next_begin_or_end_token()
            return None

        if not self.is_begin_or_end_token(self.curtoken) and \
            self.curtoken.kind != TokenKind.END_OF_INPUT:
            self.curtoken = self.next_begin_or_end_token()
        return None

    def function_header2(self):
        # function_header2 : //empty (se chequeo anteriormente que no es vacio)
        #                  | '=' IDENTIFIER
        #                  | ',' IDENTIFIER more_indetifiers '=' IDENTIFIER

        is_equal = self.curtoken.kind == TokenKind.EQUAL
        self.curtoken = self.next_token()

        if self.curtoken.kind != TokenKind.IDENTIFIER:
            if not self.is_begin_or_end_token(self.curtoken) and \
                self.curtoken.kind != TokenKind.END_OF_INPUT:
                self.curtoken = self.next_begin_or_end_token()
            return None

        if is_equal:
            curtoken = self.curtoken
            self.curtoken = self.next_begin_or_end_token()
            return ASTFuncName(curtoken.position, curtoken.lexema,
                                                        curtoken.entry)

        self.curtoken = self.next_token()
        if self.more_indetifiers():
            if self.curtoken.kind == TokenKind.EQUAL:
                self.curtoken = self.next_token()
                if self.curtoken.kind == TokenKind.IDENTIFIER:
                    curtoken = self.curtoken
                    self.curtoken = self.next_begin_or_end_token()
                    return ASTFuncName(curtoken.position, curtoken.lexema,
                                                            curtoken.entry)
        if not self.is_begin_or_end_token(self.curtoken) and \
            self.curtoken.kind != TokenKind.END_OF_INPUT:
            self.curtoken = self.next_begin_or_end_token()
        return None

    def more_indetifiers(self):
        # more_indetifiers : //empty
        #                  | ',' IDENTIFIER more_indetifiers

        if self.curtoken.kind == TokenKind.COMMA:
            self.curtoken = self.next_token()
            if self.curtoken.kind == TokenKind.IDENTIFIER:
                self.curtoken = self.next_token()
                return self.more_indetifiers()
            return False

        return True

    def return_list_cont(self):
        # return_list_cont : ']'
        #                  | IDENTIFIER more_indetifiers ']'

        if self.curtoken.kind == TokenKind.CLOSE_BRACE:
            self.curtoken = self.next_token()
            return True

        if self.curtoken.kind == TokenKind.IDENTIFIER:
            self.curtoken = self.next_token()
            if self.more_indetifiers():
                if self.curtoken.kind == TokenKind.CLOSE_BRACE:
                    self.curtoken = self.next_token()
                    return True

        return False
