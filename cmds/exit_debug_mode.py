import os
import gtk

from cmds.command import Command


class ExitDebugMode(Command):
    def __init__(self, p_prio=0):
        Command.__init__(self, p_prio)

    def execute(self, p_conn):
        if not p_conn.is_debug_mode():
            return

        term = p_conn.get_terminal()
        buff = term.buff
        term.feed_child("dbquit();%s" %os.linesep)
        p_conn.wait_until_ready()
        buff.delete(0, buff.get_char_count())

        cmdwindow = p_conn.get_mwindow().get_cmdwindow()

        gtk.gdk.threads_enter()
        cmdwindow.replace_prompt(3, cmdwindow.get_ps1())
        gtk.gdk.threads_leave()
