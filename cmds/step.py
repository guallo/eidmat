import os
import gtk
import time

from cmds.command import Command
from util.constants import VALUE


class Step(Command):
    def __init__(self, p_arg=1, p_verbose=True, p_prio=0):
        Command.__init__(self, p_prio)
        self.__arg = p_arg
        self.__verbose = p_verbose

    def execute(self, p_conn):
        # FIXME: implementar para cuando self.__verbose = False

        if not p_conn.is_debug_mode():
            return

        gtk.gdk.threads_enter()
        p_conn.get_mwindow().get_cmdwindow().replace_prompt(3, "")
        gtk.gdk.threads_leave()

        end_mark = "#%s#%s" %(VALUE, os.linesep)
        arg = self.__arg
        arg = ("out", "in")[arg] if type(arg) == bool else str(arg)
        cmd = "dbstep %s;" %arg + " " + end_mark

        self.__execute_command(cmd, p_conn, False, end_mark)
        return True

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
