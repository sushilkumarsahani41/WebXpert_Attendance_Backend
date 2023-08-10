import base64
from Crypt import Crypt
key = b'L\x80\xc1D\x80\x93|\xfb0\xbf\xef\x9d\x98\xd3l\xd5' 
url_safe_base64_data = "6pd4IE4Jh5rw7fvEV62Afw=="

# Convert URL-safe base64 to regular base64
base64_data = url_safe_base64_data.replace('-', '+').replace('_', '/')

# Decode base64 to get the original bytes
original_bytes_data = base64.b64decode(base64_data)

c = Crypt(key)

print(c.decrypt(original_bytes_data))


