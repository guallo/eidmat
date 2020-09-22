from cmds.command import Command


class ClearBreakpoints(Command):
    def __init__(self, p_funcname, p_lines=None, p_file=None, p_prio=0):
        Command.__init__(self, p_prio)

        self.__funcname = p_funcname
        self.__lines = p_lines
        self.__file = p_file

    def execute(self, p_conn):
        funcname = self.__funcname
        lines = self.__lines
        file = self.__file
        in_loadpath = not file or p_conn.is_file_in_loadpath(file)

        if in_loadpath:
            if funcname[1]:
                formatted_name = "['%s', filemarker(), '%s']" \
                                    %(funcname[0], funcname[1])
            else:
                formatted_name = "'%s'" %funcname[0]

            if lines:
                formatted_lines = ", ".join((str(l) for l in lines))
            else:
                formatted_lines = "dbstatus(%s)" %formatted_name

            cmd = "dbclear(%s, %s);\n" %(formatted_name, formatted_lines)
            self.__execute_command(cmd, p_conn)

    def __execute_command(self, p_cmd, p_conn):
        # FIXME: ver si esto se puede re-utilizar

        term = p_conn.get_terminal()
        buff = term.buff
        term.feed_child(p_cmd)
        p_conn.wait_until_ready()
        buff.delete(0, buff.get_char_count())
