import dsslib
import math, os
from filechunkio import FileChunkIO
import sys
import time
from boto.s3.key import Key

dsslib.GLOBAL_DEBUG = 1
dsslib.RADOSHOST = '127.0.0.1'
dsslib.RADOSPORT = 7480
CALLER = dsslib.USER_keystone800

obj = dsslib.getConnection(CALLER)
acl_list = ('public-read', 'private')
for i in range(1, 11):
    b1 = obj.get_bucket('rjil800bucket200010')
    print "Changing ACL to " + acl_list[i % 2]
    b1.set_acl(acl_list[i % 2])
    time.sleep(1)
