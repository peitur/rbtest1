#!/usr/bin/env python3

import os, sys, re
import flask
import jinja2
import sqlite3
import hashlib
import random

import server.users

from pprint import pprint

DB_FILE="db/test.db"
users = server.users.Users(  file=DB_FILE )


SEPPARATOR="."

ADMINUSERS=[
    {"uname":"peter.bartha","email":"peter.bartha@redbridge.se", "password":"qwerty", "role":"admin","comment":"ssh: user1/passwd1"},
    {"uname":"jonas.svensson","email":"jonas.svensson@redbridge.se", "password":"qwerty", "role":"admin","comment":"ssh: user1/passwd1"}
]

PASSWORDS=["password","123456","12345678","1234","qwerty","12345","dragon","pussy","baseball","football","letmein","monkey","696969","abc123","mustang","michael","shadow","master","jennifer","111111","2000","jordan","superman","harley","1234567","fuckme","hunter","fuckyou","trustno1","ranger","buster","thomas","tigger","robert","soccer","fuck","batman","test","pass","killer","hockey","george","charlie","andrew","michelle","love","sunshine","jessica","asshole","6969","pepper","daniel","access","123456789","654321","joshua","maggie","starwars","silver","william","dallas","yankees","123123","ashley","666666","hello","amanda","orange","biteme","freedom","computer","sexy","thunder","nicole","ginger","heather","hammer","summer","corvette","taylor","fucker","austin","1111","merlin","matthew","121212","golfer","cheese","princess","martin","chelsea","patrick","richard","diamond","yellow","bigdog","secret","asdfgh","sparky","cowboy","camaro","anthony"]

FIRSTNAMES=[
    "Maria","Elisabeth","Anna","Kristina","Margareta","Eva","Linnéa","Karin","Birgitta","Marie","Ingrid","Sofia","Marianne","Lena","Sara","Helena","Kerstin","Emma","Katarina","Johanna","Viktoria","Inger","Cecilia","Susanne","Elin","Monica","Therese","Jenny","Hanna","Louise","Anita","Carina","Irene","Ann","Ida","Linda","Helen","Gunilla","Ulla","Viola","Malin","Annika","Elsa","Ingegerd","Matilda","Josefin","Ulrika","Sofie","Anette","Alice","Julia","Astrid","Caroline","Anneli","Emelie","Kristin","Barbro","Karolina","Lisa","Amanda","Åsa","Camilla","Madeleine","Lovisa","Siv","Erika","Yvonne","Agneta","Maja","Charlotte","Rut","Britt","Sandra","Rebecca","Gun","Isabelle","Alexandra","Frida","Ellinor","Ebba","Emilia","Jessica","Ellen","Berit","Klara","Olivia","Märta","Charlotta","Ann-Marie","Agnes","Inga","Sonja","Ann-Christin","Pia","Maj","Felicia","Ella","Mona","Nathalie","Lisbeth","Karl","Erik","Lars","Anders","Per","Mikael","Johan","Olof","Nils","Jan","Gustav","Hans","Peter","Lennart","Gunnar","Fredrik","Sven","Thomas","Daniel","Bengt","Alexander","Bo","Oskar","Göran","Åke","Andreas","Christer","Stefan","Magnus","Martin","John","Mattias","Mats","Mohamed","Henrik","Leif","Ulf","Jonas","Björn","Axel","Robert","Christian","Marcus","Viktor","David","Bertil","Emil","Niklas","Arne","Ingemar","Patrik","Håkan","Christoffer","Kjell","Rickard","Joakim","Stig","Rolf","William","Wilhelm","Filip","Tommy","Roland","Simon","Sebastian","Claes","Anton","Roger","Kent","Ingvar","Johannes","Tobias","Jakob","Elias","Hugo","Ove","Jonathan","Lucas","Adam","Emanuel","Kenneth","Jörgen","Robin","Ali","Kurt","Rune","Oliver","Josef","Georg","Gösta","Isak","Arvid","Johnny","Linus","Ludvig","Albin","Torbjörn","Olle","Edvin","Dan"
]

LASTNAMES=[
    "Andersson","Johansson","Karlsson","Nilsson","Eriksson","Larsson","Olsson","Persson","Svensson","Gustafsson","Pettersson","Jonsson","Jansson","Hansson","Bengtsson","Jönsson","Lindberg","Jakobsson","Magnusson","Olofsson","Lindström","Lindqvist","Lindgren","Berg","Axelsson","Bergström","Lundberg","Lind","Lundgren","Lundqvist","Mattsson","Berglund","Fredriksson","Sandberg","Henriksson","Forsberg","Sjöberg","Ali","Wallin","Mohamed","Engström","Eklund","Danielsson","Lundin","Håkansson","Björk","Bergman","Gunnarsson","Holm","Wikström","Samuelsson","Isaksson","Fransson","Bergqvist","Nyström","Holmberg","Arvidsson","Löfgren","Söderberg","Nyberg","Blomqvist","Claesson","Nordström","Ahmed","Mårtensson","Lundström","Hassan","Viklund","Björklund","Eliasson","Pålsson","Berggren","Sandström","Lund","Nordin","Ström","Åberg","Falk","Ekström","Hermansson","Holmgren","Hellström","Dahlberg","Hedlund","Sundberg","Sjögren","Ek","Blom","Abrahamsson","Martinsson","Öberg","Andreasson","Strömberg","Månsson","Hansen","Åkesson","Dahl","Lindholm","Norberg","Holmqvist"
]

MAILPROVIDERS=[
    "gmail.com",
    "hotmail.com",
    "yahoo.com",
    "libe.com"
]

def random_firstname( ):
    return FIRSTNAMES[ random.randint( 0, len( FIRSTNAMES ) - 1 ) ]

def random_lastname( ):
    return LASTNAMES[ random.randint( 0, len( LASTNAMES ) - 1 ) ]

def random_emailprovider( ):
    return MAILPROVIDERS[ random.randint( 0, len( MAILPROVIDERS ) - 1 ) ]

def random_password( ):
    return PASSWORDS[ random.randint( 0, len( PASSWORDS ) - 1 ) ]


def checksum( s ):
    o = hashlib.new("sha1")
    o.update( s.encode("utf-8") )
    return o.hexdigest()


if __name__ == "__main__":
    db = server.db.Database( DB_FILE, debug=True )
    db.init()
    used = list()

    for a in ADMINUSERS:
        m = a['uname']
        u = a['email']
        p = a['password']
        c = a.get("comment", '')
        print("Created admin %s - %s" % ( m.lower(), p ) )
        used.append( m )
#        db.insert( { "uname": m.lower(), "email": u.lower(), 'password': checksum(p), "role": "user" } )
        users.mk_user( m.lower(), u.lower(), checksum( p ), "admin", c )

    for x in range( 0, 100  ):
        f = random_firstname()
        l = random_lastname()
        e = random_emailprovider()
        p = random_password()
        m = "%s.%s" % ( f, l )
        u = "%s@%s" % ( m.lower(), e )
        if m not in used:
            print("Created user %s - %s" % ( m.lower(), p ) )
            used.append( m )
            try:
                users.mk_user( m.lower(), u.lower(), checksum( p ), "user" )
                # { "uname": m.lower(), "email": u.lower(), 'password': checksum(p), "role": "user" } )
            except sqlite3.IntegrityError as e:
                print("ERROR: %s" % ( e ) )
    pprint( users.get_all() )
