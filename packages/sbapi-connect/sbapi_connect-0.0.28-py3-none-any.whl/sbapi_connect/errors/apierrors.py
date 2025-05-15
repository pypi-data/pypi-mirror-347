class APIError(Exception):
    pass

class APIAuthError(APIError):
    pass

class APIConnectError(APIError):
    pass
