from cmds.command import Command


class SetDebugOnEvent(Command):
    def __init__(self, p_debug_on_event, p_prio=0):
        Command.__init__(self, p_prio)
        self.__debug_on_event = p_debug_on_event

    def execute(self, p_conn):
        dct = {"err": "debug_on_error(%d);",
               "war": "debug_on_warning(%d);",
               "int": "debug_on_interrupt(%d);"}

        cmd = ""
        for (key, val) in self.__debug_on_event.iteritems():
            if key in dct:
                cmd += dct[key] %(int(val), )
        cmd += "\n"

        self.__execute_command(cmd, p_conn)

    def __execute_command(self, p_cmd, p_conn):
        # FIXME: ver si esto se puede re-utilizar

        term = p_conn.get_terminal()
        buff = term.buff
        term.feed_child(p_cmd)
        p_conn.wait_until_ready()
        buff.delete(0, buff.get_char_count())
