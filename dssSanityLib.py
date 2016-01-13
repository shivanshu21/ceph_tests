import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import re
import sys
import time
###################### INIT ########################

# PARAMS
GLOBAL_DEBUG = 1
#RADOSHOST = '127.0.0.1'
#RADOSPORT = 7480
RADOSHOST = 'dss.ind-west-1.staging.jiocloudservices.com'
RADOSPORT = 443

# ACCESS PARAMS
has_incore_params = True
access_key = ''
secret_key = ''
isSecure   = True

####################################################

################## CREATE CONNECTION ###############

def getConnection():
    conn_obj = None
    if (has_incore_params):
        conn_obj = boto.connect_s3(
            aws_access_key_id     = access_key,
            aws_secret_access_key = secret_key,
            host = RADOSHOST,
            port = RADOSPORT,
            is_secure = isSecure,
            calling_format = boto.s3.connection.OrdinaryCallingFormat(),
            #debug = 2,
        )
    else:
        return -1
    return conn_obj

####################################################

############### INFO PRESENTATION ##################

def whisper(mystr):
    if GLOBAL_DEBUG == 1:
        print "DEBUG: " + mystr
    return

def callTest(output, testname):
    if output != 0:
        print "\n\t=====================================\n\t" + testname + " : Failed"
    else:
        print "\n\t=====================================\n\t" + testname + " : Pass"
    print "\t=====================================\n\n"
    return

####################################################

############### DATA POPULATION ####################

def createMaxBuckets(num, buckpref):
    myobj = getConnection()
    if myobj is None:
        print "Cannot get connection object for user"
    else:
        listBucketNum(myobj, "User")
    if len(myobj.get_all_buckets()) < num:
        whisper("Deleting all old buckets")
        cleanupUser(myobj, buckpref)
        whisper("Creating new buckets")
        for i in range(1, num + 1):
            name = buckpref + str(i)
            buck = myobj.create_bucket(name)
            whisper("Creating bucket " + name)
            for j in range(1, 11):
                k = Key(buck)
                k.key = name + '_OBJ_' + str(j)
                whisper("Creating object " + k.key)
                k.set_contents_from_string('Data for obj ' + str(j))
    return;

####################################################

############## CLEANUP AND LISTING #################

def cleanupUser(userObj, patstr = None):
    whisper("Cleaning up...")
    if (patstr):
        pstring = patstr + '*'
    else:
        pstring = '*'
    pattern = re.compile(pstring)
    for bkt in userObj.get_all_buckets():
        if (pattern.match(bkt.name)) or (not patstr):
            for k in bkt.list():
                whisper("Deleting " + str(k))
                k.delete()
            whisper("Deleting bucket " + str(bkt))
            userObj.delete_bucket(bkt.name)

    listBucket(userObj, "User")
    return

def listBucketNum(userObj, uname):
    print "Total number of buckets for " + uname + ": " + str(len(userObj.get_all_buckets()))
    return

def listBucket(userObj, uname):
    print "Listing buckets for " + uname
    for bucket in userObj.get_all_buckets():
        print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)
    return
####################################################

############## KEEP CHANGING ACLS ##################

def keepChangingAcls(bucket):
    obj = getConnection()
    acl_list = ('public-read', 'private')
    for i in range(1, 11):
        b1 = obj.get_bucket(bucket)
        whisper("Changing ACL to " + str(acl_list[i % 2]))
        b1.set_acl(acl_list[i % 2])
        time.sleep(1)
    return
####################################################

################ BUCKET NAME GEN ###################
def getsNewBucketName():
    ts = time.time()
    str_ts = str(ts)
    index = str_ts.find('.')
    str_ts = str_ts[0:index]
    bucketpref = 'rjilbucketsanity' + str_ts
    return bucketpref

####################################################
