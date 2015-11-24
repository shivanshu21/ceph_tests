import dsslib
import math, os
import sys
import time
from boto.s3.key import Key

dsslib.GLOBAL_DEBUG = 1
dsslib.RADOSHOST = '127.0.0.1'
dsslib.RADOSPORT = 7480
CALLER = dsslib.USER_keystone3
#CALLER = dsslib.USER_aws1

################ PUBLIC URL TESTS ##################

def publicUrlTest():
    result = 0
    obj = dsslib.getConnection(CALLER)
    b1 = obj.create_bucket('urlbucket1')
    k = Key(b1)
    k.key = 'obj1'
    k.set_contents_from_string('Data of URL object')
    print "Setting ACL on obj"
    k.set_acl('public-read')
    print "Setting ACL on bucket"
    b1.set_acl('public-read')

    m = Key(b1)
    m.key = 'obj1'
    urlname = m.generate_url(1000)
    print "\nThe obj URL is: " + str(urlname)
    urlname = b1.generate_url(1000)
    print "\nThe bucket URL is: " + str(urlname)

    for i in range(1, 21):
        time.sleep(1)
        if i % 5 == 0:
            print str(20 - i) + " Seconds left before Obj deletion"

    m.delete()
    print "Object deleted\n"

    for i in range(1, 21):
        time.sleep(1)
        if i % 5 == 0:
            print str(20 - i) + " Seconds left before bucket deletion"

    obj.delete_bucket('urlbucket1')
    print "Bucket deleted\n"
    return result

def changeAcls():
    result = 0
    obj = dsslib.getConnection(CALLER)
    b1 = obj.create_bucket('aclbucket1')
    k = Key(b1)
    k.key = 'obj1'
    k.set_contents_from_string('Data of object')

    print "Setting ACL on obj"
    k.set_acl('public-read')
    print "Setting ACL on bucket"
    b1.set_acl('public-read')

    for i in range(1, 7):
        time.sleep(10)
        print "Toggling ACL"

    return result
####################################################

#################### CALL TESTS ####################

##dsslib.callTest(publicUrlTest(), "Public URL test")
dsslib.callTest(changeAcls(), "keep changing ACLs")
####################################################
