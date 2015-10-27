import boto
import boto.s3.connection
from boto.s3.key import Key

###################### INIT ########################
print "Making connections..."
## UID shivanshu
u1_access_key = 'INDCMF1YDM0N785EKCBN'
u1_secret_key = 'oxvVdSd1P3ICWlPyCehdco8h56OPqnyjtOtN52c4'

## UID notshivanshu
u2_access_key = 'EINGB4RLFBLPFLF2BFSJ'
u2_secret_key = 'cKsEUeHUD5GZzfDLbzxHBp3MVw6K2mwYSDrfjaIB'

conn_u1 = boto.connect_s3(
              aws_access_key_id     = u1_access_key,
              aws_secret_access_key = u1_secret_key,
              host = '127.0.0.1',
              port = 7480,
              is_secure = False,
              calling_format = boto.s3.connection.OrdinaryCallingFormat())

conn_u2 = boto.connect_s3(
              aws_access_key_id     = u2_access_key,
              aws_secret_access_key = u2_secret_key,
              host = '127.0.0.1',
              port = 7480,
              is_secure = False,
              calling_format = boto.s3.connection.OrdinaryCallingFormat())

####################################################


################## TEST CASE #######################
print "\nCreating and populating the bucket for user1..."
b1 = conn_u1.create_bucket('bucket_a')
k = Key(b1)
for i in range(1, 11):
    print "\tCreating obj %d" % (i)
    keyv = 'keynum' + str(i)
    valv = 'Contents of object'
    k.key = keyv
    k.set_contents_from_string(valv)

print "\nSetting ACL..."
b1.set_acl('public-read')
##b1.set_acl('private');

b2 = conn_u2.get_bucket(b1.name);
print "\nU2: Name of this bucket is {b2name}".format(b2name = b2.name)
print "U2: Attempting to read objects from a private bucket:"
m = Key(b2)
for i in range(1, 11):
    keyv = 'keynum' + str(i)
    m.key = keyv
    print "Object " + str(i) + ": " + m.get_contents_as_string()
####################################################


#################### CLEANUP #######################
print "\nCleaning up..."
for k in b1.list():
    k.delete()
conn_u1.delete_bucket('bucket_a')

print "Attemting to list buckets for both users"
print "First user's buckets:"
for bucket in conn_u1.get_all_buckets():
    print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)

print "Second user's buckets:"
for bucket in conn_u2.get_all_buckets():
    print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)

####################################################
