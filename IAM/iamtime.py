import sys
import time
import pexpect
import threading
from datetime import datetime

################ PARAMS #####################

DEBUG           = 0
NUMBER_OF_TRIES = 1      # Time reported per thread is an average over how many tries
IS_SIGN_REQ     = True   # False implies token request
IAM_TOKEN       = ''     # In case of token request, provide a new token
DURATION        = 10     # Seconds
REQ_PER_SEC     = 30     # Requests per second
#############################################


#==============================
# DO NOT ALTER BELOW THIS LINE
#==============================

MAX_ROWS = DURATION * REQ_PER_SEC
TID_COUNTER = 0
threads = []
thread_response_times = [[0 for x in range(2)] for x in range(MAX_ROWS)]
threadLock = threading.Lock()
signreq = ''

if (IS_SIGN_REQ):
    signreq = "curl -s -X POST https://iam.ind-west-1.staging.jiocloudservices.com:35357/v3/sign-auth -H \"Content-Type: application/json\" -d '{\"credentials\": {\"access\": \"c312c8c23a9e45398003b256759cef05\", \"signature\": \"XLt82oXi5FCN02w48MhU3Idy5dE=\", \"token\": \"R0VUCgoKVHVlLCAwOSBGZWIgMjAxNiAxODoyNDo1MCBHTVQKL3JqaWxidWNrZXRzYW5pdHkxNDU1MDQyMjc2Lw==\", \"action_resource_list\": [{\"action\": \"jrn:jcs:dss:CreateBucket\", \"resource\": \"jrn:jcs:dss::Bucket:newb\", \"implicit_allow\": \"False\"}]}}'"
else:
    signreq = "curl -H \"X-Auth-Token: " + IAM_TOKEN + "\" https://iam.ind-west-1.staging.jiocloudservices.com:35357/v3/token-auth?action=jrn:jcs:dss:ListBucket&resource=jrn:jcs:dss::Bucket:*"

#========================
# MULTI THREADED REQUEST
#========================

def getsThreadId():
    global TID_COUNTER
    if (TID_COUNTER >= MAX_ROWS):
        print("Too many threads spawned for the array!!");
        sys.exit(0)
    val = TID_COUNTER
    TID_COUNTER += 1
    return val

def sendreq():
    start = datetime.now()
    child = pexpect.spawn(signreq, timeout=300)
    child.read()
    end = datetime.now()
    td = end - start
    return (td.total_seconds() * 1000)

class myThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        global thread_response_times
        global threadLock
        makeRequest(self.threadID)
        return

def makeRequest(tid):
    accum_time = 0
    for i in range (1, NUMBER_OF_TRIES + 1):
        accum_time += sendreq()
    if (DEBUG == 1):
        print("TID: " + str(tid) + " - Average time taken for " + str(NUMBER_OF_TRIES)
               + " curl responses: " + str(accum_time/NUMBER_OF_TRIES) + " milliseconds.")
    threadLock.acquire()
    thread_response_times[tid][0] = tid
    thread_response_times[tid][1] = accum_time/NUMBER_OF_TRIES
    threadLock.release()
    return

def prettyprint(p_str):
    print "\n\n================================"
    print "\t" + p_str
    print "================================"
    return

# Create new threads
for i in range(0, MAX_ROWS):
    id = getsThreadId()
    threads.append(myThread(id))

# Start new Threads
for t in threads:
    t.start()
    time.sleep(1.00 / REQ_PER_SEC)

# Wait for threads
for t in threads:
    t.join()

# Process data
resptime_l = sorted(thread_response_times, key=lambda x: x[1])
timeavg = 0
prettyprint("Average response time")
print("Total runtime: " + str(DURATION) + " seconds")

for i in range(0, MAX_ROWS):
    timeavg += resptime_l[i][1]
print "Average response time at " + str(REQ_PER_SEC) + " requests per second: " + str(timeavg/MAX_ROWS)

prettyprint("Five fastest responses")
for i in range (0, 5):
    print "TID=" + str(resptime_l[i][0]) + "\tTime=" + str(resptime_l[i][1]) + " milliseconds"

prettyprint("Five slowest responses")
for i in range (MAX_ROWS - 5, MAX_ROWS):
    print "TID=" + str(resptime_l[i][0]) + "\tTime=" + str(resptime_l[i][1]) + " milliseconds"

