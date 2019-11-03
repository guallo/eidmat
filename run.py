#!/usr/bin/env python

"""
    Script principal que carga y muestra la aplicacion.
"""

if __name__ == '__main__':
    import os
    import gtk

    # Creamos el splash.
    splash = gtk.Window(gtk.WINDOW_POPUP)
    splash.set_position(gtk.WIN_POS_CENTER)
    img = gtk.Image()
    img.set_from_file(os.path.abspath(os.path.join(__file__, os.pardir,
                                                   "images", "splash.png")))
    splash.add(img)
    splash.show_all()

    # Mostramos el splash.
    while gtk.events_pending():
        gtk.main_iteration()

    from mwindow.main_window import MainWindow

    gtk.gdk.threads_init()
    MainWindow()

    # Cerramos el splash.
    splash.destroy()

    gtk.main()
