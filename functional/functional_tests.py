import dsslib
import math, os
from filechunkio import FileChunkIO
import sys
import time
from boto.s3.key import Key

dsslib.GLOBAL_DEBUG = 1
dsslib.RADOSHOST = '127.0.0.1'
dsslib.RADOSPORT = 7480
CALLER = dsslib.USER_keystone3
#CALLER = dsslib.USER_aws1

############### MAX BUCKET LIMIT ###################

def bucketMaxNumber():
    obj = dsslib.getConnection(dsslib.USER_keystone995)
    #dsslib.createMaxBuckets(dsslib.USER_keystone1,   1000, 'rjilshivanshubucket')
    dsslib.createMaxBuckets(dsslib.USER_keystone800, 1000, 'rjil800bucket')
    #dsslib.createMaxBuckets(dsslib.USER_keystone801, 1000, 'rjil801bucket')
    #dsslib.createMaxBuckets(dsslib.USER_keystone802, 1000, 'rjil802bucket')
    #dsslib.createMaxBuckets(dsslib.USER_keystone803, 1000, 'rjil803bucket')

    ## Make 1001 bucket
    try:
        obj.create_bucket('brandnewshinybucket')
        print "Bucket created unexpectedly!!"
        print "1001th bucket"
        return -1
    except:
        dsslib.whisper("\nExpected failure: " + str(sys.exc_info()) + "\n")

    ## Delete one bucket and try again
    try:
        dsslib.whisper("Deleting a bucket")
        obj.delete_bucket('rjilshivanshubucket100')
        dsslib.whisper("Creating one more bucket")
        obj.create_bucket('rjilshivanshubucket100')
    except:
        print "Unexpected failure. Cannot create bucket after deleting one: " + str(sys.exc_info())
        return -1
    return 0
'''
    ## Delete one bucket but have bucket name conflict
    try:
        dsslib.whisper("Deleting one more bucket")
        obj.delete_bucket('rjilshivanshubucket200')
        dsslib.whisper("Creating bucket with name conflict")
        obj.create_bucket('rjilshivanshubucket201')
        print "Bucket created unexpectedly even after name conflict!!"
        return -1
    except:
        dsslib.whisper("\nExpected failure: " + str(sys.exc_info()))
        obj.create_bucket('rjilshivanshubucket200')
'''
####################################################

############### MULTI PART UPLOAD ##################

def multipartObjectUpload():
    result = 0
    obj = dsslib.getConnection(CALLER)
    dsslib.whisper("Making bucket and listing...")
    obj.create_bucket('rjilshivanshuautoq')
    dsslib.whisper(str(obj.get_all_buckets()))

    source_path = '/boot/initrd.img-3.16.0-30-generic'
    source_size = os.stat(source_path).st_size
    chunk_size = 5242880 ## 5 mb
    #chunk_size = 1048576  ## 1 mb
    #chunk_size  = 2100000
    chunk_count = int(math.ceil(source_size / float(chunk_size)))

    b1 = obj.get_bucket('rjilshivanshuautoq')
    dsslib.whisper("Got bucket: " + str(b1))
    try:
        mp = b1.initiate_multipart_upload(os.path.basename(source_path))
        for i in range(chunk_count):
            dsslib.whisper("Uploading chunk: " + str(i))
            offset = chunk_size * i
            bytes = min(chunk_size, source_size - offset)
            with FileChunkIO(source_path, 'r', offset=offset, bytes=bytes) as fp:
                mp.upload_part_from_file(fp, part_num=i + 1)
        mp.complete_upload()
    except:
        print "Unexpected error: ", sys.exc_info()
        result = -1

    dsslib.cleanupUser(obj, 'rjilshiv')
    return result

####################################################

#################### DNS TESTS ####################

def dnsNamesTest():
    obj = dsslib.getConnection(CALLER)
    result = 0
    longHundredChars = 'a123456789a123456789a123456789a123456789a123456789a123456789a123456789a123456789a123456789a123456789'
    longFiftyChars = 'a123456789a123456789a123456789a123456789a123456789'
    longTFTchars = longHundredChars + longHundredChars + longFiftyChars + 'qwe'
    try:
        obj.create_bucket(longTFTchars)
        obj.delete_bucket(longTFTchars)
        print "Able to create bucket with 253 chars in name"
    except:
        print "Failed to create or delete a valid bucket name"
        print "Unexpected error: ", sys.exc_info()
        return -1

    try:
        badName = longTFTchars + 'abc'
        obj.create_bucket(badName)
        print "Unexpectedly created bucket with illegally long name"
        dsslib.listBucketNum(obj, "user3")
        dsslib.listBucket(obj, "user3")
        obj.delete_bucket(badName)
        result = -1
    except:
        print "Expected failure in creating 256 char bucket name"
        print "Expected error: ", sys.exc_info()

    try:
        badName = 'Abc'
        obj.create_bucket(badName)
        print "Unexpectedly created bucket with capital letter name"
        dsslib.listBucketNum(obj, "user3")
        dsslib.listBucket(obj, "user3")
        obj.delete_bucket(badName)
        result = -1
    except:
        print "Expected failure in creating bucket name with CAPS"
        print "Expected error: ", sys.exc_info()

    try:
        badName = 'bc/'
        obj.create_bucket(badName)
        print "Unexpectedly created bucket with slash in name"
        dsslib.listBucketNum(obj, "user3")
        dsslib.listBucket(obj, "user3")
        obj.delete_bucket(badName)
        result = -1
    except:
        print "Expected failure in creating bucket name with slash"
        print "Expected error: ", sys.exc_info()

    return result

####################################################

################ PUBLIC URL TESTS ##################

def publicUrlTest():
    result = 0
    obj = dsslib.getConnection(CALLER)
    b1 = obj.create_bucket('urlbucket1')
    k = Key(b1)
    k.key = 'obj1'
    k.set_contents_from_string('Data of URL object')
    print "Setting ACL on obj"
    k.set_acl('public-read')
    print "Setting ACL on bucket"
    b1.set_acl('public-read')

    m = Key(b1)
    m.key = 'obj1'
    urlname = m.generate_url(1000)
    print "\nThe obj URL is: " + str(urlname)
    urlname = b1.generate_url(1000)
    print "\nThe bucket URL is: " + str(urlname)

    for i in range(1, 21):
        time.sleep(1)
        if i % 5 == 0:
            print str(20 - i) + " Seconds left before Obj deletion"

    m.delete()
    print "Object deleted\n"

    for i in range(1, 21):
        time.sleep(1)
        if i % 5 == 0:
            print str(20 - i) + " Seconds left before bucket deletion"

    obj.delete_bucket('urlbucket1')
    print "Bucket deleted\n"
    return result

####################################################

#################### CALL TESTS ####################

##dsslib.callTest(bucketMaxNumber(), "Thousand bucket creation")
##dsslib.callTest(multipartObjectUpload(), "Upload object in Multiparts")
##dsslib.callTest(dnsNamesTest(), "Check various DNS name rules")
dsslib.callTest(publicUrlTest(), "Public URL test")
####################################################
