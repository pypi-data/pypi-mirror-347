import hashlib
import json
import requests
import time
import uuid


class BaseService:
    OAUTH_SANDBOX_SERVER = "https://open.huolala.cn/{0}?isSandbox=true"
    OAUTH_PRODUCTION_SERVER = "https://open.huolala.cn/{0}?isSandbox=false"
    API_PRODUCT_SERVER = "https://openapi.huolala.cn/v1"
    API_SANDBOX_SERVER = "https://openapi-pre.huolala.cn/v1"
    OAUTH_AUTHORIZE = "oauth/authorize"
    OAUTH_TOKEN = "oauth/token"

    def __init__(self, config):
        self.api_version = "1.0"
        self.config = config
        self.access_token = ""

    def set_config(self, config):
        self.config = config
        return self

    def set_access_token(self, access_token):
        self.access_token = access_token
        return self

    def get_access_token(self):
        return self.access_token

    def get_app_key(self):
        return self.config.get("appKey", "")

    def get_app_secret(self):
        return self.config.get("appSecret", "")

    def get_api_service_url(self):
        return self.API_SANDBOX_SERVER if self.is_sandbox() else self.API_PRODUCT_SERVER

    def get_service_url(self):
        return (
            self.OAUTH_SANDBOX_SERVER
            if self.is_sandbox()
            else self.OAUTH_PRODUCTION_SERVER
        )

    def get_auth_url(self, redirect_url):
        oauth_url = self.get_service_url().format("#/" + self.OAUTH_AUTHORIZE)
        return f"{oauth_url}&response_type=code&client_id={self.get_app_key()}&redirect_uri={redirect_url}"

    def get_access_token_by_code(self, code, grant_type="authorization_code"):
        params = {
            "grant_type": grant_type,
            "client_id": self.get_app_key(),
        }
        if grant_type == "authorization_code":
            params["code"] = code
        elif grant_type == "password":
            params["auth_mobile"] = code  # password模式，code为授权手机号
        uri = "&".join([f"{k}={v}" for k, v in params.items()])
        oauth_url = f"{self.get_service_url().format(self.OAUTH_TOKEN)}&{uri}"
        print(f"URL: {oauth_url}")
        return self.https_request(oauth_url)

    def fresh_access_token(self, refresh_token):
        params = {
            "grant_type": "refresh_token",
            "client_id": self.get_app_key(),
            "refresh_token": refresh_token,
        }
        uri = "&".join([f"{k}={v}" for k, v in params.items()])
        oauth_url = f"{self.get_service_url().format(self.OAUTH_TOKEN)}&{uri}"
        print(f"URL: {oauth_url}")
        return self.https_request(oauth_url)

    def is_sandbox(self):
        return self.config.get("sandbox", False)

    def call_api(self, api_method, need_token=True, api_data=None):
        try:
            api_data = api_data or {}
            timestamp = int(time.time())
            req_params = {
                "app_key": self.get_app_key(),
                "timestamp": timestamp,
                "nonce_str": self.create_uuid(),
                "api_method": api_method,
                "api_version": self.api_version,
            }
            if api_data:
                req_params["api_data"] = json.dumps(api_data)
            if need_token:
                req_params["access_token"] = self.get_access_token()
            req_params["signature"] = self.create_signature(
                req_params, self.get_app_secret()
            )
            return self.https_request(self.get_api_service_url(), req_params)
        except Exception as e:
            return {
                "ret": e.__class__.__name__,
                "msg": str(e),
                "data": e.__traceback__,
            }

    @staticmethod
    def create_uuid(prefix=""):
        return prefix + str(uuid.uuid4())

    @staticmethod
    def create_signature(params, secret):
        sorted_params = sorted(params.items())
        str_to_sign = "".join(f"{k}={v}&" for k, v in sorted_params if v)[:-1] + secret
        return hashlib.md5(str_to_sign.encode("utf-8")).hexdigest().lower()

    @staticmethod
    def https_request(url, post_data=None, timeout=5):
        try:
            if post_data:
                response = requests.post(
                    url,
                    json=post_data,
                    timeout=timeout,
                    headers={"Content-Type": "application/json"},
                )
            else:
                response = requests.get(url, timeout=timeout)
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
