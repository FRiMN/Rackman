#!/usr/bin/python

#import pygtk
#pygtk.require('2.0')
import gtk
import cairo



class Master:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.window = gtk.Window(gtk.WINDOW_POPUP)
        #self.window.set_border_width(10)
        self.window.set_opacity(1)
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
        self.window.set_decorated(False)
        #self.window.set_has_frame(True)
        self.window.set_resizable(True)
        self.window.set_opacity(0.5)
        #self.window.set_size(400, 300)

        self.area = gtk.DrawingArea()
        #self.area.set_size_request(200, 200)

        self.window.add(self.area)

        self.area.show()
        self.window.show()


        self.window.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.window.add_events(gtk.gdk.BUTTON_PRESS_MASK)

        self.window.connect("check-resize", self.resize_window)
        self.window.connect("key-press-event", self.resizing)
        self.area.connect("expose-event", self.draw_cairo)

        self.window.connect("button-press-event", self.begin_move)




        #self.window.begin_resize_drag(gtk.gdk.WINDOW_EDGE_EAST, 1, 10, 10, 1)
        #self.window.begin_resize_drag(gtk.gdk.WINDOW_EDGE_SOUTH, 1, 10, 10, 1)

        #self.window.begin_move_drag(2, 10, 10, 3000)
        #self.begin_move(self.window, None)


    def begin_move(self, widget, event):
        print 'begin move'
        print widget

        print 'Clicked at x={}, y={}'.format(event.x, event.y)

        x_root, y_root = widget.get_position()
        #event = gtk.get_current_event()
        widget.window.begin_move_drag(
                        2,
                        int(event.x), int(event.y),
                        #x_root, y_root,
                        #event.time
                        1000
        )

        print '--end move\n'

        return True


    def resizing(self, widget, event):
        print event.hardware_keycode

        x, y = widget.get_size()

        if event.hardware_keycode == 114:   # right
            x += 1
        elif event.hardware_keycode == 116: # down
            y += 1
        elif event.hardware_keycode == 113: # left
            x -= 1
        elif event.hardware_keycode == 111: # up
            y -= 1

        elif event.hardware_keycode == 37:  # Ctrl
            self.begin_move(self.window, event)

        self.area.window.resize(x, y)
        self.window.resize(x, y)

        return True


    def resize_window(self, widget):
        #print self.window.get_size()
        #self.draw_cairo(self.area)

        return True


    def draw_cairo(self, area, event):
        self.context = area.window.cairo_create()

        #self.context.clip()

        # background
        self.context.set_source_rgb(0, 1, 0)

        self.context.rectangle(0, 0, event.area.width, event.area.height)
        self.context.fill()
        self.context.stroke()


        self.context.set_source_rgb(0, 0, 1)    # foreground

        # border
        self.context.set_line_width(1)

        self.context.rectangle(1, 1, event.area.width-2, event.area.height-2)
        self.context.stroke()

        # diagonals
        self.context.set_line_width(1)

        self.context.move_to(0, 0)
        self.context.line_to(event.area.width, event.area.height)
        self.context.stroke()

        self.context.move_to(event.area.width, 0)
        self.context.line_to(0, event.area.height)
        self.context.stroke()

        # verticals
        self.context.set_line_width(1)
        self.context.set_dash([3,3])

        self.context.move_to(event.area.width/2.0, 0)
        self.context.line_to(event.area.width/2.0, event.area.height)
        self.context.stroke()

        self.context.move_to(0, event.area.height/2.0)
        self.context.line_to(event.area.width, event.area.height/2.0)
        self.context.stroke()

        return False


if __name__ == "__main__":
    base = Master()
    Slave(base)

    gtk.main()
