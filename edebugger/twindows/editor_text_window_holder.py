class EditorTextWindowHolder:
    def __init__(self):
        self.__windows = []

    def append(self, p_window, p_controller):
        name = p_window.get_name()

        if self.exist_window_of_name(name):
            raise Exception("Already exist window named '%s'" %name)

        prio = p_window.get_pos()
        windows = self.__windows

        for pos in xrange(len(windows)):
            win, ctrl = windows[pos]
            if prio < win.get_pos():
                windows.insert(pos, (p_window, p_controller))
                return

        windows.append((p_window, p_controller))

    def remove(self, p_window):
        windows = self.__windows

        for pos in xrange(len(windows)):
            if windows[pos][0] == p_window:
                del windows[pos]
                return

        raise Exception("The window %s not exist" %p_window)

    def get_windows_of_type(self, p_type):
        return [t for t in self.__windows if t[0].get_type() == p_type]

    def get_window_of_name(self, p_name):
        for t in self.__windows:
            if t[0].get_name() == p_name:
                return t

        raise Exception("There is not window with name '%s'" %p_name)

    def exist_window_of_name(self, p_name):
        for win, ctrl in self.__windows:
            if win.get_name() == p_name:
                return True

        return False

    def __iter__(self):
        for t in self.__windows:
            yield t
