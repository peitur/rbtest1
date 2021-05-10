
import re
import string
import unicodedata
from pprint import pprint

if __name__ == "__main__":
    pprint( dir( unicodedata ) )

    tst = "http://google.com"
    res = bytes( tst, "unicode-escape" )

    pprint( bytes( tst, "utf8" ) )
    for b in tst:
        r = b.encode("unicode-escape")
        #print( "%{:04d}".format( ord( r ) ), end="" )
        print("%{:02X}".format( ord( r ) ), end="" )
    print()
    print()
    for b in tst:
        r = b.encode("unicode-escape")
        print( "{0}".format(r), end="" )

    print()
    print()

    print( "{}".format( res ) )
