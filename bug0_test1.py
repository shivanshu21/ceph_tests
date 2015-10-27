import boto
import boto.s3.connection

u1_access_key = 'INDCMF1YDM0N785EKCBN'
u1_secret_key = 'oxvVdSd1P3ICWlPyCehdco8h56OPqnyjtOtN52c4'
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

b1 = conn_u1.create_bucket('shivanshu_bucket')
print "\nCreated one bucket: "
for bucket in conn_u1.get_all_buckets():
    print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)

print "\nSetting ACL..."
##b1.set_acl('public-read')
b1.set_acl('private');

b2 = conn_u2.get_bucket(b1.name);
print "U2 Reads: Name of this bucket is {b2name}".format(b2name = b2.name)
