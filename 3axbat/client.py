import requests
import urllib3
from .utils import encrypt_password, get_device, sign_request, to_json, pick_keys
from .exceptions import AuthenticationError, RateLimitError, NotFoundError, SignatureError
from .models import Profile, Friend

urllib3.disable_warnings()

class Client:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.token = None
        self.uid = None
        self.device, self.sign = get_device()
        self.base_url = "https://gw.sandboxol.com"

    def _request(self, method: str, path: str, params: dict = None, body: dict = None, auth: bool = True, use_dev: bool = False):
        params = params or {}
        body_str = to_json(body) if body else None
        
        # Login uses device=None for signature, other endpoints use self.device
        device = self.device if (auth or use_dev) else None
        ak, nonce, timestamp, signature = sign_request(path, params, body_str or '', device)
        
        headers = {
            'Host': 'gw.sandboxol.com',
            'os': 'android',
            'userdeviceid': self.device,
            'x-apikey': ak,
            'x-nonce': nonce,
            'x-time': timestamp,
            'x-sign': signature,
            'x-urlpath': path,
            'user-agent': 'okhttp/4.12.0'
        }
        
        if auth:
            headers.update({
                'userid': self.uid,
                'access-token': self.token,
                'manufacturer': '3AXBAT_LIB',
                'package_name_en': 'com.sandboxol.blockymods',
                'brand': '3AXBAT',
                'model': '3AXBAT_PY',
            })
            
        if body_str:
            headers['content-type'] = 'application/json; charset=UTF-8'
            
        q = '&'.join(f'{k}={v}' for k, v in sorted(params.items()))
        url = f'{self.base_url}{path}{f"?{q}" if q else ""}'
        
        try:
            r = self.session.request(method, url, headers=headers, data=body_str, timeout=15)
        except Exception as e:
            raise ConnectionError(f"Request failed: {e}")
        
        if r.status_code == 401:
            raise AuthenticationError("Unauthorized: Token expired or invalid.")
        if r.status_code == 403:
            raise AuthenticationError("Forbidden: Account banned or access denied.")
        if r.status_code == 404:
            raise NotFoundError("Resource not found.")
        if r.status_code == 429:
            raise RateLimitError("Rate limit exceeded.")
        if r.status_code != 200:
            raise Exception(f"HTTP Error {r.status_code}: {r.text}")
            
        try:
            resp = r.json()
        except:
            raise Exception(f"Invalid JSON response: {r.text}")

        # Check application-level errors
        if resp.get('code') == 6 or (resp.get('code') == 100001 and resp.get('message') == 'sign expired'):
            raise SignatureError("Signature expired. Check system time.")
        
        return resp

    def login(self, username: str, password: str) -> bool:
        """Logs into Blockman Go and retrieves the access token."""
        self.device, self.sign = get_device()
        encrypted_pw = encrypt_password(password)
        body = {'account': username, 'password': encrypted_pw, 'tsvAccount': '', 'tsvPlatform': '', 'tsvToken': ''}
        
        ak, nonce, timestamp, signature = sign_request('/user/api/v4/account/login', body=to_json(body), device=None)
        
        headers = {
            'Host': 'gw.sandboxol.com',
            'bmg-device-id': self.device,
            'bmg-sign': self.sign,
            'os': 'android',
            'apptype': '3AXBAT_LIB',
            'x-apikey': ak,
            'x-nonce': nonce,
            'x-time': timestamp,
            'x-sign': signature,
            'x-urlpath': '/user/api/v4/account/login',
            'content-type': 'application/json; charset=UTF-8',
            'user-agent': 'okhttp/4.12.0'
        }
        
        r = self.session.post(f'{self.base_url}/user/api/v4/account/login', headers=headers, json=body, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if data.get('code') == 1:
                self.token = data['data']['accessToken']
                self.uid = str(data['data']['userId'])
                return True
            else:
                raise AuthenticationError(f"Login failed: {data.get('message')}")
        raise AuthenticationError(f"HTTP Error {r.status_code}: {r.text}")

    def get_profile(self, user_id: str = None) -> Profile:
        """Retrieves profile information. Defaults to logged-in user."""
        if user_id:
            # Fetching other users' profiles uses a different endpoint
            resp = self._request('GET', f'/friend/api/v2/friends/{user_id}', params={'showBigParty': '1'})
        else:
            resp = self._request('GET', '/user/api/v3/user/details/info')
            
        if resp.get('code') == 1:
            return Profile.from_dict(resp.get('data', {}))
        raise Exception(f"Failed to get profile: {resp.get('message')}")

    def set_nickname(self, new_name: str) -> bool:
        """Changes the nickname of the logged-in user."""
        resp = self._request('PUT', '/user/api/v3/user/nickName', params={'newName': new_name, 'oldName': '3axbat'})
        if resp.get('code') == 1:
            return True
        raise Exception(f"Failed to set nickname: {resp.get('message')}")

    def set_description(self, text: str) -> bool:
        """Changes the description of the logged-in user."""
        if len(text) > 80:
            raise ValueError("Description too long (max 80 chars).")
        resp = self._request('PUT', '/user/api/v1/user/info', body={'details': text})
        if resp.get('code') == 1:
            return True
        raise Exception(f"Failed to set description: {resp.get('message')}")

    def get_friends(self) -> list[Friend]:
        """Retrieves the friend list of the logged-in user."""
        resp = self._request('GET', '/friend/api/v2/friends/status', params={'showBigParty': '1'})
        if resp.get('code') == 1:
            friends_data = resp.get('data', {}).get('status', [])
            return [Friend.from_dict(f) for f in friends_data]
        raise Exception(f"Failed to get friends: {resp.get('message')}")

    def send_friend_request(self, user_id: int, game_type: int = None) -> bool:
        """Sends a friend request to a user."""
        body = {'channel': 7, 'friendId': user_id, 'gameId': f'g{game_type}' if game_type else '', 'msg': '3axbat add', 'type': 1}
        resp = self._request('POST', '/friend/api/v1/friends', body=body, use_dev=True)
        if resp.get('code') == 1:
            return True
        raise Exception(f"Failed to send friend request: {resp.get('message')}")

    def get_game_server(self, game_type: int) -> str:
        """Retrieves the server IP:Port for a specific game type."""
        type_id = f'g{game_type}'
        # Note: This requires engine versions. Hardcoded fallback for now.
        eng1 = 10113 
        auth_resp = self._request('GET', '/game/api/v3/game/auth', params={'typeId': type_id, 'userId': self.uid, 'targetId': self.uid, 'gameVersion': eng1})
        
        if auth_resp.get('code') != 1:
            raise Exception("Game auth failed.")
            
        token = auth_resp['data']['token']
        disp = auth_resp['data']['dispUrl']
        region = auth_resp['data']['region']
        
        body = {'userId': int(self.uid), 'rid': region, 'ever': eng1, 'name': '3axbat'}
        bs = to_json(body)
        host = disp.split('//')[1].split(':')[0]
        
        ak, nonce, timestamp, signature = sign_request('/v1/dispatch', body=bs, device=self.device)
        headers = {
            'Host': host, 'x-shahe-uid': self.uid, 'x-shahe-token': token, 'userId': self.uid,
            'x-apikey': ak, 'x-nonce': nonce, 'x-time': timestamp, 'x-sign': signature,
            'x-urlpath': '/v1/dispatch', 'access-token': self.token,
            'Content-Type': 'application/json; charset=UTF-8', 'User-Agent': 'okhttp/4.12.0'
        }
        
        r = self.session.post(f"{disp}/v1/dispatch", headers=headers, data=bs, verify=False, timeout=15)
        if r.status_code == 200:
            resp = r.json()
            if resp.get('code') == 1:
                return resp['data'].get('gaddr', 'N/A')
        raise Exception("Failed to get game server.")