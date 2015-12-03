import dsslib
import math, os
from filechunkio import FileChunkIO
import sys
import time
from boto.s3.key import Key

dsslib.GLOBAL_DEBUG = 1
dsslib.RADOSHOST = '127.0.0.1'
dsslib.RADOSPORT = 7480
CALLER = dsslib.USER_keystone803

obj = dsslib.getConnection(CALLER)
dsslib.listBucketNum(obj, "user803")
##dsslib.listBucket(obj, "user803")
