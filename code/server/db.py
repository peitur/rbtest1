
import re, sys, os
import pathlib
import sqlite3

class Database( object ):

    def __init__( self, file, **opt ):
        self._debug = opt.get('debug', False )
        self._db_file = file
        self._db = sqlite3.connect( self._db_file )


    def init( self ):
        fields = {
            "id":"INTEGER PRIMARY KEY AUTOINCREMENT",
            "uname": "TEXT UNIQUE",
            "email": "TEXT UNIQUE",
            "password":"TEXT",
            "role":"TEXT"
        }

        sql_str = "CREATE TABLE IF NOT EXISTS users( %s )" % ( ", ".join( [ "%s %s" % (x,fields[x] ) for x in fields ] ) )
        if self._debug:
            print("Creating table and fields: %s" % ( sql_str) )

        cur = self._db.cursor()
        cur.execute( sql_str )
        self._db.commit()

    def query( self, where=dict() ):
        w = ""
        if len( where ) > 0:
            w = "where %s" % ( " and ".join( [ "%s == '%s'" % (x, where[x] ) for x in where ] ) )

        qstr = "select * from users %s" % (w)
        if self._debug:
            print("DB Q: %s" % ( qstr) )
        cur = self._db.cursor()
        cur.execute( qstr )
        return cur.fetchall()

    def update( self, data, where=dict() ):
        qstr = "select * from users where user.id == '%s'" % ( userid )
        if self._debug:
            print("DB U: %s" % ( qstr) )

        cur = self._db.cursor()
        cur.execute( qstr )
        self._db.commit()

    def insert( self, data ):
        qstr = "insert into users( uname, email, password, role ) values( '%s', '%s', '%s', '%s' )" % ( data['uname'], data['email'], data['password'], data['role'] )
        if self._debug:
            print("DB I: %s" % ( qstr) )

        cur = self._db.cursor()
        try:
            cur.execute( qstr )
        except sqlite3.IntegrityError as e:
            print("ERROR: %s" % ( e ) )

        self._db.commit()
