import re
import os

from edebugger.completion.symbol import Symbol


class Extractor:
    def __init__(self):
        header_pattern = "^--.+--$"
        symbol_pattern = "^\#\n.+\n\{\n((\n)|(\}.+\n)|([^\}].*\n))*\}$"
        symbol_pattern = symbol_pattern.replace("\n", os.linesep)
        both_pattern = "(%s)|(%s)" %(header_pattern, symbol_pattern)
        self.__header_pattern = re.compile(header_pattern, re.M)
        self.__symbol_pattern = re.compile(symbol_pattern, re.M)
        self.__both_pattern = re.compile(both_pattern, re.M)

    def extract(self, p_file):
        f = open(p_file, "r")
        string = f.read()
        f.close()

        index = 0
        length = len(string)
        blocks = []
        header_pattern = self.__header_pattern
        symbol_pattern = self.__symbol_pattern
        both_pattern = self.__both_pattern
        searching_header = True
        curblock = None

        while True:
            string = string[index : ]

            if searching_header:
                match = re.search(header_pattern, string)
                if match:
                    header = match.group()[2 : -2]
                    index = match.end()
                    curblock = {header: []}
                    blocks.append(curblock)
                    searching_header = False
                else:
                    break
            else:
                match = re.search(both_pattern, string)
                if match:
                    text = match.group()
                    if text[0] == "#":  # symbol
                        brace = "\n{".replace("\n", os.linesep)
                        brace_index = text.index(brace)
                        lexema = text[text.index(os.linesep) + 1 : brace_index]
                        info = text[brace_index + 3 : -2]
                        symbol = Symbol(lexema, info)
                        curblock.values()[0].append(symbol)
                        index = match.end()
                    else:  # header
                        index = match.start()
                        searching_header = True
                else:
                    break

            if index >= length:
                break

        return blocks
