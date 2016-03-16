import os
import sys
import time
import dssSanityLib
from boto.s3.key import Key

###################### MAIN ########################

def main(argv):

    ## PARAM OVERRIDES
    dssSanityLib.GLOBAL_DEBUG = 1                    # The lib supresses debug logs by default. Override here.
    #dssSanityLib.RADOSHOST = '127.0.0.1'            # The lib points to DSS staging endpoint by default. Override here.
    #dssSanityLib.RADOSPORT = 7480                   # The lib points to DSS staging endpoint by default. Override here.

    ret = dssSanityLib.fetchArgs(argv)
    if(ret == -1):
        sys.exit(2)

    userObj = dssSanityLib.getConnection(1)
    b = userObj.create_bucket('gangadhar')
    #k = Key(b)
    #k.key = 'obj'
    #k.set_contents_from_string('obj text')
    #out = k.get_contents_as_string()
    #k.set_acl('public-read-write')
    #k.get_acl()

    #b.set_acl('private')
    #b.get_acl()

    #nuObj = dssSanityLib.getConnection(2)
    #c = nuObj.get_bucket('twopubbuck')
    #k = Key(c)
    #k.key = 'obj500'
    #k.set_contents_from_string('obj text')

    return

if __name__ == "__main__":
    main(sys.argv[1:])

####################################################
'''
#    userObj.create_bucket('bucket0');
#    userObj.create_bucket('bucket1');
#    userObj.create_bucket('bucket2');
#    userObj.create_bucket('bucket3');
#    userObj.create_bucket('bucket4');
#    userObj.create_bucket('bucket5');
#    userObj.create_bucket('bucket6');
#    userObj.create_bucket('bucket7');
#    userObj.create_bucket('bucket8');
#    userObj.create_bucket('bucket9');

'''


'''
    #print userObj.get_all_buckets();
    b = userObj.get_bucket('shivbucket0002');
    k = Key(b)
    k.key = 'obj501'
    #k.set_contents_from_string('obj500 sample text')
    out = k.get_contents_as_string()
    print "Obj has: " + str(out)
    #k.delete()

    # Copy object workflow
    b = userObj.create_bucket('copysourcebucket')
    k = Key(b)
    k.key = 'obj500'
    k.set_contents_from_string('obj text')

    c = userObj.get_bucket('copydestbucket')
    l = c.copy_key('obj', 'copysourcebucket', 'obj')
    print str(l)
'''

