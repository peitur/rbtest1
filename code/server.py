#!/usr/bin/env python3

import os, sys, re
import flask
import jinja2
import sqlite3
import hashlib

import server.users

from pprint import pprint

DB_FILE="db/test.db"
users = server.users.Users(  file=DB_FILE, debug=True )

app = flask.Flask( __name__, template_folder="templates.d" )
app.secret_key = b'aaaaaaaaaaaaaaaaaaaaaa'

@app.route('/')
@app.route('/index')
@app.route('/login', methods=['GET', 'POST'])
def page_login( ):

    if flask.request.method == 'POST':

        username = flask.request.form['username']
        reqpaswd = get_checksum( flask.request.form['userpass'] )

        info = users.login_user( username, reqpaswd )

        if not info:
            return flask.redirect( flask.url_for( 'page_error_badlogin' ) )

        pprint( info )

        flask.session['username'] = info['uname']
        flask.session['userid'] = info['id']
        flask.session['userrole'] = info['role']
        flask.session['email'] = info['email']
        flask.session['role'] = info['role']


        if info['role'] in ("user"):
            return flask.redirect( flask.url_for( 'page_user' ) )
        elif info['role'] in ("admin"):
            return flask.redirect( flask.url_for( 'page_admin' ) )
        else:
            return flask.redirect( flask.url_for( 'page_logout' ) )

    admins = users.get_admins()
    return flask.render_template("login.j2", adminlist=admins)


@app.route('/user')
def page_user():

    if 'username' in flask.session and flask.session['username']:
        username = flask.session['username']
        user = users.get_username( username ).pop(0)
        admins = users.get_admins()
        return flask.render_template("user.j2", user={ "name": user['uname'], "role": user['role']}, adminlist=admins )

    return flask.redirect( "/error" )


@app.route('/admin')
def page_admin():
    ## SEC: user role validation not done
    if 'username' in flask.session and flask.session['username']:
        username = flask.session['username']
        user = users.get_username( username ).pop(0)
        admins = users.get_admins()
        ucomment = users.get_user_comment( username )

        return flask.render_template("admin.j2", user={ "name": user['uname'], "comment": ucomment }, adminlist=admins )

    return flask.redirect( "/error" )

@app.route('/register',methods=['GET', 'POST'])
def page_register():
    flask.session.clear()

    if flask.request.method == 'POST':
        role = "user"
        firstname = flask.request.form['fname']
        lastname = flask.request.form['fname']
        username = "%s.%s" % ( firstname.lower(), lastname.lower() )
        email = flask.request.form['email']
        if flask.request.form['userpass1'] != flask.request.form['userpass2']:
            return flask.redirect( "/error" )
        password = get_checksum( flask.request.form['userpass1'] )
        if 'role' in flask.request.form:
            role = flask.request.form['role']
        users.mk_user( username, email, password, role )

        return flask.redirect( flask.url_for( 'page_login' ) )

    admins = users.get_admins()
    return flask.render_template("register.j2" )


@app.route('/logout',methods=['GET', 'POST'])
def page_logout():
    flask.session.clear()
    return flask.redirect( flask.url_for( 'page_login' ) )


@app.route('/error/bad_login')
def page_error_badlogin():
    return "bad login"

@app.route('/error')
def page_error():
    return "oops"

################
def get_checksum( s ):
    o = hashlib.new("sha1")
    o.update( s.encode("utf-8") )
    return o.hexdigest()


if __name__ == "__main__":
    app.run( host="0.0.0.0", debug=True )
