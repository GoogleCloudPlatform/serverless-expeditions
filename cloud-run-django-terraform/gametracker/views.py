from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import os

from .models import *


def home(request, game_name=None):

    filtered_game = None
    context = {}

    if settings.DEBUG:
        context["debug"] = (
            f'< DB_HOST="{settings.DATABASES["default"]["HOST"]}"'
            f'| PROXY="{os.environ.get("USE_CLOUD_SQL_AUTH_PROXY", "False")}"'
            f'| BUCKET="{settings.GS_BUCKET_NAME}" >'
        )

    context["game_name"] = game_name
    context["games"] = Game.objects.all().order_by("name")

    if game_name:
        search = Game.objects.filter(name__iexact=game_name)
        if len(search) == 1:
            filtered_game = search.get()
        else:
            context["error"] = f"Invalid game: {game_name}"

            return render(request, "index.html", context)

        context["matches"] = Match.objects.filter(game=filtered_game).order_by(
            "-datetime"
        )
    else:
        context["matches"] = Match.objects.all().order_by("-datetime")

    context["players"] = Player.objects.all().order_by("name")
    context["filtered_game"] = filtered_game

    winrates = []

    for player in context["players"]:
        if filtered_game:
            rate = player.winning_matches.filter(game=filtered_game).count() / player.matches.filter(game=filtered_game).count()
        else:
            rate = player.winning_matches.count() / player.matches.count()
        winrates.append({"player": player.name, "rate": f"{rate * 100}%" })

    context["winrates"] = winrates

    return render(request, "index.html", context)

