#!/usr/bin/env python

from distutils.core import setup
from glob import glob
from rackman import VERSION

setup(name          =   'Rackman',
      version       =   VERSION,
      description   =   'A tool measure distances on the screen',
      keywords      =   'tool, application, gtk, measuring, screen, monitor, mm, in, px, pt',
      author        =   'Nik Volkov',
      author_email  =   'freezemandix@ya.ru',
      url           =   'https://github.com/FRiMN/Rackman',
      py_modules    =   [
                            'rackman',
                        ],
      license       =   'mit',
      data_files    =   [
                            ('/usr/share/icons/hicolor/scalable/apps/', ['rackman.svg']),
                            ('/usr/share/applications', ['rackman.desktop']),
                            #('/usr/share/locale', glob('./locale/*/LC_MESSAGES/*.mo')),
                            ('/usr/share/locale/ru/LC_MESSAGES', ['./locale/ru/LC_MESSAGES/rackman.mo']),
                            ('/usr/share/locale/en/LC_MESSAGES', ['./locale/en/LC_MESSAGES/rackman.mo']),
                        ],
      obsoletes     =   [
                            'Rackman',
                        ],
      requires      =   [
                            'PyGTK (>=2.0)',
                        ],
     )
