import random
import time
import hashlib
import base64
import re
import json
import requests
import urllib3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

urllib3.disable_warnings()

# Extracted RSA Public Key for password encryption
PUB_KEY_PEM = b"-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCLzlsA+3wXCAph80r/xs1bWhVrsJSOQmSBTA0GaBpVIzXqFBaibDmYA3WJDM9rcQ7KpYSyrJ02iFlsN43RnizrHfS+xPtdwuxBQ2Clow5cYPZucqQYL9HIlbBLoighH2eGQqGlVadL7r384iKTz9mmckSUa8hhJzS+WwUAqVO3DwIDAQAB\n-----END PUBLIC KEY-----"

# Extracted API Key Pairs
KEY_PAIRS = [
    ("6aDtpIdzQdgGwrpP6HzuPA", "9EuDKGtoWAOWoQH1cRng-d5ihNN60hkGLaRiaZTk-6s"),
    ("h0jCHbhVd9Fpkx-FGkxeRw", "lOTB7DNdMMpdyUO-psJ5b2ivYGmU5RAy6j6bkpoMYcs"),
    ("dM9XM3sxjfVI6AC77GS9rw", "6aNQVhd8pP-Gg7_xM2PTEp92G-77tzHGnPKrwslxmAg")
]

DEFAULT_DEVICE_ID = "E0-8F-4C-8D-E2-1C"
DEFAULT_BMG_SIGN = "xEGRkZHZJbCH+27N+LBJxktf57OrioeTvwcAUumrFhQ="

def md5(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()

def rand_hex(length: int) -> str:
    return ''.join(random.choices('0123456789abcdef', k=length))

def encrypt_password(password: str) -> str:
    key = RSA.import_key(PUB_KEY_PEM)
    cipher = PKCS1_v1_5.new(key)
    return base64.b64encode(cipher.encrypt(password.encode())).decode()

def pick_keys():
    return random.choice(KEY_PAIRS)

def to_json(obj) -> str:
    return json.dumps(obj, separators=(',', ':'))

def fetch_device_list():
    try:
        r = requests.get(
            'https://pastebin.com/raw/m4EZm0z5', 
            headers={'User-Agent': 'vse.taki.wizard', 'Host': 'pastebin.com'}, 
            verify=False, 
            timeout=10
        )
        if r.status_code != 200: return []
        pattern = r'{"device":\s*"([^"]+)",\s*"signature":\s*"([^"]+)"}'
        return re.findall(pattern, r.text)
    except:
        return []

def get_device():
    devices = fetch_device_list()
    if devices:
        return random.choice(devices)
    return DEFAULT_DEVICE_ID, DEFAULT_BMG_SIGN

def sign_request(path: str, params: dict = None, body: str = None, device: str = None, ak: str = None, sk: str = None):
    params = params or {}
    body = body or ''
    if ak is None or sk is None:
        ak, sk = pick_keys()
    
    nonce = rand_hex(32)
    timestamp = str(int(time.time()))
    param_str = '&'.join(f'{k}={params[k]}' for k in sorted(params))
    
    base = ak + path + nonce + timestamp + param_str + body + sk
    first_hash = md5(base)
    final_hash = md5(first_hash + device) if device else first_hash
    
    return ak, nonce, timestamp, final_hash