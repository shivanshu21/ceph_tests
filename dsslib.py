import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import re
import sys
###################### INIT ########################

# PARAMS
GLOBAL_DEBUG = 0
##RADOSHOST = 's3-website-us-west-2.amazonaws.com'
##RADOSPORT = 80
RADOSHOST = '127.0.0.1'
RADOSPORT = 7480

# USER PROFILES
USER_local1 = 0
USER_local2 = 1
USER_keystone1 = 2
USER_keystone2 = 3
USER_keystone3 = 4
USER_keystone800 = 5
USER_keystone801 = 6
USER_keystone802 = 7
USER_keystone803 = 8
USER_keystone804 = 9
USER_aws1 = 10
USER_aws2 = 11
USER_aws3 = 12
USER_aws4 = 13

user_profiles = [
        {'access': 'INDCMF1YDM0N785EKCBN'            , 'secret': 'oxvVdSd1P3ICWlPyCehdco8h56OPqnyjtOtN52c4'}, ## Local user1
        {'access': 'EINGB4RLFBLPFLF2BFSJ'            , 'secret': 'cKsEUeHUD5GZzfDLbzxHBp3MVw6K2mwYSDrfjaIB'}, ## Local user2
        {'access': '842f26b29ddd4331a5af8fc800ce04ca', 'secret': 'b772c2bb2ad149fcb941d298e2dabfb5'}, ## admintenant user1
        {'access': 'cb92f272dc514e80acc782023c442c20', 'secret': 'd115d835aa2a4053a5d66bd93aea2046'}, ## admintenant user2
        {'access': '911093f31862430b955a6cdea71fee2e', 'secret': '31a3770da550495d99dcc065488e1351'}, ## roottenant  user1
        {'access': '5b1b1de1e75c44df8f66b9ccfa36e7b4', 'secret': '741feaaf1c5142dd93ab9d622e47de1c'}, ## USER Tenant Role 800
        {'access': '06abdb34014a48f5b31a75171a820cba', 'secret': 'd98cb04ddafb48859e461b9cfbce2bc4'}, ## USER Tenant Role 801
        {'access': '6fd687641b69440b9e47261ead074bec', 'secret': '0859f01207394b5eaebbbf63920485ec'}, ## USER Tenant Role 802
        {'access': 'af12fdd0d8aa447f92b5af083a34c6fe', 'secret': '8644fcb3be854900959573237911f245'}, ## USER Tenant Role 803
        {'access': '1acc62c9a01a4f9aa3dc0773cdc8b9de', 'secret': 'e1ba72ff044d41d4baf57ae083f23533'}, ## USER Tenant Role 804
        {'access': 'AKIAIGMW3FGB7KRR7ZRQ',             'secret': '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'}, ## AWS shivanshu21 User_pers0
        {'access': 'AKIAJMPEGDRHNCBXZZAQ',             'secret': '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'}, ## AWS shivanshu21 User_pers1
        {'access': 'AKIAJRH3XDVUZMPYWOQQ',             'secret': '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'}, ## AWS shivanshuG
        {'access': 'AKIAJ7JM6D3OFIV4PZSA',             'secret': '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'}, ## AWS shivanshu21 pers3
    ]

####################################################

################## CREATE CONNECTION ###############

def getConnection(user):
    if user > 9:
        AWS_ACCESS_KEY_ID = user_profiles[user]['access']
        AWS_SECRET_ACCESS_KEY = user_profiles[user]['secret']
        conn_obj = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        if conn_obj is None:
            print "NULL Object returned for user!!"
        return conn_obj

    conn_obj = boto.connect_s3(
                   aws_access_key_id     = user_profiles[user]['access'],
                   aws_secret_access_key = user_profiles[user]['secret'],
                   host = RADOSHOST,
                   port = RADOSPORT,
                   is_secure = False,
                   calling_format = boto.s3.connection.OrdinaryCallingFormat()
               )
    return conn_obj

####################################################

#################### WHISPER #######################

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

################### FILLSUSER  #####################

def createMaxBuckets(user, num, buckpref):
    myobj = getConnection(user)
    if myobj is None:
        print "Cannot get user obj"
    else:
        listBucketNum(myobj, "user")
    if len(myobj.get_all_buckets()) < num:
        whisper("Deleting all old buckets")
        cleanupUser(myobj, buckpref)
        whisper("Creating new buckets")
        for i in range(1, num + 1):
            name = buckpref + str(i)
            buck = myobj.create_bucket(name)
            for j in range(1, 11):
                k = Key(buck)
                k.key = name + '_OBJ_' + str(j)
                k.set_contents_from_string('Data for obj ' + str(j))

    return;

####################################################

############## CLEANUP AND LISTING #################

def cleanupUser(user, patstr):
    whisper("Cleaning up...")
    pstring = patstr + '*'
    pattern = re.compile(pstring)
    for bkt in user.get_all_buckets():
        if pattern.match(bkt.name):
            for k in bkt.list():
                whisper("Deleting " + str(k))
                k.delete()
            whisper("Deleting bucket " + str(bkt))
            user.delete_bucket(bkt.name)

    whisper("Attemting to list buckets for this user")
    for bkt in user.get_all_buckets():
        whisper("{name}\t{created}".format(name = bkt.name, created = bkt.creation_date))
    whisper("Done")
    return

def listBucketNum(userobj, uname):
    print "Total number of buckets for " + uname + ": " + str(len(userobj.get_all_buckets()))
    return

def listBucket(userobj, uname):
    print "Listing buckets for " + uname
    for bucket in userobj.get_all_buckets():
        print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)
    return
####################################################

############## KEEP CHANGING ACLS ##################

def keepChangingAcls(username, bucket):
    obj = dsslib.getConnection(username)
    acl_list = ('public-read', 'private')
    for i in range(1, 11):
        b1 = obj.get_bucket(bucket)
        whisper("Changing ACL to " + str(acl_list[i % 2]))
        b1.set_acl(acl_list[i % 2])
        time.sleep(1)
    return
####################################################
