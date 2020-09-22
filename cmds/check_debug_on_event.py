import gobject

from cmds.command import Command
from util.data import Data


class CheckDebugOnEvent(Command):
    __gsignals__ = {"debug_on_event_update_request": (gobject.SIGNAL_RUN_LAST,
                                                      gobject.TYPE_NONE,
                                                      (Data, ))
                    }

    def __init__(self, p_prio=0):
        Command.__init__(self, p_prio)

    def execute(self, p_conn):
        debug_on_event = p_conn.get_debug_on_event()

        data = Data()
        data.set_data("debug_on_event", debug_on_event)

        self.emit_("debug_on_event_update_request", data)
