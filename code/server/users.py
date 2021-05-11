

import re, sys, os
import pathlib
import sqlite3
import server.db


class Users( object ):

    def __init__( self, **opt ):
        self._debug = opt.get( "debug", False )
        self._db_file = opt.get("file", "db/users.db")
        self._db = server.db.Database( file=self._db_file )

    def get_user( self, username ):
        ret = list()
        fields = ["id", "uname","role","password","email"]
        qres = self._db.query( "users", fields , {"uname": username } )
        for r in qres:
            ret.append( { fields[x]: v for x,v in enumerate(r) } )
        return ret


    def get_all( self ):
        ret = list()
        fields = ["id", "uname","role","password","email"]
        qres = self._db.query( "users", fields )
        for r in qres:
            ret.append( { fields[x]: v for x,v in enumerate(r) } )
        return ret

    def mk_user( self, username, email, password, role="user" ):
        self._db.insert( { "uname": username.lower(), "email": email.lower(), 'password': password, "role": role } )
