#!/usr/bin/python2
# -*- coding: utf-8 -*-

import click
import os, sys
import subprocess
import rackman


VERSION = rackman.__version__
RELEASE = 'trusty'

basedir = os.path.realpath('.')


@click.group(chain=True)
def cli():
    """Building script for Rackman"""
    pass


@cli.command()
def build_deb():
    """Building DEB package"""

    click.secho('*** Creating distribution archive...', fg='yellow')
    comm = "python setup.py sdist"
    try:
        # https://docs.python.org/2/distutils/introduction.html#distutils-simple-example
        os.chdir( basedir )
        subprocess.call(comm, shell=True)
    except OSError as e:
        click.echo("ERR: {}; {}".format(comm, e), err=True)
        sys.exit(os.EX_OSERR)

    click.secho('*** Transforming to debain package from distribution archive...', fg='yellow')
    comm = "py2dsc --suite='{}' Rackman-{}.tar.gz".format(RELEASE, VERSION)
    try:
        # https://pypi.python.org/pypi/stdeb/#debianize-distutils-command
        os.chdir( "{}/dist".format(basedir) )
        subprocess.call(comm, shell=True)
    except OSError as e:
        click.echo("ERR: {}; {}".format(comm, e), err=True)
        sys.exit(os.EX_OSERR)

    click.secho('*** Configuring and building debian package...', fg='yellow')
    try:
        os.chdir( "{}/dist/deb_dist/rackman-{}".format(basedir, VERSION) )
        subprocess.call("sed -i -- '/^Depends:/ s/$/, python-gtk2 (>=2.24.0), python-cairo (>=1.8.8)/g' ./debian/control", shell=True)
        subprocess.call("sed -i -- '/^Build-Depends:/ s/$/, python-gtk2 (>=2.24.0), python-cairo (>=1.8.8)/g' ./debian/control", shell=True)
        subprocess.call("sed -i -- 's/python-rackman/rackman/g' ./debian/control ./debian/rules", shell=True)
        subprocess.call("dpkg-buildpackage -rfakeroot -uc -us", shell=True)
    except OSError as e:
        click.echo("ERR: dpkg-buildpackage -rfakeroot -uc -us; {}".format(e), err=True)
        sys.exit(os.EX_OSERR)

    click.secho('*** Signing debian package...', fg='yellow')
    comm = "debuild -S -sa -k$GPGKEY"
    try:
        # https://help.ubuntu.com/community/GnuPrivacyGuardHowto
        # https://help.launchpad.net/Packaging/PPA/BuildingASourcePackage
        os.chdir( "{}/dist/deb_dist/rackman-{}".format(basedir, VERSION) )
        subprocess.call(comm, shell=True)
    except OSError as e:
        click.echo("ERR: {}; {}".format(comm, e), err=True)
        sys.exit(os.EX_OSERR)


@cli.command()
def push():
    """Pushing DEB in Launchpad"""
    # https://help.launchpad.net/Packaging/PPA/Uploading#Next_steps
    comm = "dput ppa:freezemandix/rackman rackman_{}-1_source.changes".format(VERSION)
    try:
        os.chdir( "{}/dist/deb_dist/".format(basedir) )
        subprocess.call(comm, shell=True)
    except OSError as e:
        click.echo("ERR: {}; {}".format(comm, e), err=True)
        sys.exit(os.EX_OSERR)


@cli.command()
def clean():
    """Cleaning ./dist and ./build directories"""
    import shutil

    path = os.path.join(basedir, 'dist')
    try:
        shutil.rmtree(path)
    except OSError as e:
        click.echo("ERR: remove {}; {}".format(path, e), err=True)

    path = os.path.join(basedir, 'build')
    try:
        shutil.rmtree(path)
    except OSError as e:
        click.echo("ERR: remove {}; {}".format(path, e), err=True)


@cli.command()
@click.option('--html', '-h', is_flag=True, help='generating html documentation')
@click.option('--man', '-m', is_flag=True, help='generating man documentation')
def build_doc(html, man):
    """Building documentation from README.md"""
    # Building html page
    if html:
        comm = "pandoc " \
               "--standalone " \
               "--self-contained " \
               "--smart " \
               "--normalize " \
               "-V lang:russian " \
               "-f markdown " \
               "-t html " \
               "-o ./doc/html/ru/index.html README.md"
        try:
            os.chdir( basedir )
            subprocess.call(comm, shell=True)
        except OSError as e:
            click.echo("ERR: {}; {}".format(comm, e), err=True)
            sys.exit(os.EX_OSERR)

    # Building man page
    if man:
        from datetime import datetime
        import gzip, shutil
        comm = "pandoc " \
               "--standalone " \
               "--self-contained " \
               "--smart " \
               "--normalize " \
               "-V lang:russian " \
               "-f markdown " \
               "-t man " \
               "-o ./doc/man/ru/rackman README.md"
        date = datetime.today().strftime('%Y-%m-%destroy_window')
        try:
            os.chdir( basedir )
            subprocess.call(comm, shell=True)

            # add metadata in man page
            subprocess.call('''sed -i -- 's/.TH "" "" "" "" ""/.TH RACKMAN 1 {} {} ""/g' ./doc/man/ru/rackman'''.format(date, VERSION), shell=True)

            # compressing man page (rackman -> rackman.1.gz)
            with open(os.path.join(basedir, 'doc/man/ru/rackman'), 'rb') as f_in, gzip.open(os.path.join(basedir, 'doc/man/ru/rackman.1.gz'), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        except OSError as e:
            click.echo("ERR: {}; {}".format(comm, e), err=True)
            sys.exit(os.EX_OSERR)


@cli.command()
@click.option('--update', '-u', is_flag=False, help='update messages.pot from rackman.py')
@click.option('--merge', '-m', is_flag=False, help='merge po files with messages.pot')
@click.option('--add', '-a', is_flag=False, help='add translation for new language')
@click.option('--build', '-b', is_flag=False, help='build mo files from po files')
@click.option('--lang', '-l', default='en', help='language (default=en)')
def build_lang(update, merge, add, build, lang):
    """Building i18n files"""
    # https://help.launchpad.net/Translations/POTemplates

    if update:
        comm = 'xgettext -k_ -kN_ ' \
               '--package-version={} ' \
               '--package-name=rackman ' \
               '--copyright-holder="by Nik Volkov" ' \
               '--msgid-bugs-address=freezemandix@ya.ru ' \
               '-o messages.pot rackman.py'.format(VERSION)
        try:
            os.chdir( basedir )
            subprocess.call(comm, shell=True)
        except OSError as e:
            click.echo("ERR: {}; {}".format(comm, e), err=True)
            sys.exit(os.EX_OSERR)

    if add:
        comm = 'msginit --locale={}'.format(lang)
        try:
            os.chdir( basedir )
            subprocess.call(comm, shell=True)
        except OSError as e:
            click.echo("ERR: {}; {}".format(comm, e), err=True)
            sys.exit(os.EX_OSERR)

    if merge:
        comm = 'msgmerge -UN {}.po messages.pot'.format(lang)
        try:
            os.chdir( basedir )
            subprocess.call(comm, shell=True)
        except OSError as e:
            click.echo("ERR: {}; {}".format(comm, e), err=True)
            sys.exit(os.EX_OSERR)

    if build:
        comm = 'msgfmt {lang}.po -o locale/{lang}/LC_MESSAGES/rackman.mo'.format(lang=lang)
        try:
            os.chdir( basedir )
            path = 'locale/{}/LC_MESSAGES/'.format(lang)
            if os.path.isdir(path) is False:
                os.makedirs(path)
            subprocess.call(comm, shell=True)
        except OSError as e:
            click.echo("ERR: {}; {}".format(comm, e), err=True)
            sys.exit(os.EX_OSERR)


@cli.command()
@click.pass_context
def build_all(ctx):
    """Building all in DEB (full cycle)"""
    for lang in ('en', 'ru'):
        ctx.invoke(build_lang, lang=lang, update=True, merge=True)
        while True:
            if click.confirm('Whether translations are true to the {} po files?'.format(lang)):
                ctx.invoke(build_lang, lang=lang, build=True)
                break

    ctx.invoke(build_doc, html=True, man=True)
    ctx.invoke(clean)
    ctx.invoke(build_deb)


if __name__ == '__main__':
    cli()
