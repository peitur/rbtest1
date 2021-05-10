#!/usr/bin/env python3

import os, sys, re
import flask
import jinja2
import sqlite3
import hashlib

import server.db

from pprint import pprint

USERS={
    "user1":{ "id":"1", "name":"user one", "passwd":"user1pass", "role":"admin"},
    "user2":{ "id":"2", "name":"user two", "passwd":"user2pass", "role":"user" },
    "user3":{ "id":"3", "name":"user three", "passwd":"user3pass", "role":"user"},
    "user4":{ "id":"4", "name":"user four", "passwd":"user4pass", "role":"user"}
}

db = server.db.Database("db/test.db")

app = flask.Flask( __name__, template_folder="templates.d" )
app.secret_key = b'aaaaaaaaaaaaaaaaaaaaaa'

@app.route('/')
@app.route('/index')
@app.route('/login', methods=['GET', 'POST'])
def page_login( ):

    if flask.request.method == 'POST':

        username = flask.request.form['username']

        info = db.query( {"uname": username })
        pprint( info )

        reqpaswd = get_checksum( flask.request.form['userpass'] )
        refpaswd = info['password']

        if refpaswd == reqpaswd:

            user = info
            flask.session['username'] = username
            flask.session['userid'] = user['id']

            if user['role'] in ("user"):
                return flask.redirect( flask.url_for( 'page_user' ) )
            elif user['role'] in ("admin"):
                return flask.redirect( flask.url_for( 'page_admin' ) )

        else:
            return flask.redirect( flask.url_for( 'page_error_badlogin' ) )

    return flask.render_template("login.j2")


@app.route('/user')
def page_user():

    if 'username' in flask.session and flask.session['username']:
        user = USERS[ flask.session['username']]

        return flask.render_template("user.j2", user={ "name": user['name']} )

    return flask.redirect( "/error" )


@app.route('/admin')
def page_admin():

    if 'username' in flask.session and flask.session['username']:
        user = USERS[ flask.session['username']]

        return flask.render_template("admin.j2", user={ "name": user['name']} )

    return flask.redirect( "/error" )


@app.route('/logout',methods=['GET', 'POST'])
def page_logout():
    flask.session.clear()
    return flask.redirect( flask.url_for( 'page_login' ) )


@app.route('/error/bad_login')
def page_error_badlogin():
    return "bad login"


################
def get_checksum( s ):
    o = hashlib.new("sha1")
    o.update( s.encode("utf-8") )
    return o.hexdigest()


if __name__ == "__main__":
    app.run( host="0.0.0.0", debug=True )
