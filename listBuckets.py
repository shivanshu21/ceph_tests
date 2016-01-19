#!/bin/python
import dssSanityLib
from boto.s3.key import Key

dssSanityLib.GLOBAL_DEBUG = 1

obj = dssSanityLib.getConnection()
dssSanityLib.listBucketNum(obj, "user")
dssSanityLib.listBucket(obj, "user")
