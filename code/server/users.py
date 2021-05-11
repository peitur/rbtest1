

import re, sys, os
import pathlib
import sqlite3
import server.db

from pprint import pprint

class Users( object ):

    def __init__( self, **opt ):
        self._debug = opt.get( "debug", False )
        self._db_file = opt.get("file", "db/users.db")
        self._db = server.db.Database( file=self._db_file, debug=self._debug )

    def login_user( self, username, passwd ):
        ret = list()
        fields = ["id", "uname","password", "email","role"]
        qres = self._db.query( "users", fields , {"uname": username, "password":passwd } )

        if len( qres ) != 1:
            return None

        for r in qres:
            ret.append( { fields[x]: v for x,v in enumerate(r) } )
        return ret.pop(0)

    def get_username( self, username ):
        ret = list()
        fields = ["id", "uname","role","password","email"]
        qres = self._db.query( "users", fields , {"uname": username } )
        for r in qres:
            ret.append( { fields[x]: v for x,v in enumerate(r) } )
        return ret

    def get_user_comment( self, username ):
        ret = list()
        fields = ["id", "uname","comment"]
        qres = self._db.query( "users", fields , {"uname": username } )
        for r in qres:
            ret.append( { fields[x]: v for x,v in enumerate(r) } )
        return ret.pop(0)['comment']


    def get_userid( self, userid ):
        ret = list()
        fields = ["id", "uname","role","password","email"]
        qres = self._db.query( "users", fields , {"id": userid } )
        for r in qres:
            ret.append( { fields[x]: v for x,v in enumerate(r) } )
        return ret

    def get_all( self ):
        ret = list()
        fields = ["id", "uname","role","email"]
        qres = self._db.query( "users", fields )
        for r in qres:
            ret.append( { fields[x]: v for x,v in enumerate(r) } )
        return ret

    def get_admins( self ):
        ret = list()
        fields = ["id", "uname","role","email"]
        qres = self._db.query( "users", fields, {"role":"admin"} )
        for r in qres:
            ret.append( { fields[x]: v for x,v in enumerate(r) } )
        return ret


    def mk_user( self, username, email, password, role="user", comment='' ):
        self._db.insert( { "uname": username.lower(), "email": email.lower(), 'password': password, "role": role , "comment":comment} )
