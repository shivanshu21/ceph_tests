import dsslib
import math, os
from filechunkio import FileChunkIO
import sys

dsslib.GLOBAL_DEBUG = 1
dsslib.RADOSHOST = '127.0.0.1'
dsslib.RADOSPORT = 7480
CALLER = dsslib.USER_keystone1
#CALLER = dsslib.USER_aws1

############### MAX BUCKET LIMIT ###################

def bucketMaxNumber():
    obj = dsslib.getConnection(CALLER)
    print "Total number of buckets for the user: " + str(len(obj.get_all_buckets()))
    if len(obj.get_all_buckets()) != 1000:
        dsslib.whisper("Deleting all old buckets")
        dsslib.cleanupUser(obj)
        dsslib.whisper("Creating new buckets")
        for i in range(1, 1001):
            name = 'rjilshivanshubucket' + str(i)
            obj.create_bucket(name)

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
    obj = dsslib.getConnection(dsslib.USER_keystone3)
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

    dsslib.cleanupUser(obj)
    return result

####################################################

#################### CALL TESTS ####################

dsslib.callTest(bucketMaxNumber(), "Thousand bucket creation")
dsslib.callTest(multipartObjectUpload(), "Upload object in Multiparts")

####################################################
