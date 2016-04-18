#!/usr/bin/env python

from distutils.core import setup
from rackman import __version__

setup(name          =   'Rackman',
      version       =   __version__,
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
                            ('/usr/share/rackman', ['rackman.conf']),
                            ('/usr/share/locale/ru/LC_MESSAGES', ['./locale/ru/LC_MESSAGES/rackman.mo']),
                            ('/usr/share/locale/en/LC_MESSAGES', ['./locale/en/LC_MESSAGES/rackman.mo']),
                            ('/usr/share/doc/rackman/html/ru', ['./doc/html/ru/index.html']),
                            ('/usr/share/man/ru/man1', ['./doc/man/ru/rackman.1.gz']),
                        ],
      obsoletes     =   [
                            'Rackman',
                        ],
      requires      =   [
                            'PyGTK (>=2.0)',
                        ],
      scripts       =   [
                            'rackman'
                        ],
     )
