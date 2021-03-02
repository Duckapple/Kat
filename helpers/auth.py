from helpers.config import getConfig, getConfigUrl

_HEADERS = {"User-Agent": "Kat"}

def login(session):
    config = getConfig()
    user = config.get("user", {})
    username = user.get("username")
    token = user.get("token")
    login_url = getConfigUrl("loginurl", "login")

    session.post(
        login_url,
        data={"user": username, "token": token, "script": "true"},
        headers=_HEADERS,
    )