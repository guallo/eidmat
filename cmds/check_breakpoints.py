import gobject

from cmds.command import Command
from util.data import Data


class CheckBreakpoints(Command):
    __gsignals__ = {"breakpoints_update_request": (gobject.SIGNAL_RUN_LAST,
                                                   gobject.TYPE_NONE,
                                                   (Data, ))
                   }

    def __init__(self, p_funcname, p_filename, p_file, p_prio=0):
        Command.__init__(self, p_prio)

        self.__funcname = p_funcname
        self.__filename = p_filename
        self.__file = p_file

    def execute(self, p_conn):
        # FIXME: re-implementar este metodo haciendo
        #        uso de 'p_conn.is_file_in_loadpath'

        funcname = self.__funcname

        if funcname[1]:
            real = "['%s', filemarker(), '%s']" %(funcname[0], funcname[1])
        else:
            real = "'%s'" %funcname[0]

        dbstatus = p_conn.dbstatus(real)
        lines = []

        if dbstatus:
            file_ = dbstatus[0]["file"]

            if (funcname[1] or file_):  # Esto es evitando funciones definidas
                                        # en el CommandWindow.
                if not file_:
                    file_ = p_conn.file_in_loadpath("'%s'" %self.__filename)

                if self.__file == file_:
                    lines = dbstatus[0]["lines"]

        data = Data()
        data.set_data("file", self.__file)
        data.set_data("function", funcname[1] if funcname[1] else funcname[0])
        data.set_data("lines", lines)

        self.emit_("breakpoints_update_request", data)
