import requests
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

from logger import Logger
from tables_matchmaker import settings

l = Logger()


@api_view(['GET'])
def play_game(request):
    """Redirects to authorization server.

    Args:
        game: the game the player intends to queue up to play.
        skill: skill preference of the player's opponent.
        behaviour: behaviour preference of the player's opponent.
        granularity: dilution of the reputation (2 (most diluted) -> 10 (least diluted))

    Returns:
        400: if the request is not GET.
        401: if the arguments are not present in the request.
        redirect: if all is correct redirects to authorization server sending over only granularity
    """

    request.session.flush()

    if request.method == "GET":

        game = request.GET.get("game", None)
        skill = request.GET.get("skill", None)
        behaviour = request.GET.get("behaviour", None)
        granularity = request.GET.get("granularity", None)

        if not (game and skill and behaviour and granularity):
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

        request.session['game'] = game

        request.session['skill_preference'] = skill
        request.session['behaviour_preference'] = behaviour
        request.session['granularity_preference'] = granularity
        request.session.save()
        request.session.modified = True
        return HttpResponseRedirect(redirect_to=settings.URL_AUTHORIZE + f'&scope=read_{granularity}%20write')

    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def exchange(request):
    if request.method == "GET":
        code = request.GET.get("code", None)
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET

        token = requests.post(settings.URL_TOKEN,
                              data={"client_id": client_id, "client_secret": client_secret,
                                    "grant_type": "authorization_code",
                                    "code": code})

        token = token.json()['access_token']
        request.session['access_token'] = token

        reputation = requests.get(settings.URL_REPUTATION, headers={'Authorization': 'Bearer ' + token})

        reputation = reputation.json()

        request.session['skill'] = reputation['skill']
        request.session['behaviour'] = reputation['behaviour']

        response = HttpResponseRedirect(
            redirect_to=f"http://localhost:8002/matchmake")
        response.set_cookie('player_id', request.session.session_key)

        return response

        # for key, value in request.session.items():
        #     print(' >>>>> {} => {}'.format(key, value))

    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
