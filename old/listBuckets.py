import boto
import boto.s3.connection
import sys
from boto.s3.key import Key

###################### INIT ########################
RADOSHOST = '127.0.0.1'
RADOSPORT = 7480
BUCKETNAME = 'bucket_a'

print "Making connections..."

## UID shivanshu keystone
u1_access_key = '842f26b29ddd4331a5af8fc800ce04ca'
u1_secret_key = 'b772c2bb2ad149fcb941d298e2dabfb5'

conn_u1 = boto.connect_s3(
              aws_access_key_id     = u1_access_key,
              aws_secret_access_key = u1_secret_key,
              host = RADOSHOST,
              port = RADOSPORT,
              is_secure = False,
              calling_format = boto.s3.connection.OrdinaryCallingFormat())

####################################################


################## TEST CASE #######################
print "\nCreating and populating the bucket for user1..."
b1 = conn_u1.create_bucket(BUCKETNAME)
k = Key(b1)
'''
for i in range(1, 11):
    print "\tCreating obj %d" % (i)
    keyv = 'keynum' + str(i)
    valv = 'Contents of object' + str(i)
    k.key = keyv
    k.set_contents_from_string(valv)
    k.set_acl('public-read')

print "\nSetting ACL..."
b1.set_acl('public-read-write')
'''
try:
    print "\nU1: Trying list all buckets for U1"
    b2 = conn_u1.create_bucket('buck_b')
    b3 = conn_u1.create_bucket('buck_c')
    b4 = conn_u1.create_bucket('buck_d')
    b5 = conn_u1.create_bucket('buck_e')
    b6 = conn_u1.create_bucket('buck_f')

    print "\nListing all buckets for user1"
    for buck in conn_u1.get_all_buckets():
        print "Name: " + buck.name

    print "\nListing bucket contents"
    for k in b1.list():
        print "Object: " + str(k)

except:
    print "Unexpected error: ", sys.exc_info()

####################################################


#################### CLEANUP #######################
print "\nCleaning up..."
for bkt in conn_u1.get_all_buckets():
    for k in bkt.list():
        k.delete()
    conn_u1.delete_bucket(bkt.name)

## Test case
conn_u1.delete_bucket('nonexistbuck')

print "Attemting to list buckets"
print "First user's buckets:"
for bucket in conn_u1.get_all_buckets():
    print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)

###################################################
