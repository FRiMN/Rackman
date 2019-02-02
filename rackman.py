#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This software uses semantic versioning (SemVer v2.0.0).
# Copyright: (c) 2015-2018 by Nik Volkov.
# License: MIT, see LICENSE for more details.


import pygtk
pygtk.require('2.0')
import gtk
import cairo
import math
from string import Template
import os.path
import gettext
import time
import gobject
import glib


__version__ = '1.11.3'
app_name = 'rackman'

TV_RATIOS = {
        '1.25': '5:4',
        '1.33': '4:3',
        '1.50': '3:2',
        '1.56': '14:9',
        '1.60': '16:10',
        '1.78': '16:9',
    }


def set_translate():
    global _, COLORS

    if os.path.isfile('./locale/ru/LC_MESSAGES/{}.mo'.format(app_name)):
        trans_path = './locale'  # for local version
    else:
        trans_path = '/usr/share/locale'  # for system-wide version

    t = gettext.translation(app_name, trans_path)
    _ = t.ugettext
    COLORS = {
        _('Black'): {
            'rgb': (0, 0, 0),
            'key': 'K',
            'marker': 'Blac_k',
            'eng_name': 'Black',
        },
        _('White'): {
            'rgb': (1, 1, 1),
            'key': 'W',
            'marker': '_White',
            'eng_name': 'White',
        },
        _('Green'): {
            'rgb': (0, 1, 0),
            'key': 'G',
            'marker': '_Green',
            'eng_name': 'Green',
        },
        _('Blue'): {
            'rgb': (0, 0, 1),
            'key': 'B',
            'marker': '_Blue',
            'eng_name': 'Blue',
        },
        _('Red'): {
            'rgb': (1, 0, 0),
            'key': 'R',
            'marker': '_Red',
            'eng_name': 'Red',
        },
        _('Orange'): {
            'rgb': (1, 0.5, 0),
            'key': 'O',
            'marker': '_Orange',
            'eng_name': 'Orange',
        },
        _('Violet'): {
            'rgb': (0.5, 0, 0.5),
            'key': 'V',
            'marker': '_Violet',
            'eng_name': 'Violet',
        },
        _('Pink'): {
            'rgb': (1, 0.5, 1),
            'key': 'P',
            'marker': '_Pink',
            'eng_name': 'Pink',
        },
    }


def set_config():
    global config

    config = {}
    conf_file_name = "rackman.conf"
    conf_path_curdir = os.path.join('./', conf_file_name)
    conf_path_share = os.path.join('/usr/share/rackman/', conf_file_name)
    conf_path_home = os.path.join(os.path.expanduser('~'), '.config/rackman/', conf_file_name)
    conf_paths = (conf_path_share, conf_path_home, conf_path_curdir)
    for conf_path in conf_paths:
        if os.path.isfile(conf_path):
            print("Read config {}".format(conf_path))
            execfile(conf_path, config)  # чтение предустановок из файла конфигурации


def set_icon():
    global icon

    icon_file_name = 'rackman.svg'
    icon_path_curdir = os.path.join('./', icon_file_name)
    icon_path_share = os.path.join('/usr/share/icons/hicolor/scalable/apps/', icon_file_name)
    if os.path.isfile(icon_path_curdir):
        icon_path = icon_path_curdir
    else:
        icon_path = icon_path_share

    icon = gtk.gdk.pixbuf_new_from_file(icon_path)


class Key:
    up = 111
    down = 116
    left = 113
    right = 114


class Screenshot:
    def __init__(self, parent, slave):
        self.parent = parent
        self.slave = slave

        self.img_width = 100
        self.img_height = 100

        self.zoom = 2
        self.grab_rate = 15

    def build_window(self):
        self.image = gtk.Image()
        self.image.show()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Rackman magnifier')
        self.window.set_icon(icon)
        self.window.set_resizable(False)
        self.window.set_keep_above(config['slave_above'])
        self.window.add(self.image)
        self.window.connect("destroy", self.destroy_window)
        self.grab_timeout = None
        self.window.resize(200, 200)
        self.window.show()

    def destroy_window(self, w):
        self.window.destroy()
        del self.window

    def set_timeout(self):
        """ Set timer for magnifier grabbing """
        if hasattr(self, 'window') and self.grab_timeout == None:
            self.grab_timeout = glib.timeout_add(1000 / self.grab_rate, self.take)
            self.window.show()

    def take(self):
        """ Magnifier grab image """
        if hasattr(self, 'window'):
            _x, _y = self.slave.window.get_position()
            _width, _height = self.slave.window.get_size()

            x = _x - 25
            y = _y - 25
            width = _width + 50
            height = _height + 50

            pxbf = gtk.gdk.Pixbuf(
                gtk.gdk.COLORSPACE_RGB,
                False,
                8,
                width,
                height
            )

            pxbf.get_from_drawable(
                gtk.gdk.get_default_root_window(),
                gtk.gdk.colormap_get_system(),
                x, y, 0, 0,
                width,
                height
            )

            pxbf_scaled = pxbf.scale_simple(
                width * self.zoom,
                height * self.zoom,
                gtk.gdk.INTERP_BILINEAR
            )

            self.image.set_from_pixbuf(pxbf_scaled)
            # self.window.resize(width, height)

            self.grab_timeout = None
            self.set_timeout()
        return False


class Master:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_opacity(1)
        self.window.set_resizable(False)
        self.window.set_title( config['master_title'] )
        self.window.set_icon(icon)
        self.window.set_keep_above( config['master_above'] )
        self.window.connect("destroy", lambda w: gtk.main_quit())

        tableH = gtk.Table(rows=5, columns=4, homogeneous=False)
        self.window.add(tableH)
        tableH.set_col_spacings(2)
        tableH.show()

        menu_row = 0,1
        label_row = 1,2
        value_row = 2,3
        sub_label_row = 3,4
        sub_value_row = 4,5


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


        self.lpr = lpr = gtk.Label( _('Percents (W x H / D)') )
        lpr.show()
        tableH.attach(lpr, 0,3, *sub_label_row)

        self.vpr = vpr = gtk.Entry()
        vpr.set_editable(False)
        vpr.set_width_chars(25)
        vpr.show()
        tableH.attach(vpr, 0,3, *sub_value_row)


        self.lar = lar = gtk.Label( _('Aspect ratio') )
        lar.show()
        tableH.attach(lar, 3,4, *sub_label_row)

        self.var = var = gtk.Entry()
        var.set_editable(False)
        var.set_width_chars(8)
        var.show()
        tableH.attach(var, 3,4, *sub_value_row)

        menubar = self.get_main_menu()
        tableH.attach(menubar, 0,4, *menu_row)
        menubar.show()

        self.ev = gtk.gdk.Event(gtk.gdk.EXPOSE)

        self.window.show()

    @property
    def menu_items(self):
        if not hasattr(self, '__cached_menu_items'):
            self.__cached_menu_items = self.generate_menu()

        return self.__cached_menu_items

    def generate_menu(self):
        items = []

        self.generate_menu_backgrounds(items)
        self.generate_menu_foregrounds(items)
        self.generate_menu_opacity(items)
        self.generate_menu_metrics(items)
        self.generate_menu_tools(items)

        return items

    def generate_menu_tools(self, items):
        t = _('_Tools')

        items.append(('/{}'.format(t), None, None, 0, '<Branch>'))
        items.append(('/{}/{}'.format(t, _('Rotate')), '<ctrl>R', self.size_change, 1, '<Item>'))
        items.append(('/{}/{}'.format(t, _('Fix 100%')), '<ctrl>F', self.fix_percent, 2, '<Item>'))
        items.append(('/{}/{}'.format(t, _('Magnifier')), '<ctrl>M', self.toggle_magnifier, 3, '<Item>'))
        items.append(('/{}/{}'.format(t, _('Help')), '<ctrl>H', self.open_help, 4, '<Item>'))

    def generate_menu_metrics(self, items):
        m = _('_Metric')
        m_ = _('Metric')
        link = '/{}/px'.format(m_)
        mc = self.metric_change

        items.append(('/{}'.format(m), None, None, 0, '<Branch>'))
        items.append(('/{}/p_x'.format(m), None, mc, 1, '<RadioItem>'))
        items.append(('/{}/_mm'.format(m), None, mc, 2, link))
        items.append(('/{}/_in'.format(m), None, mc, 3, link))
        items.append(('/{}/_pt (Adobe)'.format(m), None, mc, 4, link))

    def generate_menu_opacity(self, items):
        o = _('_Opacity')
        o_ = _('Opacity')
        oc = self.opacity_change
        opacity_value = int(config['slave_opacity'] * 100)
        link = '/{}/{}'.format(o_, opacity_value)

        items.append(('/{}'.format(o), None, None, 0, '<Branch>'))
        opacitys = range(10, 101, 10)
        for i in opacitys:
            if i == opacity_value:
                key = '<ctrl>{}'.format(str(i)[-2])
                items.append(('/{}/_{}'.format(o, i), key, oc, i, '<RadioItem>'))
        for i in opacitys:
            if i != opacity_value:
                key = '<ctrl>{}'.format(str(i)[-2])
                if i == 100:
                    mark = '/{}/10_0'.format(o)
                else:
                    mark = '/{}/_{}'.format(o, i)
                items.append((mark, key, oc, i, link))

    def generate_menu_foregrounds(self, items):
        f = _('_Foreground')
        f_ = _('Foreground')
        cc = self.color_change
        color = config['foreground_color']
        link = '/{}/{}'.format(f_, _(color))

        items.append(('/{}'.format(f), None, None, 0, '<Branch>'))
        for i in COLORS:
            C = COLORS[i]
            if C['eng_name'] == color:
                key = '<ctrl><shift>{}'.format(C['key'])
                items.append(('/{}/{}'.format(f, _(C['marker'])), key, cc, 1, '<RadioItem>'))
        for i in COLORS:
            C = COLORS[i]
            if C['eng_name'] is not color:
                key = '<ctrl><shift>{}'.format(C['key'])
                items.append(('/{}/{}'.format(f, _(C['marker'])), key, cc, 2, link))

    def generate_menu_backgrounds(self, items):
        b = _('_Background')
        b_ = _('Background')
        cc = self.color_change
        color = config['background_color']
        link = '/{}/{}'.format(b_, _(color))

        items.append(('/{}'.format(b), None, None, 0, '<Branch>'))
        for i in COLORS:
            C = COLORS[i]
            if C['eng_name'] == color:
                key = '<alt><shift>{}'.format(C['key'])
                items.append(('/{}/{}'.format(b, _(C['marker'])), key, cc, 1, '<RadioItem>'))
        for i in COLORS:
            C = COLORS[i]
            if C['eng_name'] is not color:
                key = '<alt><shift>{}'.format(C['key'])
                items.append(('/{}/{}'.format(b, _(C['marker'])), key, cc, 2, link))

    def toggle_magnifier(self, ret, widget):
        if hasattr(screenshot, 'window'):
            screenshot.window.destroy()
        else:
            screenshot.build_window()
            screenshot.set_timeout()

    def open_help(self, ret, widget):
        import webbrowser
        urls = (
            os.path.realpath('./doc/html/ru/index.html'),
            '/usr/share/doc/rackman/html/ru/index.html',
        )
        for url in urls:
            print('Try open {}'.format(url))
            if os.path.isfile(url):
                print('\t ...open in webbrowser')
                webbrowser.open(url)
                break

    def color_change(self, ret, widget):
        color_name = widget.name.split('/')[-1]
        color_context = widget.name.split('/')[-2]
        rgb = COLORS[ _(color_name) ]['rgb']

        if color_context == _('Background'):
            slave.background = rgb
        elif color_context == _('Foreground'):
            slave.foreground = rgb
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

        item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
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

    def fix_percent(self, ret, widget):
        w, h = slave.window.get_size()
        slave.percent_full = (w, h)
        slave.window.emit("check-resize")   # обновление показателей


class Slave():
    def __init__(self, parent):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_decorated(False)
        self.window.set_title(config['slave_title'])
        self.window.set_icon(icon)
        self.window.set_resizable(True)
        self.window.set_keep_above(config['slave_above'])
        if config['transient'] == True:
            self.window.set_transient_for(parent.window)
        else:
            self.window.set_transient_for(None)
        self.window.set_opacity(config['slave_opacity'])

        self.parent = parent
        self.metric = ('px', 1, 0, 2)

        w, h = self.window.get_size()
        self.percent_full = (w, h)

        self.area = gtk.DrawingArea()

        self.background = COLORS[ _( config['background_color'] ) ]['rgb']
        self.foreground = COLORS[ _( config['foreground_color'] ) ]['rgb']

        self.window.add(self.area)

        self.area.show()
        self.window.show()

        self.window.connect("check_resize", self.resize_window)
        self.window.connect("key_press_event", self.resizing)
        self.area.connect("expose_event", self.draw_cairo)

    def resizing(self, widget, event):
        x, y = widget.get_size()
        ox, oy = widget.get_position()
        keycode = event.hardware_keycode

        acc = 1
        if event.state & gtk.gdk.SHIFT_MASK:
            acc = config['fast_mode_speed']

        # TODO: Объединить
        if event.state & gtk.gdk.CONTROL_MASK:
            if keycode == Key.right:
                ox += acc
            elif keycode == Key.down:
                oy += acc
            elif keycode == Key.left:
                ox -= acc
            elif keycode == Key.up:
                oy -= acc
        elif event.state & gtk.gdk.MOD1_MASK:   # ~ alt
            if keycode == Key.right:
                ox -= acc
                x += acc*2
            elif keycode == Key.down:
                oy -= acc
                y += acc*2
            elif keycode == Key.left:
                if x > acc*2:
                    ox += acc
                    x -= acc*2
            elif keycode == Key.up:
                if y > acc*2:
                    oy += acc
                    y -= acc*2
        else:
            if keycode == Key.right:
                x += acc
            elif keycode == Key.down:
                y += acc
            elif keycode == Key.left:
                x -= acc
            elif keycode == Key.up:
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

        percent_w = ( w * 100.0 / self.percent_full[0] )
        percent_h = ( h * 100.0 / self.percent_full[1] )
        percent_d = ( gipo * 100.0 / ( math.sqrt(self.percent_full[0]*self.percent_full[0] + self.percent_full[1]*self.percent_full[1]) ) )

        if w >= h:
            ratio = float(w) / h
        else:
            ratio = float(h) / w

        r = str( round(ratio, 3) )
        if r in TV_RATIOS.keys():
            ratio_tv = '({})'.format(TV_RATIOS[r])
        else:
            ratio_tv = ''

        T = Template('{:.${precision}f}{:s}')
        norm = T.substitute(precision=precision_norm)
        high = T.substitute(precision=precision_high)

        self.parent.vw.set_text( norm.format( round(w       * metric_mod, precision_norm), metric_name.split()[0] ) )
        self.parent.vh.set_text( norm.format( round(h       * metric_mod, precision_norm), metric_name.split()[0] ) )
        self.parent.vd.set_text( high.format( round(gipo    * metric_mod, precision_high), metric_name.split()[0] ) )
        self.parent.va.set_text( '{:.1f}° / {:.1f}°'.format( round(grad1,1), round(grad2,1) ) )

        self.parent.vpr.set_text( '{:.2f}% x {:.2f}% / {:.2f}%'.format( percent_w, percent_h, percent_d ) )
        self.parent.var.set_text( '{:.3f}:1 {:s}'.format( ratio, ratio_tv ) )

        return True

    def get_monitor(self):
        window = gtk.Window()
        screen = window.get_screen()
        gdk_win = gtk.Widget.get_window(self.window)   # получаем gdk.Window из gtk.Window
        curmon = screen.get_monitor_at_window(gdk_win)

        _px = screen.get_monitor_geometry(curmon)[2]
        _mm = screen.get_monitor_width_mm(curmon)

        dpm = float(_px) / float(_mm)
        return dpm

    def draw_cairo(self, area, event):
        """ Отрисовывает измерительные метки в окне измерителя """
        self.context = area.window.cairo_create()
        self.ea = event.area

        self.draw_background(event)
        self.context.set_source_rgb(*self.foreground)    # foreground
        self.draw_border(event)
        self.draw_diagonals(event)
        self.draw_verticals(event)

        return True

    def draw_verticals(self, event):
        self.context.set_line_width(1)
        self.context.set_dash([3, 3])
        self.context.move_to(event.area.width / 2.0, 0)
        self.context.line_to(event.area.width / 2.0, event.area.height)
        self.context.stroke()
        self.context.move_to(0, event.area.height / 2.0)
        self.context.line_to(event.area.width, event.area.height / 2.0)
        self.context.stroke()

    def draw_diagonals(self, event):
        self.context.set_line_width(1)
        self.context.move_to(0, 0)
        self.context.line_to(event.area.width, event.area.height)
        self.context.stroke()
        self.context.move_to(event.area.width, 0)
        self.context.line_to(0, event.area.height)
        self.context.stroke()

    def draw_border(self, event):
        self.context.set_line_width(1)
        self.context.rectangle(1, 1, event.area.width - 2, event.area.height - 2)
        self.context.stroke()

    def draw_background(self, event):
        self.context.set_source_rgb(*self.background)
        self.context.rectangle(0, 0, event.area.width, event.area.height)
        self.context.fill()
        self.context.stroke()


if __name__ == "__main__":
    print("Rackman ver. {}".format(__version__))

    set_config()
    set_translate()
    set_icon()

    global base, slave, screenshot
    base = Master()
    slave = Slave(base)
    screenshot = Screenshot(base, slave)

    slave.window.emit("check-resize")
    gtk.main()
