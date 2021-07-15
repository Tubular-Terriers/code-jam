from urllib import parse

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

gameserver_url = "https://pongconsole.xyz/"

client_id = "864835657091252234"
redirect_uri = parse.quote(f"{gameserver_url}login-success", safe="")

discord_auth_url = (
    "https://discord.com/api/oauth2/authorize?"
    + f"client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=identify"
)


class todoHome(TemplateView):
    def get(self, request, *args, **kwargs):

        return render(request, "index.html")


def login_via_discord(request):
    return redirect(discord_auth_url)
