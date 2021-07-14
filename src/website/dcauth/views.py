from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

gameserver_url = "https://pongconsole.xyz/"
discord_auth_url = "https://discord.com/api/oauth2/authorize?client_id=864848740387782666&redirect_uri=https%3A%2F%2Fpongconsole.xyz%2F&response_type=code&scope=identify"


class todoHome(TemplateView):
    def get(self, request, *args, **kwargs):

        return render(request, "index.html")


def login_via_discord(request):
    return redirect(discord_auth_url)
