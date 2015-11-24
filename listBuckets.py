import dsslib
import math, os
from filechunkio import FileChunkIO
import sys
import time
from boto.s3.key import Key

dsslib.GLOBAL_DEBUG = 1
dsslib.RADOSHOST = '127.0.0.1'
dsslib.RADOSPORT = 7480
CALLER = dsslib.USER_keystone800

obj = dsslib.getConnection(CALLER)
dsslib.listBucketNum(obj, "user800")
##dsslib.listBucket(obj, "user800")

##==========================================================




'''=================================================================
##Keeps listing bucket and other script changes ACLs
b1 = obj.get_bucket('rjil800bucket200010')
b1.set_acl('public-read')

intruder = dsslib.getConnection(dsslib.USER_keystone801)
for i in range(1, 101):
    try:
        b2 = intruder.get_bucket('rjil800bucket200010')
        print b2.list()
    except:
        print "Error: ", sys.exc_info()
====================================================================
'''

'''
##Checks if the buckets created post 1000 are actually present. And checks if a ghost bucket is present.
====================================================================
try:
    print "Getting created bucket 10"
    b = obj.get_bucket('rjil800bucket200010')
    print "Getting created bucket 14"
    c = obj.get_bucket('rjil800bucket200014')
except:
    print "Error: ", sys.exc_info()

print "Increased bucket capacity per user. Now trying to create buckets"
for i in range(1, 11):
    print "Creating rjil800bucket2000" + str(i)
    obj.create_bucket('rjil800bucket2000' + str(i))
'''
