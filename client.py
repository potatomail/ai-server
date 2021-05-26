import requests

class APIError(Exception):
    pass

class AIServerBackend:
    def __init__(self, host, api_key, port):
        self.host = host
        self.api_key = api_key
        self.port = port

        self._session = requests.Session()
        self.session.headers.update({'X-Api-Key': api_key})

    def _raise_for_status(self, r):
        if not r.ok:
            msg = ''
            try:
                msg = r.json()['error']
            except:
                r.raise_for_status()
            raise APIError(msg)

    def _url(self, path):
        return 'http://%s:%d%s' % (self.host, self.port, path)
