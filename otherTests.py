import sys
import time
import dsslib
import math, os
from boto.s3.key import Key
from filechunkio import FileChunkIO

dsslib.GLOBAL_DEBUG = 1
dsslib.RADOSHOST = '127.0.0.1'
dsslib.RADOSPORT = 7480
#CALLER = dsslib.USER_keystone803
#obj = dsslib.getConnection(CALLER)



'''=========================================================
## AWS user policy prevents user from listing bucket but allows getting objects inside the particular bucket
## Make listing buckets allowed. Generate signed URLs then make listing buckets not allowed in user policy.
## Check if the URLs still work.
'''
obj = dsslib.getConnection(dsslib.USER_aws2)
b = obj.get_bucket('shivanshubucketauto4')
for i in b.list():
    print 'New key: ' + str(i)
    try:
        print str(i)
        #print "Trying to get object URL..."
        #print i.generate_url(1000);
    except:
        print "No permission!"







'''=========================================================
##Try getting bucket of vishaluec tenant from user under shivanshu21 in AWS

#dsslib.createMaxBuckets(dsslib.USER_aws1, 10, "shivanshubucketauto")
obj = dsslib.getConnection(dsslib.USER_aws1)
alienBucket = obj.get_bucket('shivanshubucketman00')
j = 0
for i in alienBucket.list():
    j = j + 1
    print 'New key: ' + str(i)
    try:
        print "Trying to get object" + str(j) + "..."
        i.get_contents_to_filename('file' + str(j))
        print "===== Got it."
    except:
        print "No permission!"
'''



'''=========================================================
##Try coping an object from a public read bucket to a public read write bucket
b1 = obj.get_bucket('rjil803bucket997')
b1.set_acl('public-read')
key1 = Key(b1)
key1.key = 'rjil803bucket997_OBJ_1'

newobj = dsslib.getConnection(dsslib.USER_keystone804)
newobj.create_bucket('mynewbucket')
b2 = newobj.get_bucket('mynewbucket')
b2.set_acl('public-read-write')

key1.copy('mynewbucket', 'copiedkey')
print "Copied key. Sleeping."
time.sleep(10)

key2 = Key(b2)
key2.key = 'copiedkey'
key2.delete()
newobj.delete_bucket('mynewbucket')
'''

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
