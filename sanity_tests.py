import os
import sys
import time
import getopt
import dssSanityLib
from boto.s3.key import Key
from filechunkio import FileChunkIO

############### MAX BUCKET LIMIT ###################

def bucketSanity():

    ## Create five buckets
    dssSanityLib.whisper("Creating five test buckets and putting objects in them...")
    bucketpref = dssSanityLib.getsNewBucketName()
    dssSanityLib.createMaxBuckets(12, bucketpref)

    ## Bucket name conflict during creation
#    dssSanityLib.whisper("Trying to create a bucket with name conflict...")
#    userObj = dssSanityLib.getConnection()
#    buck_str = bucketpref + '1'
#    try:
#        b = userObj.create_bucket(buck_str)
#        print "Error: Unexpectedly created bucket " + buck_str
#        return -1
#    except:
#        print "Expected failure: " + str(sys.exc_info())

    ## Delete all buckets
    try:
        userObj = dssSanityLib.getConnection()
        dssSanityLib.whisper("Deleting the test buckets...")
        dssSanityLib.cleanupUser(userObj, bucketpref)
    except:
        print "Unexpected failure: " + str(sys.exc_info())
        return -1
    return 0

####################################################

############### MULTI PART UPLOAD ##################

def multipartObjectUpload():
    result = 0
    dssSanityLib.whisper("Making bucket and listing...")
    userObj = dssSanityLib.getConnection()
    bucketpref = dssSanityLib.getsNewBucketName()
    b = userObj.create_bucket(bucketpref)
    b.set_acl('public-read-write')
    dssSanityLib.listBucket(userObj, "User")

    source_path = MULTIPART_LARGE_FILE
    source_size = os.stat(source_path).st_size
    chunk_size = 5242880 ## 5 mb
    #chunk_size = 1048576  ## 1 mb
    chunk_count = int(math.ceil(source_size / float(chunk_size)))

    b1 = userObj.get_bucket(bucketpref)
    dssSanityLib.whisper("Got bucket: " + str(b1))
    try:
        mp = b1.initiate_multipart_upload(os.path.basename(source_path))
        for i in range(chunk_count):
            dssSanityLib.whisper("Uploading chunk: " + str(i))
            offset = chunk_size * i
            bytes = min(chunk_size, source_size - offset)
            with FileChunkIO(source_path, 'r', offset=offset, bytes=bytes) as fp:
                mp.upload_part_from_file(fp, part_num=i + 1)
        mp.complete_upload()
    except:
        print "Unexpected error during multipart upload: ", sys.exc_info()
        result = -1

    dssSanityLib.cleanupUser(userObj, bucketpref)
    return result

####################################################

#################### DNS TESTS ####################

def dnsNamesTest():
    userObj = dssSanityLib.getConnection()
    result = 0
    longHundredChars = 'a123456789a123456789a123456789a123456789a123456789a123456789a123456789a123456789a123456789a123456789'
    longFiftyChars = 'a123456789a123456789a123456789a123456789a123456789'
    longTFTchars = longHundredChars + longHundredChars + longFiftyChars + 'qwe'
    try:
        userObj.create_bucket(longTFTchars)
        userObj.delete_bucket(longTFTchars)
        print "Able to create bucket with 253 chars in name"
    except:
        print "Failed to create or delete a valid bucket name"
        print "Unexpected error: ", sys.exc_info()
        return -1

    try:
        badName = longTFTchars + 'abc'
        userObj.create_bucket(badName)
        print "Unexpectedly created bucket with illegally long name"
        dssSanityLib.listBucketNum(userObj, "user")
        dssSanityLib.listBucket(userObj, "user")
        userObj.delete_bucket(badName)
        result = -1
    except:
        print "Expected failure in creating 256 char bucket name"
        print "Expected error: ", sys.exc_info()

    try:
        badName = 'Abc'
        userObj.create_bucket(badName)
        print "Unexpectedly created bucket with capital letter name"
        dssSanityLib.listBucketNum(userObj, "user")
        dssSanityLib.listBucket(userObj, "user")
        userObj.delete_bucket(badName)
        result = -1
    except:
        print "Expected failure in creating bucket name with CAPS"
        print "Expected error: ", sys.exc_info()

    try:
        badName = 'bc/'
        userObj.create_bucket(badName)
        print "Unexpectedly created bucket with slash in name"
        dssSanityLib.listBucketNum(userObj, "user")
        dssSanityLib.listBucket(userObj, "user")
        userObj.delete_bucket(badName)
        result = -1
    except:
        print "Expected failure in creating bucket name with slash"
        print "Expected error: ", sys.exc_info()

    return result

####################################################

################ PUBLIC URL TESTS ##################

def publicUrlTest():
    result = 0
    userObj = dssSanityLib.getConnection()
    bucketpref = dssSanityLib.getsNewBucketName()
    b1 = userObj.create_bucket(bucketpref)
    print "Setting ACL on bucket"
    b1.set_acl('public-read')

    k = Key(b1)
    k.key = 'userObj1'
    k.set_contents_from_string('Data of URL object')
    print "Setting ACL on obj"
    k.set_acl('public-read')

    m = Key(b1)
    m.key = 'userObj1'
    urlname = m.generate_url(1000)
    print "\nThe userObj URL is: " + str(urlname)
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
    userObj.delete_bucket(bucketpref)
    print "Bucket deleted\n"

    return result

####################################################

###################### MAIN ########################

def main(argv):
    MULTIPART_LARGE_FILE = '/boot/initrd.img-3.16.0-55-generic' # Need a large file to upload in multiparts.
    dssSanityLib.GLOBAL_DEBUG = 1                               # The lib supresses debug logs by default. Override here.
    ##dssSanityLib.RADOSHOST = '127.0.0.1'                      # The lib points to DSS staging endpoint by default. Override here.
    ##dssSanityLib.RADOSPORT = 7480                             # The lib points to DSS staging endpoint by default. Override here.

    try:
        opts, args = getopt.getopt(argv,"a:s:h:i",["access-key=","secret-key=","ifile="])
    except getopt.GetoptError:
        printsHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printsHelp()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            try:
                import dsskeys
                dssSanityLib.has_incore_params = True
                dssSanityLib.access_key = dsskeys.access_key
                dssSanityLib.secret_key = dsskeys.secret_key
            except ImportError:
                print "Error: Failed to import dsskeys from file. Make sure that the file is present."
        else:
            if opt in ("-a", "--access-key"):
                dssSanityLib.has_incore_params = True
                dssSanityLib.access_key = arg
            elif opt in ("-s", "--secret-key"):
                print "Sending secret key using command line is unsafe. Use dsskeys file."
                print "Sleeping for 5 seconds before continuing..."
                time.sleep(5)
                dssSanityLib.secret_key = arg

    if (not dssSanityLib.has_incore_params):
        printsHelp()
        return -1

    ## TESTCASES
    #dssSanityLib.callTest(bucketSanity(), "Create buckets and objects then delete them")
    #dssSanityLib.callTest(multipartObjectUpload(), "Upload object in Multiparts")
    #dssSanityLib.callTest(dnsNamesTest(), "Check various DNS name rules")
    #dssSanityLib.callTest(publicUrlTest(), "Public URL test")

    ## Do cleanup
    userObj = dssSanityLib.getConnection()
    dssSanityLib.cleanupUser(userObj, 'rjilbucketsanity')
    return

def printsHelp():
    print "HELP"
    print "===="
    print 'sanity_tests.py {-a <Access Key> -s <Secret Key>} or {-i To read from dsskeys}'
    print 'sanity_tests.py {--access-key <Access Key> --secret-key <Secret Key>} or { --ifile To read from dsskeys}'
    print "\nDSSKEYS FILE"
    print "============"
    print "Make a file called dsskeys.py and put inside it:"
    print "    access_key = \'<value>\'"
    print "    secret_key = \'<value>\'"
    return

if __name__ == "__main__":
    main(sys.argv[1:])

####################################################
