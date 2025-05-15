from .base.apibase       import APIBase, APISession
from .errors.apierrors   import APIError, APIAuthError, APIConnectError
from typing              import Optional

class Connect(APIBase):
    def __init__(self, username: str, password: str, otp: Optional[int] = None):
        """
        Connect to Servebolt's Admin area with your Servebolt username and password

        Parameters:
            - username: str             - Email address used when account was signed up
            - password: str             - Password chosen when account was signed up
            - otp_secret: (opt) str     - OTP secret to generate OTP code
        """

        self.credentials: dict[str, str | int] = {
            'username': username,
            'password': password
        }

        if otp: self._add_otp(otp)

        resp = self._session.post(self._base_url + '/auth/login', json=self.credentials)
        data = resp.json()

        self.mfa_required = data.get('error') == 'mfa_required'

        if resp.status_code == 200:
            self._account_data = data.get('data')
        elif resp.status_code == 403 and self.mfa_required:
            self._login_data = data
        else:
            raise APIConnectError(f"Connection failed: {resp.text} Response code: {resp.status_code}")

    def __mfa_challenge(self, mfa_token: str, otp: int) -> dict:
        json_payload = {'mfa_token': mfa_token, 'otp': otp}

        resp = self._session.post(
            self._base_url + '/auth/mfa/otp', 
            json=json_payload)
        resp.raise_for_status()
        data = resp.json().get('data')

        if data is not None:
            return data

        return {}

    def _add_otp(self, otp: int | str):
        self.credentials.update({'otp': int(otp)})
        self._otp_available = True
        self.__otp = int(otp)

    def login(self, otp: Optional[int | str] = None) -> dict:
        if otp: self._add_otp(otp)

        if self.mfa_required and not hasattr(self, '_otp_available'):
            otp_error_msg = f"MFA enabled for account {self.credentials.get('username')}: Missing OPT code"
            raise APIAuthError(otp_error_msg)
        elif self.mfa_required:
            mfa_token = self._login_data.get('mfa_token')
            data = self.__mfa_challenge(mfa_token, self.__otp)
        elif not self.mfa_required:
            data = self._account_data
        else:
            raise APIError("General login fail. Double check MFA and OTP")

        self.account_data = data
        return data

    def mfa_required_check(self) -> bool:
        return self.mfa_required

    def get_account_data(self) -> dict:
        return self.account_data

    def get_session(self) -> APISession:
        return self._session

    def get_login_data(self):
        return self._login_data
