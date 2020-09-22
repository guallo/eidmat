import os
import gobject

from cmds.command import Command
from util.constants import VAR


class SetBreakpoints(Command):
    __gsignals__ = {"response_request": (gobject.SIGNAL_RUN_LAST,
                                         gobject.TYPE_NONE,
                                         ())}

    def __init__(self, p_lines, p_funcname, p_file=None, p_prio=0):
        Command.__init__(self, p_prio)

        self.__lines = p_lines
        self.__funcname = p_funcname
        self.__file = p_file

    def execute(self, p_conn):
        lines = self.__lines
        funcname = self.__funcname
        file = self.__file

        while True:
            in_loadpath = not file or p_conn.is_file_in_loadpath(file)

            if in_loadpath:
                if funcname[1]:
                    formatted_name = "['%s', filemarker(), '%s']" \
                                        %(funcname[0], funcname[1])
                else:
                    formatted_name = "'%s'" %funcname[0]

                formatted_lines = ", ".join((str(l) for l in lines))
                cmd = "%s = dbstop(%s, %s); clear %s;\n" \
                        %(VAR, formatted_name, formatted_lines, VAR)

                self.__execute_command(cmd, p_conn)
                return
            else:
                self.emit_("response_request")
                response = self.get_data("response")
                self.set_data("response", None)
                if response == 2:
                    return
                
                dir = os.path.dirname(file)
                if response == 0:
                    cmd = "cd '%s';\n" %dir
                else:  # response = 1
                    cmd = "addpath('%s', '-begin');\n" %dir

                self.__execute_command(cmd, p_conn)

    def __execute_command(self, p_cmd, p_conn):
        # FIXME: ver si esto se puede re-utilizar

        term = p_conn.get_terminal()
        buff = term.buff
        term.feed_child(p_cmd)
        p_conn.wait_until_ready()
        buff.delete(0, buff.get_char_count())
