import boto
import boto.s3.connection
access_key = 'INDCMF1YDM0N785EKCBN'
secret_key = 'oxvVdSd1P3ICWlPyCehdco8h56OPqnyjtOtN52c4'

conn = boto.connect_s3(
            aws_access_key_id     = access_key,
            aws_secret_access_key = secret_key,
            host = '127.0.0.1',
            port = 7480,
            is_secure = False,
            calling_format = boto.s3.connection.OrdinaryCallingFormat())

u2_access_key = 'EINGB4RLFBLPFLF2BFSJ'
u2_secret_key = 'cKsEUeHUD5GZzfDLbzxHBp3MVw6K2mwYSDrfjaIB'

conn_u2 = boto.connect_s3(
              aws_access_key_id     = u2_access_key,
              aws_secret_access_key = u2_secret_key,
              host = '127.0.0.1',
              port = 7480,
              is_secure = False,
              calling_format = boto.s3.connection.OrdinaryCallingFormat())





#bucket = conn.create_bucket('my-new-bucket')

print "First user's buckets:"
for bucket in conn.get_all_buckets():
    print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)
    ##conn.delete_bucket(bucket.name)

print "Second user's buckets:"
for bucket in conn_u2.get_all_buckets():
    print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)
