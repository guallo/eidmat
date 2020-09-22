import gobject

from cmds.command import Command
from util.data import Data


class CheckStack(Command):
    __gsignals__ = {"stack_update_request": (gobject.SIGNAL_RUN_LAST,
                                             gobject.TYPE_NONE,
                                             (Data, ))
                   }

    def __init__(self, p_file, p_omit=0, p_prio=0):
        Command.__init__(self, p_prio)

        self.__file = p_file
        self.__omit = p_omit

    def execute(self, p_conn):
        if "is patch for Octave-3.2.3":
            dbwhere = p_conn.dbwhere() if p_conn.dbstack()["frames"] else {}
            #dbwhere = p_conn.dbwhere()  # Puede hacer un beep!
            file_ = self.__file
            positions = []
            current = False

            if dbwhere and dbwhere["file"] == file_:
                pos = (dbwhere["line"], dbwhere["column"])

                if None not in pos:
                    positions.append(pos)
                    current = True

            data = Data()
            data.set_data("positions", positions)
            data.set_data("current", current)

            self.emit_("stack_update_request", data)
            return

        file_ = self.__file
        omit = self.__omit
        omit = str(omit) if omit else ""
        dbstack = p_conn.dbstack(omit)

        positions = []
        frames = dbstack["frames"]
        current = bool(frames and frames[0]["file"] == file_)
        for frame in frames:
            if frame["file"] == file_:
                positions.append((frame["line"], frame["column"]))

        data = Data()
        data.set_data("positions", positions)
        data.set_data("current", current)

        self.emit_("stack_update_request", data)
