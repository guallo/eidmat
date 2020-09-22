class Source:
    def __init__(self, string):
        self.string = string + "\0"
        self.cursor = 0

    def next_char(self):
        char = self.string[self.cursor]
        self.cursor += 1
        return char

    def back(self):
        self.cursor -= 1

    def get_line_no_at(self, index):  # index starts from 0
        return self.string.count('\n', 0, index) + 1


class SourceString(Source):
    pass


class SourceFile(Source):
    def __init__(self, path):
        file_ = open(path, "r")
        string = file_.read()
        file_.close()

        Source.__init__(self, string)
