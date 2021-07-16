import requests
from dotenv import load_dotenv
import hashlib
import os
from .auth_manager import AuthManager

from urllib import parse

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

load_dotenv()

GAMESERVER_URL = "https://pongconsole.xyz/dcauth/"
DEBUG_URL = "http://127.0.0.1:8000/dcauth/"

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

authmng = AuthManager()


class todoHome(TemplateView):
    def get(self, request, *args, **kwargs):

        return render(request, "index.html")


def login_via_discord(request):
    REDIRECT_URI = f"{GAMESERVER_URL}login-success"

    discord_auth_url = (
        "https://discord.com/api/oauth2/authorize?"
        + f"client_id={CLIENT_ID}&redirect_uri={parse.quote(REDIRECT_URI)}&response_type=code&scope=identify"
    )
    return redirect(discord_auth_url)


def login_success(request):
    if request.GET["code"] is not None:
        code = request.GET["code"]
        access_token = get_access_token(code)
        uid = get_user_id(access_token)
        authmng.add(uid)
    return render(request, "token.html", {"uid": authmng.get(uid)})


# Tools
def get_access_token(code):
    API_ENDPOINT = "https://discord.com/api"
    REDIRECT_URI = f"{GAMESERVER_URL}login-success"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(
        f"{API_ENDPOINT}/oauth2/token", data=parse.urlencode(data), headers=headers
    )
    r.raise_for_status()
    response = r.json()
    return response["access_token"]


def get_user_id(access_token):
    API_ENDPOINT = "https://discord.com/api"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(f"{API_ENDPOINT}/users/@me", headers=headers)
    r.raise_for_status()
    res = r.json()
    return res["id"]
