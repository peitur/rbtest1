#!/usr/bin/env python3

import os, sys, re
import flask
import jinja2
import sqlite3
import hashlib

import server.users

from pprint import pprint

USERS={
    "user1":{ "id":"1", "name":"user one", "passwd":"user1pass", "role":"admin"},
    "user2":{ "id":"2", "name":"user two", "passwd":"user2pass", "role":"user" },
    "user3":{ "id":"3", "name":"user three", "passwd":"user3pass", "role":"user"},
    "user4":{ "id":"4", "name":"user four", "passwd":"user4pass", "role":"user"}
}

DB_FILE="db/test.db"
users = server.users.Users(  file=DB_FILE )

app = flask.Flask( __name__, template_folder="templates.d" )
app.secret_key = b'aaaaaaaaaaaaaaaaaaaaaa'

@app.route('/')
@app.route('/index')
@app.route('/login', methods=['GET', 'POST'])
def page_login( ):

    if flask.request.method == 'POST':

        username = flask.request.form['username']
        reqpaswd = get_checksum( flask.request.form['userpass'] )

        q = users.get_user( username )
        if len( q ) != 1:
            return flask.redirect( flask.url_for( 'page_error_badlogin' ) )

        info = q.pop(0)

        refpaswd = info['password']

        if refpaswd == reqpaswd:

            flask.session['username'] = username
            flask.session['userid'] = info['id']
            flask.session['userrole'] = info['role']
            flask.session['email'] = info['email']
            flask.session['role'] = info['role']

            pprint( info )

            if info['role'] in ("user"):
                return flask.redirect( flask.url_for( 'page_user' ) )
            elif info['role'] in ("admin"):
                return flask.redirect( flask.url_for( 'page_admin' ) )
            else:
                return flask.redirect( flask.url_for( 'page_logout' ) )

        else:
            return flask.redirect( flask.url_for( 'page_error_badlogin' ) )

    return flask.render_template("login.j2")


@app.route('/user')
def page_user():

    if 'username' in flask.session and flask.session['username']:
        username = flask.session['username']
        user = users.get_user( username ).pop(0)

        return flask.render_template("user.j2", user={ "name": user['uname']} )

    return flask.redirect( "/error" )


@app.route('/admin')
def page_admin():
    ## SEC: user role validation not done
    if 'username' in flask.session and flask.session['username']:
        username = flask.session['username']
        user = users.get_user( username ).pop(0)

        return flask.render_template("admin.j2", user={ "name": user['uname']} )

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
