import boto
import boto.s3.connection
from boto.s3.key import Key

###################### INIT ########################
RADOSHOST = '127.0.0.1'
RADOSPORT = 7480

print "Making connections..."

'''
## Local users
u1_access_key = 'INDCMF1YDM0N785EKCBN'
u1_secret_key = 'oxvVdSd1P3ICWlPyCehdco8h56OPqnyjtOtN52c4'
u2_access_key = 'EINGB4RLFBLPFLF2BFSJ'
u2_secret_key = 'cKsEUeHUD5GZzfDLbzxHBp3MVw6K2mwYSDrfjaIB'
'''

## UID shivanshu keystone
u1_access_key = '842f26b29ddd4331a5af8fc800ce04ca'
u1_secret_key = 'b772c2bb2ad149fcb941d298e2dabfb5'

## UID goswami keystone Same tenant as shivanshu
u2_access_key = 'cb92f272dc514e80acc782023c442c20'
u2_secret_key = 'd115d835aa2a4053a5d66bd93aea2046'

## UID reliance keystone Diff tenant
##u2_access_key = '911093f31862430b955a6cdea71fee2e'
##u2_secret_key = '31a3770da550495d99dcc065488e1351'
##'''

conn_u1 = boto.connect_s3(
              aws_access_key_id     = u1_access_key,
              aws_secret_access_key = u1_secret_key,
              host = RADOSHOST,
              port = RADOSPORT,
              is_secure = False,
              calling_format = boto.s3.connection.OrdinaryCallingFormat())

conn_u2 = boto.connect_s3(
              aws_access_key_id     = u2_access_key,
              aws_secret_access_key = u2_secret_key,
              host = RADOSHOST,
              port = RADOSPORT,
              is_secure = False,
              calling_format = boto.s3.connection.OrdinaryCallingFormat())

####################################################


################## TEST CASE #######################
print "\nCreating and populating the bucket for user1..."
b1 = conn_u1.create_bucket('bucket_b')
k = Key(b1)
for i in range(1, 11):
    print "\tCreating obj %d" % (i)
    keyv = 'keynum' + str(i)
    valv = 'Contents of object'
    k.key = keyv
    k.set_contents_from_string(valv)

print "\nSetting ACL..."
b1.set_acl('public-read-write')

b2 = conn_u2.get_bucket(b1.name);
print "\nU2: Name of this bucket is {b2name}".format(b2name = b2.name)

print "\nU2: Listing keys from U1 bucket"
for i in b2.list():
    print "U1 bucket key: " + str(i)

print "\nU2 tries to write to this bucket"
m = Key(b2)
for i in range(20, 25):
    print "\tCreating obj %d" % (i)
    keyv = 'keynum' + str(i)
    valv = 'Contents of object'
    k.key = keyv
    k.set_contents_from_string(valv)

print "\nU2: Listing keys from U1 bucket to see its own objects"
for i in b2.list():
    print "bucket key: " + str(i)

print "\nU2 tries to fetch its own object:"
m.key = 'keynum20'
print "My object: " + m.get_contents_as_string()

print "U2: Attempting to fetch objects of other user:"
for i in range(1, 11):
    keyv = 'keynum' + str(i)
    m.key = keyv
    print "Object " + str(i) + ": " + m.get_contents_as_string()
####################################################


#################### CLEANUP #######################
print "\nCleaning up..."
for k in b1.list():
    k.delete()
conn_u1.delete_bucket('bucket_b')

print "Attemting to list buckets for both users"
print "First user's buckets:"
for bucket in conn_u1.get_all_buckets():
    print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)

print "Second user's buckets:"
for bucket in conn_u2.get_all_buckets():
    print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)

####################################################
