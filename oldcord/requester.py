import requests

class Requester:
    def __init__(self, ua, base_url):
        self.headers = {"User-Agent": ua}
        self.base_url = f"{base_url.rstrip('/')}/api/v6"
        self.session = requests.Session()
        self.session.cookies.update({
            "default_client_build": "october_5_2017",
            "enabled_patches": '["emojiAnywhere","modernizeWebRTC"]',
            "legal_agreed": "true",
            "locale": "en-US",
            "debug_mode": "true",
            "enabled_plugins": '["changeURLs","httpInLocal","noTrack","replaceDiscordText"]',
            "release_date": "october_5_2017"
        })

    def _url(self, endpoint):
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _addToken(self, token):
        self.headers["Authorization"] = f"Bot {token}"

    def POST(self, endpoint, data):
        return self.session.post(self._url(endpoint), json=data, headers=self.headers)

    def GET(self, endpoint):
        return self.session.get(self._url(endpoint), headers=self.headers)

    def PATCH(self, endpoint, data):
        return self.session.patch(self._url(endpoint), json=data, headers=self.headers)

    def DELETE(self, endpoint):
        return self.session.delete(self._url(endpoint), headers=self.headers)

    def PUT(self, endpoint, data):
        return self.session.put(self._url(endpoint), json=data, headers=self.headers)
