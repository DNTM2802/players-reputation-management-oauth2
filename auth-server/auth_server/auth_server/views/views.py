from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib import messages
from django.template.response import TemplateResponse

# Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

# OAuth2
from oauth2_provider.decorators import protected_resource
from oauth2_provider.models import AccessToken

# Forms
from ..forms import *

# Serializers
from ..serializers.serializers import playerReputationSerializer

# Utils
from ..utils.utils import pop_scopes


# HTML views

def register_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def home(request):
    return render(request=request, template_name="index.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                next_hop = request.GET.get("next", None)
                if next_hop:
                    return redirect(next_hop)
                else:
                    return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()

    return TemplateResponse(request, 'login.html', {"login_form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


# REST Views

@api_view(('GET', 'POST',))  # Only POST and GET allowed
@protected_resource()  # An access token (not expired) is required
@csrf_exempt  # Ignore CSRF tokens for POST requests
def rw_reputation(request):
    """
    Used by an OAuth2 client in order to read or write a player's reputation.
    The client can read a player's reputation doing a GET request and carrying
    OAuth2 token that provides a level N of anonymity, being N from 2 to 10 the
    read scope of the token (ex: read_3 for level 3).
    The client can write a player's reputation with a POST request and a JSON
    body containing integer values for the keys 'skill_update' and
    'behaviour_update'.
    The client can only read and write one time, therefore the correspondent scope
    of the provided token is removed upon it's first usage.

    :param request: web request
    :return: JSON response with HTTP status code 200, 400, 401 or 500
    """
    # Get OAuth2 token and player from it
    try:
        token_str = request.headers.get('Authorization').split(' ')[1]
        token = AccessToken.objects.get(token=token_str)
        player = token.user
    except Exception as e:
        return Response({'detail': 'Unknown server error.'}, status=500)

    # Read reputation
    if request.method == 'GET':

        # read_* scopes are required for GET requests, pop them from token
        popped_scopes = pop_scopes(token, "GET")
        if not popped_scopes:
            return Response({'detail': 'Unauthorized.'}, status=401)

        # Serialize reputation information
        return Response(playerReputationSerializer(player, popped_scopes))

    # Write reputation
    elif request.method == 'POST':

        # write scope is required for POST requests, pop it from token
        popped_scopes = pop_scopes(token, "POST")
        if not popped_scopes:
            return Response({'detail': 'Unauthorized.'}, status=401)

        # Check if body is JSON with reputation update
        if all(k in request.data for k in ('skill_update', 'behaviour_update')):
            try:
                player.skill += request.data['skill_update']
                player.behaviour += request.data['behaviour_update']
                player.save()
            except Exception as e:
                return Response({'detail': 'Could not update player\'s reputation.'}, status=500)
            return Response({'detail': 'Reputation updated.'}, status=200)
        else:
            return Response({'detail': 'Malformed reputation submitted.'}, status=400)
