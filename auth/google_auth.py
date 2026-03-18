import requests
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

def google_login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account"
    }

    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    return url


# ---------- GET USER INFO ----------
def get_user_info(code):

    # Step 1: exchange code for token
    token_url = "https://oauth2.googleapis.com/token"

    token_data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    token_response = requests.post(token_url, data=token_data)

    if token_response.status_code != 200:
        return None

    token_json = token_response.json()

    access_token = token_json.get("access_token")

    # Step 2: get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    user_response = requests.get(userinfo_url, headers=headers)

    if user_response.status_code != 200:
        return None

    user_info = user_response.json()

    return {
        "name": user_info["name"],
        "email": user_info["email"],
        "picture": user_info.get("picture")
    }


# ---------- LOGOUT ----------
def logout():

    st.query_params.clear()
