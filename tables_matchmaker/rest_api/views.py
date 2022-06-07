from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from tables_matchmaker import settings


@api_view(['GET'])
def play_game(request):
    if request.method == "GET":
        typegame = request.GET.get("game", None)
        return HttpResponse(settings.URL_AUTHORIZE)
    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def exchange(request):
    if request.method == "GET":
        auth_code = request.GET.get("code", None)
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET

        url = 'https://www.w3schools.com/python/demopage.php'
        myobj = {'somekey': 'somevalue'}

        x = requests.post(url, data=myobj)
        print(x)
        # return HttpResponse(status=status.HTTP_200_OK)
        return HttpResponseRedirect(redirect_to='http://google.com/')

    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
