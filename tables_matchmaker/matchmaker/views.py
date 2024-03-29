import random

import requests
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from logger import Logger
from matchmaker.match_player import match_player
from tables_matchmaker import settings

l = Logger()

# Create your views here.
from matchmaker.models import Player, Room, Game


def room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return redirect(settings.URL_USER_AGENT)

    player_id = request.COOKIES.get('player_id')
    if player_id:
        s = SessionStore(session_key=player_id)
        room = Room.objects.get(id=s['room'])
        return render(request, 'matchmaker/matchmake.html', {
            'room': room,
        })


def matchmake(request):
    player_id = request.COOKIES.get('player_id')
    global l
    if player_id:
        s = SessionStore(session_key=player_id)

        if s.has_key('skill_preference') and s.has_key('behaviour_preference') and s.has_key(
                'granularity_preference') and s.has_key('skill') and s.has_key('behaviour'):

            player = Player.objects.filter(player_id=player_id)
            if not Player.objects.filter(player_id=player_id).exists():
                player = Player()
                player.player_id = player_id
                player.skill = s['skill']
                player.behaviour = s['behaviour']
                player.skill_preference = s['skill_preference']
                player.behaviour_preference = s['behaviour_preference']
                player.granularity_preference = s['granularity_preference']
                player.game = Game.objects.get(name=s['game'])
                player.save()
            else:
                player = player[0]

            room_to_go = match_player(player)

            # found a match
            if room_to_go.match_ready:
                s['room'] = room_to_go.id
                s.save()
                s.modified = True
                response = HttpResponseRedirect(reverse('room', args=[room_to_go.id]))
                response.set_cookie('session_id', s.session_key)
                return response

            # didn't find match
            else:
                s['room'] = room_to_go.id
                s.save()
                s.modified = True
                response = HttpResponseRedirect(reverse('room', args=[room_to_go.id]))
                response.set_cookie('session_id', s.session_key)
                return response

    return redirect("http://localhost:8000/logout")


def match_manager(request):
    if request.method == "POST":
        try:
            room_id = request.GET.get('room_id', None)
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return redirect(settings.URL_USER_AGENT)

        if room.player_set.all().count() < 2:
            return HttpResponseRedirect('/room/' + room_id)

        players = list(room.player_set.all())
        random.shuffle(players)  # mix the players

        # winner -> first item of queryset
        # loser -> last item of queryset
        # other -> in between first and last item of queryset
        # no need to update the "others" because the default value is the correct one -> 0

        winner = players[0]
        winner.is_winner = 1
        winner.save()

        loser = players[-1]
        loser.is_winner = -1
        loser.save()

        cheaters = [random.randint(0, 1) for _ in range(len(players))]

        for player_index, player in enumerate(players):
            is_cheater = cheaters[player_index]
            if is_cheater == 1:
                player.is_cheater = -2
            player.save()

        room.player_set.set(players)
        room.save()

        data = {
            player.player_id: {'is_winner': player.is_winner, 'is_cheater': player.is_cheater}
            for player in room.player_set.all()
        }

        for player_id, player_values in data.items():
            player_session = SessionStore(session_key=player_id)

            access_token = player_session['access_token']

            update_reputations = requests.post(settings.URL_REPUTATION,
                                               data={"skill_update": player_values['is_winner'],
                                                     "behaviour_update": player_values[
                                                         'is_cheater']},
                                               headers={'Authorization': 'Bearer ' + access_token})
            if update_reputations.status_code != 200:
                # TODO: Error message??
                return redirect(settings.URL_USER_AGENT)

            # Remove session
            player_session.flush()

        return render(request, 'matchmaker/results.html', {
            'room': room,
        })

    if request.method == "GET":
        try:
            room_id = request.GET.get('room_id', None)
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return redirect(settings.URL_USER_AGENT)

        if room.player_set.all().count() < 2:
            return HttpResponseRedirect('/room/' + room_id)

        return render(request, 'matchmaker/results.html', {
            'room': room,
        })
