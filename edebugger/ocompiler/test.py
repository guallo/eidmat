from source import SourceFile
from symbol_table import SymbolTable
from scanner import Scanner
from token import TokenKind
from parser import Parser

#source = SourceFile("/usr/share/octave/3.2.3/m/pkg/pkg.m")
#source = SourceFile("/usr/share/octave/3.2.3/m/plot/print.m")
#source = SourceFile("/usr/share/octave/3.2.3/m/miscellaneous/edit.m")
#source = SourceFile("/usr/share/octave/3.2.3/m/plot/__go_draw_axes__.m")
source = SourceFile("/home/eacuesta/Desktop/untitled.m")
symbol_table = SymbolTable()
scanner = Scanner(source, symbol_table)

"""
while True:
    token = scanner.next_token()
    #print token.lexema, token.position.line

    if token.kind == TokenKind.END_OF_INPUT:
        break
"""

parser = Parser(scanner, symbol_table)
ast = parser.parse()

def disp(ast, nested):
    for block in ast.blocks:
        print nested + str(block), block.start_pos.line, block.end_pos.line

        disp(block, nested + "|   ")

disp(ast, "")
