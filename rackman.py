#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk

class Master:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.window = gtk.Window(gtk.WINDOW_POPUP)
        #self.window.set_border_width(10)
        self.window.set_opacity(0.5)
        #self.window.set_decorated(False)
        #self.window.connect("check-resize", self.resize_window)
        self.window.connect("destroy", lambda w: gtk.main_quit())

        #self.button = gtk.Button("Hello World")
        #self.button.connect("clicked", self.hello, None)
        #self.window.add(self.button)
        #self.button.show()

        self.window.show()

    def hello(self, widget, data=None):
        print "Hello World"

    #def resize_window(self, widget):
        #print self.window.get_size()




class Slave:
    def __init__(self, parent):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DND)
        #self.window = gtk.Dialog("My dialog",
                     #parent.window,
                     #gtk.DIALOG_DESTROY_WITH_PARENT,
        #)
        self.window.set_decorated(False)
        #self.window.set_has_frame(True)
        #self.window.set_frame_dimensions(1, 5, 1, 1)
        self.window.set_resizable(True)
        self.window.set_opacity(0.5)
        #self.window.set_size(400, 300)

        #self.window.connect("destroy", lambda w: gtk.main_quit())

        self.area = gtk.DrawingArea()
        self.area.set_size_request(200, 200)

        self.window.add(self.area)

        #self.area.set_events(gtk.gdk.POINTER_MOTION_MASK |
                            #gtk.gdk.POINTER_MOTION_HINT_MASK )
        self.area.connect("expose-event", self.draw)

        self.area.show()
        self.window.show()

        #self.window.begin_resize_drag(gtk.gdk.WINDOW_EDGE_EAST, 1, 10, 10, 1)

    def draw(self, area, event):
        #self.style = self.area.get_style()
        #self.gc = self.style.fg_gc[gtk.STATE_NORMAL]

        canvas = self.area.window

        self.gc_border = canvas.new_gc(
                    foreground=gtk.gdk.Color(red=0, green=65000, blue=65000),
                    #background=gtk.gdk.Color(green=65535),

                    #font=None,
                    #function=-1,
                    fill=1,
                    #tile=None,
                    #stipple=None,
                    #clip_mask=None,
                    #subwindow_mode=-1,
#
                    #ts_x_origin=-1,
                    #ts_y_origin=-1,
#
                    #clip_x_origin=-1,
                    #clip_y_origin=-1,
#
                    #graphics_exposures=-1,
#
                    line_width=3,
                    line_style=2,
#
                    #cap_style=-1,
                    #join_style=-1,
        )
        self.gc_diagonal = canvas.new_gc(
                    foreground=gtk.gdk.Color(red=0, green=65000, blue=65000),
                    #background=gtk.gdk.Color(green=65535),

                    #font=None,
                    #function=-1,
                    fill=1,
                    #tile=None,
                    #stipple=None,
                    #clip_mask=None,
                    #subwindow_mode=-1,
#
                    #ts_x_origin=-1,
                    #ts_y_origin=-1,
#
                    #clip_x_origin=-1,
                    #clip_y_origin=-1,
#
                    #graphics_exposures=-1,
#
                    line_width=1,
                    line_style=2,
#
                    #cap_style=-1,
                    #join_style=-1,
        )
        self.gc_center = canvas.new_gc(
                    foreground=gtk.gdk.Color(red=0, green=65000, blue=65000),
                    #background=gtk.gdk.Color(green=65535),

                    #font=None,
                    #function=-1,
                    fill=1,
                    #tile=None,
                    #stipple=None,
                    #clip_mask=None,
                    #subwindow_mode=-1,

                    #ts_x_origin=-1,
                    #ts_y_origin=-1,

                    #clip_x_origin=-1,
                    #clip_y_origin=-1,

                    #graphics_exposures=-1,

                    line_width=1,
                    line_style=1,

                    #cap_style=-1,
                    #join_style=-1,
        )

        #canvas.draw_line(self.gc, 10, 10, 20, 30)
        canvas.draw_rectangle(self.gc_border, False, 0,0, 199,199)

        canvas.draw_line(self.gc_diagonal, 0,0, 199,199)
        canvas.draw_line(self.gc_diagonal, 0,199, 199,0)

        return True



class Ruler:
    xpm_data = [
    "16 16 3 1",
    "       c None",
    ".      c #000000000000",
    "X      c #FFFFFFFFFFFF",
    "................",
    "..            ..",
    ". .          . .",
    ".  .        .  .",
    ".   .      .   .",
    ".    .    .    .",
    ".     .  .     .",
    ".      ..      .",
    ".      ..      .",
    ".     .  .     .",
    ".    .    .    .",
    ".   .      .   .",
    ".  .        .  .",
    ". .          . .",
    "..            ..",
    "................"
    ]

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_opacity(0.5)
        self.window.set_decorated(False)

        self.window.connect("check-resize", self.resize_window)

        #hruler = gtk.HRuler()
        #vruler = gtk.VRuler()
#
        #hruler.set_metric(gtk.PIXELS)
        #vruler.set_metric(gtk.PIXELS)

        self.window.show()

        pixmap, mask = gtk.gdk.pixmap_create_from_xpm_d(self.window.window,
                                                        None,
                                                        self.xpm_data)

        image = gtk.Image()
        image.set_from_pixmap(pixmap, mask)
        image.show()

        self.window.add(image)

    def resize_window(self, widget):
        print self.window.get_size()




def main():
    gtk.main()


if __name__ == "__main__":
    #ruler = Ruler()
    base = Master()
    #ruler.window.set_transient_for(base.window)

    Slave(base)

    #dialog = gtk.Dialog("My dialog",
                     #base.window,
                     #gtk.DIALOG_DESTROY_WITH_PARENT,
                     #)
    #dialog.set_decorated(False)
    #dialog.set_opacity(0.5)
    #dialog.show()
#
    #drawing_area = gtk.DrawingArea()
    #drawing_area.set_size_request(200, 200)
    #drawable = drawing_area.window
    #style = drawing_area.get_style()
    #gc = style.fg_gc[gtk.STATE_NORMAL]
    #drawable.draw_line(gc, 10, 10, 50, 50)

    main()
