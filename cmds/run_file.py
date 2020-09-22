import os
import gtk
import time
import gobject

from cmds.command import Command
from util.constants import VALUE
from conn.terminal import TerminalState


class RunFile(Command):
    __gsignals__ = {"response_request": (gobject.SIGNAL_RUN_LAST,
                                         gobject.TYPE_NONE,
                                         ())}

    def __init__(self, p_funcname, p_args=(), p_sep="", p_file=None, p_prio=0):
        Command.__init__(self, p_prio)

        self.__funcname = p_funcname
        self.__args = p_args
        self.__sep = p_sep
        self.__file = p_file

    def execute(self, p_conn):
        funcname = self.__funcname
        args = self.__args
        sep = self.__sep
        file_ = self.__file

        while True:
            in_loadpath = not file_ or p_conn.is_file_in_loadpath(file_)

            if in_loadpath:
                parentesis = "(" + ", ".join(args) + ")" if args else ""
                end_mark = "#%s#%s" %(VALUE, os.linesep)
                cmd = funcname + parentesis + sep + " " + end_mark
                self.__clear_prompt(p_conn)
                self.__execute_command(cmd, p_conn, False, end_mark)
                return True
            else:
                self.emit_("response_request")
                response = self.get_data("response")
                self.set_data("response", None)
                if response == 2:
                    return

                dir = os.path.dirname(file_)
                if response == 0:
                    cmd = "cd '%s';\n" %dir
                else:  # response = 1
                    cmd = "addpath('%s', '-begin');\n" %dir

                self.__execute_command(cmd, p_conn)

    def __execute_command(self, p_cmd, p_conn, p_eat_all=True, p_until=""):
        # FIXME: ver si esto se puede re-utilizar

        term = p_conn.get_terminal()
        buff = term.buff
        term.feed_child(p_cmd)

        if p_eat_all:
            p_conn.wait_until_ready()
            buff.delete(0, buff.get_char_count())
        else:
            while True:
                text = buff.get_text(0, buff.get_char_count(), True)
                index = text.find(p_until)

                if index != -1:
                    buff.delete(0, index + len(p_until))
                    break

                time.sleep(0.001)

    def __clear_prompt(self, p_conn):
        state = p_conn.get_terminal().state_
        psx = 1 if state == TerminalState.READY else 3
        gtk.gdk.threads_enter()
        p_conn.get_mwindow().get_cmdwindow().replace_prompt(psx, "")
        gtk.gdk.threads_leave()
