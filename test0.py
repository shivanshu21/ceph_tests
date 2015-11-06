import dsslib

dsslib.GLOBAL_DEBUG = 1

obj = dsslib.getConnection(dsslib.USER_aws1)
##obj = dsslib.getConnection(dsslib.USER_keystone1)
print "User: " + str(obj)
print obj.get_all_buckets()
print obj.create_bucket('rjilshivanshuautoq')
print obj.create_bucket('rjilshivanshuautow')
print obj.create_bucket('rjilshivanshuautoe')
print obj.create_bucket('rjilshivanshuautor')
print obj.create_bucket('rjilshivanshuautot')
print obj.create_bucket('rjilshivanshuautoy')
print obj.get_all_buckets()
dsslib.cleanupUser(obj)
