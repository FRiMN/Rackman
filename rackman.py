#!/usr/bin/python
# -*- coding: utf-8 -*-

# This software uses semantic versioning (SemVer v2.0.0).
# Copyright: (c) 2015 by Nik Volkov.
# License: MIT, see LICENSE for more details.


#import pygtk
#pygtk.require('2.0')
import gtk
import cairo
import math
from string import Template
import os.path
import gettext



VERSION = '1.6.8'



def initial():
    global window, screen, _, COLORS, icon

    window = gtk.Window()
    screen = window.get_screen()



    app_name = 'rackman'

    if os.path.isfile( './locale/ru/LC_MESSAGES/{}.mo'.format(app_name) ):
        trans_path = './locale'
    else:
        trans_path = '/usr/share/locale'

    t = gettext.translation(app_name, trans_path)
    _ = t.ugettext



    COLORS = {
                    _('Black'):        (0, 0, 0),
                    _('White'):        (1, 1, 1),
                    _('Green'):        (0, 1, 0),
                    _('Blue'):         (0, 0, 1),
                    _('Red'):          (1, 0, 0),
                    _('Orange'):       (1, 0.5, 0),
                    _('Violet'):       (0.5, 0, 0.5),
                    _('Pink'):         (1, 0.5, 1),
    }



    icon_file_name = 'rackman.svg'
    icon_path_curdir = os.path.join('./', icon_file_name)
    icon_path_share = os.path.join('/usr/share/icons/hicolor/scalable/apps/', icon_file_name)

    if os.path.isfile( icon_path_curdir ):
        icon_path = icon_path_curdir
    else:
        icon_path = icon_path_share

    icon = gtk.gdk.pixbuf_new_from_file(icon_path)



class Master:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_opacity(1)
        self.window.set_resizable(False)
        self.window.set_title("Rackman [Master]")
        self.window.set_icon(icon)
        self.window.connect("destroy", lambda w: gtk.main_quit())


        tableH = gtk.Table(rows=3, columns=4, homogeneous=False)
        self.window.add(tableH)
        tableH.set_col_spacings(2)
        tableH.show()

        menu_row = 0,1
        label_row = 1,2
        value_row = 2,3


        self.lw = lw = gtk.Label( _('Width') )
        lw.show()
        tableH.attach(lw, 0,1, *label_row)

        self.vw = vw = gtk.Entry()
        vw.set_editable(False)
        vw.set_width_chars(8)
        vw.show()
        tableH.attach(vw, 0,1, *value_row)


        self.lh = lh = gtk.Label( _('Height') )
        lh.show()
        tableH.attach(lh, 1,2, *label_row)

        self.vh = vh = gtk.Entry()
        vh.set_editable(False)
        vh.set_width_chars(8)
        vh.show()
        tableH.attach(vh, 1,2, *value_row)


        self.ld = ld = gtk.Label( _('Diagonal') )
        ld.show()
        tableH.attach(ld, 2,3, *label_row)

        self.vd = vd = gtk.Entry()
        vd.set_editable(False)
        vd.set_width_chars(9)
        vd.show()
        tableH.attach(vd, 2,3, *value_row)


        self.la = la = gtk.Label( _('Angles (Goriz / Vert)') )
        la.show()
        tableH.attach(la, 3,4, *label_row)

        self.va = va = gtk.Entry()
        va.set_editable(False)
        va.set_width_chars(11)
        va.show()
        tableH.attach(va, 3,4, *value_row)


        self.menu_items = (
                    ('/{}'.format(    _('_Background') ),               None,               None,                   0,  '<Branch>'),
                    ('/{}/{}'.format( _('Background'), _('_White') ),   '<alt><shift>W',    self.color_change,      1,  '<RadioItem>'),
                    ('/{}/{}'.format( _('Background'), _('Blac_k') ),   '<alt><shift>K',    self.color_change,      2,  '/{}/{}'.format( _('Background'), _('White') )),
                    ('/{}/{}'.format( _('Background'), _('_Green') ),   '<alt><shift>G',    self.color_change,      3,  '/{}/{}'.format( _('Background'), _('White') )),
                    ('/{}/{}'.format( _('Background'), _('_Blue') ),    '<alt><shift>B',    self.color_change,      4,  '/{}/{}'.format( _('Background'), _('White') )),
                    ('/{}/{}'.format( _('Background'), _('_Red') ),     '<alt><shift>R',    self.color_change,      5,  '/{}/{}'.format( _('Background'), _('White') )),
                    ('/{}/{}'.format( _('Background'), _('_Orange') ),  '<alt><shift>O',    self.color_change,      6,  '/{}/{}'.format( _('Background'), _('White') )),
                    ('/{}/{}'.format( _('Background'), _('_Violet') ),  '<alt><shift>V',    self.color_change,      7,  '/{}/{}'.format( _('Background'), _('White') )),
                    ('/{}/{}'.format( _('Background'), _('_Pink') ),    '<alt><shift>P',    self.color_change,      8,  '/{}/{}'.format( _('Background'), _('White') )),

                    ('/{}'.format(    _('_Foreground') ),               None,               None,                   0,  '<Branch>'),
                    ('/{}/{}'.format( _('Foreground'), _('_Red') ),     '<ctrl><shift>R',   self.color_change,      5,  '<RadioItem>'),
                    ('/{}/{}'.format( _('Foreground'), _('_White') ),   '<ctrl><shift>W',   self.color_change,      1,  '/{}/{}'.format( _('Foreground'), _('Red') )),
                    ('/{}/{}'.format( _('Foreground'), _('Blac_k') ),   '<ctrl><shift>K',   self.color_change,      2,  '/{}/{}'.format( _('Foreground'), _('Red') )),
                    ('/{}/{}'.format( _('Foreground'), _('_Green') ),   '<ctrl><shift>G',   self.color_change,      3,  '/{}/{}'.format( _('Foreground'), _('Red') )),
                    ('/{}/{}'.format( _('Foreground'), _('_Blue') ),    '<ctrl><shift>B',   self.color_change,      4,  '/{}/{}'.format( _('Foreground'), _('Red') )),
                    ('/{}/{}'.format( _('Foreground'), _('_Orange') ),  '<ctrl><shift>O',   self.color_change,      6,  '/{}/{}'.format( _('Foreground'), _('Red') )),
                    ('/{}/{}'.format( _('Foreground'), _('_Violet') ),  '<ctrl><shift>V',   self.color_change,      7,  '/{}/{}'.format( _('Foreground'), _('Red') )),
                    ('/{}/{}'.format( _('Foreground'), _('_Pink') ),    '<ctrl><shift>P',   self.color_change,      8,  '/{}/{}'.format( _('Foreground'), _('Red') )),

                    ('/{}'.format(    _('_Opacity') ),                  None,               None,                   0,  '<Branch>'),
                    ('/{}/_50'.format( _('Opacity') ),                  '<ctrl>5',          self.opacity_change,    50, '<RadioItem>'),
                    ('/{}/_10'.format( _('Opacity') ),                  '<ctrl>1',          self.opacity_change,    10, '/{}/50'.format( _('Opacity') )),
                    ('/{}/_20'.format( _('Opacity') ),                  '<ctrl>2',          self.opacity_change,    20, '/{}/50'.format( _('Opacity') )),
                    ('/{}/_30'.format( _('Opacity') ),                  '<ctrl>3',          self.opacity_change,    30, '/{}/50'.format( _('Opacity') )),
                    ('/{}/_40'.format( _('Opacity') ),                  '<ctrl>4',          self.opacity_change,    40, '/{}/50'.format( _('Opacity') )),
                    ('/{}/_60'.format( _('Opacity') ),                  '<ctrl>6',          self.opacity_change,    60, '/{}/50'.format( _('Opacity') )),
                    ('/{}/_70'.format( _('Opacity') ),                  '<ctrl>7',          self.opacity_change,    70, '/{}/50'.format( _('Opacity') )),
                    ('/{}/_80'.format( _('Opacity') ),                  '<ctrl>8',          self.opacity_change,    80, '/{}/50'.format( _('Opacity') )),
                    ('/{}/_90'.format( _('Opacity') ),                  '<ctrl>9',          self.opacity_change,    90, '/{}/50'.format( _('Opacity') )),
                    ('/{}/10_0'.format( _('Opacity') ),                 '<ctrl>0',          self.opacity_change,    100,'/{}/50'.format( _('Opacity') )),

                    ('/{}'.format(   _('_Metric') ),                    None,               None,                   0,  '<Branch>'),
                    ('/{}/p_x'.format(_('Metric') ),                    None,               self.metric_change,     1,  '<RadioItem>'),
                    ('/{}/_mm'.format(_('Metric') ),                    None,               self.metric_change,     2,  '/{}/px'.format( _('Metric') )),
                    ('/{}/_in'.format(_('Metric') ),                    None,               self.metric_change,     3,  '/{}/px'.format( _('Metric') )),
                    ('/{}/_pt (Adobe)'.format( _('Metric') ),           None,               self.metric_change,     4,  '/{}/px'.format( _('Metric') )),

                    ('/{}'.format(    _('_Tools') ),                    None,               None,                   0,  '<Branch>'),
                    ('/{}/{}'.format( _('Tools'), _('Rotate') ),        '<ctrl>R',          self.size_change,       1,  '<Item>'),
        )

        menubar = self.get_main_menu()
        tableH.attach(menubar, 0,4, *menu_row)
        menubar.show()

        self.ev = gtk.gdk.Event(gtk.gdk.EXPOSE)


        self.window.show()


    def color_change(self, ret, widget):
        color_name = widget.name.split('/')[-1]
        color_context = widget.name.split('/')[-2]

        if color_context == _('Background'):
            slave.background = COLORS[ _(color_name) ]
        elif color_context == _('Foreground'):
            slave.foreground = COLORS[ _(color_name) ]
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


    def metric_change(self, ret, widget):
        metric_name = widget.name.split('/')[-1].lower()

        slave.metric = list(slave.metric)
        slave.metric[0] = metric_name
        slave.metric = tuple(slave.metric)
        slave.window.emit("check-resize")   # обновление показателей


    def size_change(self, ret, widget):
        w, h = slave.window.get_size()
        slave.window.resize(h, w)



class Slave:
    def __init__(self, parent):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_decorated(False)
        self.window.set_title("Rackman [Slave]")
        self.window.set_icon(icon)
        self.window.set_resizable(True)
        self.window.set_keep_above(True)
        #self.window.set_transient_for(parent.window)
        self.window.set_opacity(0.5)

        self.parent = parent
        self.metric = ('px', 1, 0, 2)

        self.area = gtk.DrawingArea()

        self.background = COLORS[ _('White') ]
        self.foreground = COLORS[ _('Red') ]

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
        
        acc = 1
        if event.state & gtk.gdk.SHIFT_MASK:
            acc = 50

        if event.state & gtk.gdk.CONTROL_MASK:
            if event.hardware_keycode == 114:   # right
                ox += acc
            elif event.hardware_keycode == 116: # down
                oy += acc
            elif event.hardware_keycode == 113: # left
                ox -= acc
            elif event.hardware_keycode == 111: # up
                oy -= acc
        else:
            if event.hardware_keycode == 114:   # right
                x += acc
            elif event.hardware_keycode == 116: # down
                y += acc
            elif event.hardware_keycode == 113: # left
                x -= acc
            elif event.hardware_keycode == 111: # up
                y -= acc

        self.window.move(ox, oy)
        self.window.resize(x, y)

        return True


    def resize_window(self, widget):
        dpm = self.get_monitor()
        w, h = self.window.get_size()
        metric_name = self.metric[0]

        if metric_name == 'px':
            metric_mod = 1
            precision_norm = 0
            precision_high = 2
        elif metric_name == 'mm':
            metric_mod = 1.0 / dpm
            precision_norm = 2
            precision_high = 2
        elif metric_name == 'in':
            metric_mod = 1.0 / dpm / 25.4
            precision_norm = 3
            precision_high = 3
        elif metric_name == 'pt (adobe)':
            metric_mod = 1.0 / dpm / 0.352777
            precision_norm = 1
            precision_high = 1
        else:
            raise ValueError( "Unknown metric: {}".format(metric_name) )

        self.metric = (metric_name, metric_mod, precision_norm, precision_high)

        gipo = math.sqrt(h*h + w*w)     # гипотенуза

        grad1 = math.degrees( math.asin( h / gipo ) )
        grad2 = 90 - grad1

        T = Template('{:.${precision}f}{:s}')
        norm = T.substitute(precision=precision_norm)
        high = T.substitute(precision=precision_high)

        self.parent.vw.set_text( norm.format( round(w       * metric_mod, precision_norm), metric_name.split()[0] ) )
        self.parent.vh.set_text( norm.format( round(h       * metric_mod, precision_norm), metric_name.split()[0] ) )
        self.parent.vd.set_text( high.format( round(gipo    * metric_mod, precision_high), metric_name.split()[0] ) )
        self.parent.va.set_text( '{:.1f}° / {:.1f}°'.format( round(grad1,1), round(grad2,1) ) )

        return True


    def get_monitor(self):
        gdk_win = gtk.Widget.get_window(self.window)   # получаем gdk.Window из gtk.Window
        curmon = screen.get_monitor_at_window(gdk_win)

        _px = screen.get_monitor_geometry(curmon)[2]
        _mm = screen.get_monitor_width_mm(curmon)

        dpm = float(_px) / float(_mm)

        return dpm


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

    initial()

    base = Master()
    slave = Slave(base)
    slave.window.emit("check-resize")

    gtk.main()
