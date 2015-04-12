#!/usr/bin/python
# -*- coding: utf-8 -*-

# See license in the file LICENSE.
# This software uses semantic versioning (SemVer v2.0.0).


#import pygtk
#pygtk.require('2.0')
import gtk
import cairo
import math


VERSION = '1.4.0'

COLORS = {
                'black':        (0, 0, 0),
                'white':        (1, 1, 1),
                'green':        (0, 1, 0),
                'blue':         (0, 0, 1),
                'red':          (1, 0, 0),
                'orange':       (1, 0.5, 0),
                'violet':       (0.5, 0, 0.5),
                'pink':         (1, 0.5, 1),
}


class Master:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_opacity(1)
        self.window.set_resizable(False)
        self.window.set_title("Rackman [Master]")
        self.window.connect("destroy", lambda w: gtk.main_quit())


        tableH = gtk.Table(rows=3, columns=4, homogeneous=False)
        self.window.add(tableH)
        tableH.set_col_spacings(2)
        tableH.show()

        menu_row = 0,1
        label_row = 1,2
        value_row = 2,3


        self.lw = lw = gtk.Label('Ширина')
        lw.show()
        tableH.attach(lw, 0,1, *label_row)

        self.vw = vw = gtk.Entry()
        vw.set_editable(False)
        vw.set_width_chars(6)
        vw.show()
        tableH.attach(vw, 0,1, *value_row)


        self.lh = lh = gtk.Label('Высота')
        lh.show()
        tableH.attach(lh, 1,2, *label_row)

        self.vh = vh = gtk.Entry()
        vh.set_editable(False)
        vh.set_width_chars(6)
        vh.show()
        tableH.attach(vh, 1,2, *value_row)


        self.ld = ld = gtk.Label('Диагональ')
        ld.show()
        tableH.attach(ld, 2,3, *label_row)

        self.vd = vd = gtk.Entry()
        vd.set_editable(False)
        vd.set_width_chars(9)
        vd.show()
        tableH.attach(vd, 2,3, *value_row)


        self.la = la = gtk.Label('Углы (Г / В)')
        la.show()
        tableH.attach(la, 3,4, *label_row)

        self.va = va = gtk.Entry()
        va.set_editable(False)
        va.set_width_chars(11)
        va.show()
        tableH.attach(va, 3,4, *value_row)


        self.menu_items = (
                    ('/_Background',        None,               None,                   0,  '<Branch>'),
                    ('/Background/_White',  '<alt><shift>W',    self.color_change,      1,  '<RadioItem>'),
                    ('/Background/Blac_k',  '<alt><shift>K',    self.color_change,      2,  '/Background/White'),
                    ('/Background/_Green',  '<alt><shift>G',    self.color_change,      3,  '/Background/White'),
                    ('/Background/_Blue',   '<alt><shift>B',    self.color_change,      4,  '/Background/White'),
                    ('/Background/_Red',    '<alt><shift>R',    self.color_change,      5,  '/Background/White'),
                    ('/Background/_Orange', '<alt><shift>O',    self.color_change,      6,  '/Background/White'),
                    ('/Background/_Violet', '<alt><shift>V',    self.color_change,      7,  '/Background/White'),
                    ('/Background/_Pink',   '<alt><shift>P',    self.color_change,      8,  '/Background/White'),

                    ('/_Foreground',        None,               None,                   0,  '<Branch>'),
                    ('/Foreground/_Red',    '<ctrl><shift>R',   self.color_change,      5,  '<RadioItem>'),
                    ('/Foreground/_White',  '<ctrl><shift>W',   self.color_change,      1,  '/Foreground/Red'),
                    ('/Foreground/Blac_k',  '<ctrl><shift>K',   self.color_change,      2,  '/Foreground/Red'),
                    ('/Foreground/_Green',  '<ctrl><shift>G',   self.color_change,      3,  '/Foreground/Red'),
                    ('/Foreground/_Blue',   '<ctrl><shift>B',   self.color_change,      4,  '/Foreground/Red'),
                    ('/Foreground/_Orange', '<ctrl><shift>O',   self.color_change,      6,  '/Foreground/Red'),
                    ('/Foreground/_Violet', '<ctrl><shift>V',   self.color_change,      7,  '/Foreground/Red'),
                    ('/Foreground/_Pink',   '<ctrl><shift>P',   self.color_change,      8,  '/Foreground/Red'),

                    ('/_Opacity',           None,               None,                   0,  '<Branch>'),
                    ('/Opacity/_50',        '<ctrl>5',          self.opacity_change,    50, '<RadioItem>'),
                    ('/Opacity/_10',        '<ctrl>1',          self.opacity_change,    10, '/Opacity/50'),
                    ('/Opacity/_20',        '<ctrl>2',          self.opacity_change,    20, '/Opacity/50'),
                    ('/Opacity/_30',        '<ctrl>3',          self.opacity_change,    30, '/Opacity/50'),
                    ('/Opacity/_40',        '<ctrl>4',          self.opacity_change,    40, '/Opacity/50'),
                    ('/Opacity/_60',        '<ctrl>6',          self.opacity_change,    60, '/Opacity/50'),
                    ('/Opacity/_70',        '<ctrl>7',          self.opacity_change,    70, '/Opacity/50'),
                    ('/Opacity/_80',        '<ctrl>8',          self.opacity_change,    80, '/Opacity/50'),
                    ('/Opacity/_90',        '<ctrl>9',          self.opacity_change,    90, '/Opacity/50'),
                    ('/Opacity/10_0',       '<ctrl>0',          self.opacity_change,    100,'/Opacity/50'),
        )

        menubar = self.get_main_menu()
        tableH.attach(menubar, 0,4, *menu_row)
        menubar.show()

        self.ev = gtk.gdk.Event(gtk.gdk.EXPOSE)


        self.window.show()


    def color_change(self, ret, widget):
        color_name = widget.name.split('/')[-1].lower()
        color_context = widget.name.split('/')[-2].lower()

        if color_context == 'background':
            slave.background = COLORS[color_name]
        elif color_context == 'foreground':
            slave.foreground = COLORS[color_name]
        else:
            raise ValueError( "Unknown color_context: {}".format(color_context) )

        self.ev.area = slave.ea
        slave.area.emit("expose-event", self.ev)


    def opacity_change(self, ret, widget):
        try:
            if self.old_opacity != ret:
                slave.window.set_opacity(ret / 100.0)
                self.old_opacity = ret
        except AttributeError:
            self.old_opacity = ret


    def get_main_menu(self):
        accel_group = gtk.AccelGroup()

        self.item_factory = item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
        item_factory.create_items(self.menu_items)
        self.window.add_accel_group(accel_group)

        return item_factory.get_widget("<main>")



class Slave:
    def __init__(self, parent):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_decorated(False)
        self.window.set_title("Rackman [Slave]")
        self.window.set_resizable(True)
        self.window.set_keep_above(True)
        #self.window.set_transient_for(parent.window)
        self.window.set_opacity(0.5)

        self.parent = parent

        self.area = gtk.DrawingArea()
        self.background = COLORS['white']
        self.foreground = COLORS['red']

        self.window.add(self.area)

        self.area.show()
        self.window.show()


        self.window.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.window.add_events(gtk.gdk.BUTTON_PRESS_MASK)

        self.window.connect("check-resize", self.resize_window)
        self.window.connect("key-press-event", self.resizing)
        self.area.connect("expose-event", self.draw_cairo)


    def resizing(self, widget, event):
        x, y = widget.get_size()
        ox, oy = widget.get_position()

        if event.state & gtk.gdk.CONTROL_MASK:
            if event.hardware_keycode == 114:   # right
                ox += 1
            elif event.hardware_keycode == 116: # down
                oy += 1
            elif event.hardware_keycode == 113: # left
                ox -= 1
            elif event.hardware_keycode == 111: # up
                oy -= 1
        else:
            if event.hardware_keycode == 114:   # right
                x += 1
            elif event.hardware_keycode == 116: # down
                y += 1
            elif event.hardware_keycode == 113: # left
                x -= 1
            elif event.hardware_keycode == 111: # up
                y -= 1

        self.window.move(ox, oy)
        self.window.resize(x, y)

        return True


    def resize_window(self, widget):
        w, h = self.window.get_size()

        gipo = math.sqrt(h*h + w*w)     # гипотенуза

        grad1 = math.degrees( math.asin( h / gipo ) )
        grad2 = 90 - grad1

        self.parent.vw.set_text( '{:d}px'.format(w) )
        self.parent.vh.set_text( '{:d}px'.format(h) )
        self.parent.vd.set_text( '{:.2f}px'.format(gipo) )
        self.parent.va.set_text( '{:.1f}° / {:.1f}°'.format( round(grad1,2), round(grad2,2) ) )

        return True


    def draw_cairo(self, area, event):
        self.context = area.window.cairo_create()
        self.ea = event.area

        # background
        self.context.set_source_rgb(*self.background)

        self.context.rectangle(0, 0, event.area.width, event.area.height)
        self.context.fill()
        self.context.stroke()


        self.context.set_source_rgb(*self.foreground)    # foreground

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
    print "Rackman ver. {}".format(VERSION)

    base = Master()
    slave = Slave(base)

    gtk.main()
