# -*- coding: utf-8 -*-
"""
    argus
    ~~~~~~

    A monitoring tool

    :copyright: (c) 2013-2018 by Michiel Scholten.
    :license: BSD, see LICENSE for more details.
"""

from sqlite3 import dbapi2 as sqlite3

import click
from flask import (Flask, _app_ctx_stack, abort, flash, g, redirect,
                   render_template, request, session, url_for)

import settings
from modules import diskspacealarm, network, pushover

# get hostname for the current node
HOSTNAME = network.get_local_hostname()

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db


@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


## Main program
@click.group()
def cli():
    pass


@cli.command()
def check_diskspace():
    diskspacealarm.check_diskspace(settings, HOSTNAME)


@cli.command()
def rebooted():
    """Sends a message about the node having rebooted"""
    message = '[{}] Node has been rebooted. Local IP is {}, public IP is {}'.format(
        HOSTNAME,
        network.get_local_ip(),
        network.get_public_ip()
    )
    pushover.send_message(settings, message)


@cli.command()
def node_info():
    print('Node {}\nLocal IP is {}\nPublic IP is {}\n'.format(
        HOSTNAME,
        network.get_local_ip(),
        network.get_public_ip()
    ))
    diskspace_info  = diskspacealarm.check_diskspace(settings, HOSTNAME)
    if diskspace_info:
        print(diskspace_info)


if __name__ == '__main__':
    #init_db()
    cli()
    app.run()
