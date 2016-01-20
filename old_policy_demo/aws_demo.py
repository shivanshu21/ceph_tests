import dsslib
import math, os
from filechunkio import FileChunkIO
import sys
import time
from boto.s3.key import Key
from termcolor import colored
dsslib.GLOBAL_DEBUG = 1

def u1print(text):
    print colored("U1: "+text, "blue")
    return

def u2print(text):
    print colored("U2: "+text, "green")
    return

#=======================================
def crBucket():
    u1Obj = dsslib.getConnection(dsslib.USER_aws1)
    try:
        u1print("Creating bucket in my own tenant")
        u1Obj.create_bucket('shivanshu21demobucket1')
        dsslib.createMaxBuckets(dsslib.USER_aws1, 10, 'shivanshu21demobucket1')
        u1print("Created bucket!")
    except:
        u1print("Failed to create bucket: " + str(sys.exc_info()))
    return
#=======================================

def u1Bucket():
    u2Obj = dsslib.getConnection(dsslib.USER_aws2)
    BUCKET = 'shivanshu21demobucket1'
    u2print("\nTrying to get bucket of my own tenant")
    try:
        u2b = u2Obj.get_bucket(BUCKET)
        u2print("Got bucket!")
        for k in u2b.list():
            u2print("Object: " + str(k))
    except:
        u2print("Failed to get bucket: " + str(sys.exc_info()))
    return
#=======================================

def vishalBucket():
    u2Obj = dsslib.getConnection(dsslib.USER_aws2)
    BUCKET = 'shivanshubucketman00' ## In Vishal tenant<<<<<<<<<<
    u2print("Trying to get bucket in diff tenant")
    try:
        u2b = u2Obj.get_bucket(BUCKET)
        u2print("Got bucket!")
        for k in u2b.list():
            u2print("Object: " + str(k))
    except:
        u2print("Failed to get bucket: " + str(sys.exc_info()))
    return
#=======================================

def writeVishalBucket():
    u2Obj = dsslib.getConnection(dsslib.USER_aws2)
    u2print("Putting objects in Vishals bucket")
    dsslib.createMaxBuckets(dsslib.USER_aws2, 10, 'shivanshubucketman00')
    u2b = u2Obj.get_bucket('shivanshubucketman00')
    k = Key(u2b)
    k.key = 'shivanshubucketman00_OBJ_2'
    k.set_acl('public-read')
    return
#=======================================

def localPrivateBucket():
    loc1 = dsslib.getConnection(dsslib.USER_keystone803)
    b1 = loc1.create_bucket('shivanshudemo001')
    dsslib.createMaxBuckets(dsslib.USER_keystone803, 10, 'shivanshudemo001')
    b1.set_acl('private')
    loc2 = dsslib.getConnection(dsslib.USER_keystone804)
    b2 = loc2.get_bucket('shivanshudemo001')
    print b2.list()
    return
#=======================================

#crBucket()
#u1Bucket()
#vishalBucket()
#writeVishalBucket()
#localPrivateBucket()

u2Obj = dsslib.getConnection(dsslib.USER_aws2)



'''
obj = dsslib.getConnection(dsslib.USER_aws3)
bb = obj.get_bucket('shivanshubucketman00')
for k in bb.list():
    u1print(str(k.get_acl()))

pers3 = dsslib.getConnection(dsslib.USER_aws4)
#pers3.create_bucket('shivanshubucketauto99')
#pers3.create_bucket('shivanshubucketauto98')
pers3.delete_bucket('shivanshubucketauto99')
pers3.delete_bucket('shivanshubucketauto98')
'''
