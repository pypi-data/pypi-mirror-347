from requests import Session

class APISession(Session):
    pass

class APIBase:
    _base_url = 'https://api.servebolt.io/v1'
    _application_json = 'application/json'
    _headers = {'Content-Type': _application_json, 'Accept': _application_json}
    
    _session = APISession()
    _session.headers.update(_headers)

    def close_session(self):
        """
        Closes the API HTTP session
        """
        try:
            self._session.close()
        except Exception as e:
            raise Exception(e)
