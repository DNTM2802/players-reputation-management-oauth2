from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from logger import Logger
from matchmaker.match_player import match_player

l = Logger()

# Create your views here.
from matchmaker.models import Player, Room, Game


def room(request, room_id):
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

    return redirect("https://localhost:8000/logout")


def match_manager(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        return
    except Room.DoesNotExist:
        return HttpResponseRedirect('/room/' + room_id)
