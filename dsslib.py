import boto
import boto.s3.connection
from boto.s3.key import Key
import re
import sys
###################### INIT ########################

# PARAMS
GLOBAL_DEBUG = 0
RADOSHOST = 's3-website-us-west-2.amazonaws.com'
RADOSPORT = 80
#RADOSHOST = '127.0.0.1'
#RADOSPORT = 7480

# USER PROFILES
USER_local1 = 0
USER_local2 = 1
USER_keystone1 = 2
USER_keystone2 = 3
USER_keystone3 = 4
USER_aws1 = 5

user_profiles = [
        {'access': 'INDCMF1YDM0N785EKCBN'            , 'secret': 'oxvVdSd1P3ICWlPyCehdco8h56OPqnyjtOtN52c4'}, ##Local user1
        {'access': 'EINGB4RLFBLPFLF2BFSJ'            , 'secret': 'cKsEUeHUD5GZzfDLbzxHBp3MVw6K2mwYSDrfjaIB'}, ##Local user2
        {'access': '842f26b29ddd4331a5af8fc800ce04ca', 'secret': 'b772c2bb2ad149fcb941d298e2dabfb5'},         ##admintenant user1
        {'access': 'cb92f272dc514e80acc782023c442c20', 'secret': 'd115d835aa2a4053a5d66bd93aea2046'},         ##admintenant user2
        {'access': '911093f31862430b955a6cdea71fee2e', 'secret': '31a3770da550495d99dcc065488e1351'},         ##roottenant  user1
    ]

####################################################

################## CREATE CONNECTION ###############

def getConnection(user):
    if user == USER_aws1:
        conn_obj = boto.connect_s3()
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

#################### CLEANUP #######################

def cleanupUser(user):
    whisper("Cleaning up...")
    pattern = re.compile('rjilshiv*')
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
####################################################
