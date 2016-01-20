import base64
import hashlib
import hmac
def get_signature(url, secret):
    msg = base64.urlsafe_b64decode(str(url))
    key = str(secret)
    signed = base64.encodestring(hmac.new(key, msg, hashlib.sha1).digest()).strip()
    return signed

_url = "/docsbuck002"
_secret = ""
sign = get_signature(_url, _secret)
print "Signature is: " + str(sign)
