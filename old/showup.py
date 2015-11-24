import boto
import boto.s3.connection
import re
import sys
from boto.s3.key import Key

###################### INIT ########################
RADOSHOST = '127.0.0.1'
RADOSPORT = 7480
BUCKETNAME = 'bucket_a'

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
##u2_access_key = 'cb92f272dc514e80acc782023c442c20'
##u2_secret_key = 'd115d835aa2a4053a5d66bd93aea2046'

## UID reliance keystone Diff tenant
u2_access_key = '911093f31862430b955a6cdea71fee2e'
u2_secret_key = '31a3770da550495d99dcc065488e1351'
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

print "Total number of buckets for the user: " + str(len(conn_u1.get_all_buckets()))

print "Attemting to list buckets for both users"
print "First user's buckets:"
for bucket in conn_u1.get_all_buckets():
    print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)

####################################################
