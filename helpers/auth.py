from helpers.config import getUrl

_HEADERS = {"User-Agent": "Kat"}

def login(config, session):
    username = config.get("user", "username")
    token = config.get("user", "token")
    login_url = getUrl(config, "loginurl", "login")

    session.post(
        login_url,
        data={"user": username, "token": token, "script": "true"},
        headers=_HEADERS,
    )