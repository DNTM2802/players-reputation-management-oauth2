from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

# Rest Framework
from rest_framework.response import Response

# Forms
from auth_server.forms import *

# Utils
from auth_server.utils.utils import retrieve_and_transform_resource


def register_cmd_view(request):
    """
    Player registration phase 1 (external IdP).
    Redirects the user to the external IdP in order to start the
    registration process.

    :param request:
    :return: HttpResponseRedirect to external IdP
    """
    if request.method == "GET":
        return HttpResponseRedirect(
            redirect_to='https://preprod.autenticacao.gov.pt/oauth/askauthorization?redirect_uri=http://127.0.0.1:8000/register_cmd_callback&client_id=9113170755799990166&scope=http://interop.gov.pt/MDC/Cidadao/NIC&response_type=token')


def register_cmd_callback_view(request):
    """
    Endpoint to which the external IdP sends the access token.
    As the external IdP uses Oauth2 implicit flow, this endpoint
    renders a form and a piece of JavaScript code. The JavaScript
    code retrieves the access token from the URL hash, places it
    in the form and submits the form. The token is then retrieved
    from the form and a request to the external protected resource
    is performed. This resource wil allow the creation of a TempPlayer,
    which will be assigned a random ID. The registration process continues
    with a request to the register_credentials endpoint. This request
    carries a cookie containing the TempPlayer ID, and a csrf token
    mechanism to prevent forgery.

    :param request:
    :return:
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Oauth2ImplicitTokenForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # Retrieve nic from external IdP with provided oauth2 token
            user_nic_pbkdf2 = retrieve_and_transform_resource(form.cleaned_data.get('oauth2_token'))
            if user_nic_pbkdf2 is None:
                messages.error(request, "Invalid token.")
                return redirect("profile")

            # Can't register if already registered
            if Player.objects.filter(nic=user_nic_pbkdf2).exists():
                messages.error(request, "The provided user is already registered.")
                return redirect("profile")

            # Create a TempPlayer (but delete possible older entries first)
            delete_qs = TempPlayer.objects.filter(nic=user_nic_pbkdf2)
            if delete_qs:
                delete_qs.delete()

            tmp_player = TempPlayer()
            tmp_player.nic = user_nic_pbkdf2
            tmp_player.save()

            # Redirect TempPlayer to the credentials form with a cookie with his temporary id
            # The cookie will later be able to identify the TempPlayer which the form was given to
            response = HttpResponseRedirect('/register_credentials/')
            response.set_cookie('user_id', tmp_player.id)
            return response

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Oauth2ImplicitTokenForm()

    return render(request=request, template_name="oauth2token.html", context={"oauth2_form": form})


def register_credentials_view(request):
    """
    Player registration phase 2 (credentials).
    View that renders the registration of the player's credentials, after
    a successfully retrieving of identification from the external IdP.
    This view is only showed if the request carries a cookie that identifies
    a user (TempPlayer) that completed the registration phase 1.
    If this phase is completed successfully, a new Player is registered in the
    system.

    :param request:
    :return: redirect to user profile.
    """
    if request.method == "POST":
        form = NewPlayerForm(request.POST)
        if form.is_valid():  # Already checks for 'id' aka cookie
            player = form.save()

            # Update authentication status
            player.auth_status = Player.AUTH_STATUS.CMD
            player.save()

            login(request, player)
            messages.success(request, "Registration successful.")
            return redirect("profile")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return redirect("profile")

    # TempPlayer asking for a credentials form (registration phase 2)
    cookie = request.COOKIES.get('user_id')

    # Pursue registration only if TempPlayer cookie is set! Otherwise, the TempPlayer can not be recognized.
    if cookie:
        form = NewPlayerForm(initial={'id': cookie})
        request.COOKIES.pop('user_id')  # TempUser cookie no longer needed
        return render(request=request, template_name="register.html", context={"register_form": form})
    messages.error(request, 'Something went wrong! Restart the registration process.')
    return redirect("profile")


def login_view(request):
    """
    View that allows player authentication via credentials.
    Every non-authenticated request that tries to access protected
    endpoints ends up here.

    :param request:
    :return: Login form or player profile page.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:

                # Update authentication status
                user.auth_status = Player.AUTH_STATUS.CREDENTIALS
                user.save()

                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                next_hop = request.GET.get("next", None)
                if next_hop:
                    return redirect(next_hop)
                else:
                    return redirect("profile")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def login_cmd_view(request):
    """
    Redirects the user to the external IdP in order to retrieve its
    external identification.

    :param request:
    :return: HttpResponseRedirect to external IdP
    """
    if request.method == "GET":
        return HttpResponseRedirect(
            redirect_to='https://preprod.autenticacao.gov.pt/oauth/askauthorization?redirect_uri=http://127.0.0.1:8000/accounts/login_cmd_callback&client_id=9113170755799990166&scope=http://interop.gov.pt/MDC/Cidadao/NIC&response_type=token')


def login_cmd_callback_view(request):
    """
    Endpoint to which the external IdP sends the access token.
    As the external IdP uses Oauth2 implicit flow, this endpoint
    renders a form and a piece of JavaScript code. The JavaScript
    code retrieves the access token from the URL hash, places it
    in the form and submits the form. The token is then retrieved
    from the form and a request to the external protected resource
    is performed. If this resource (nic) allows the identification
    of a valid Player, the player is logged in.

    :param request:
    :return:
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Oauth2ImplicitTokenForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # Retrieve nic from external IdP with provided oauth2 token
            user_nic_pbkdf2 = retrieve_and_transform_resource(form.cleaned_data.get('oauth2_token'))
            if user_nic_pbkdf2 is None:
                return Response({'detail': 'Invalid token.'}, status=401)

            # Login user using CMD nic
            user = Player.objects.filter(nic=user_nic_pbkdf2).first()
            if user is not None:

                # Update authentication status
                user.auth_status = Player.AUTH_STATUS.CMD
                user.save()

                login(request, user)
                messages.info(request, f"You are now logged in as {user.username}.")
                next_hop = request.GET.get("next", None)
                if next_hop:
                    return redirect(next_hop)
                else:
                    return redirect("profile")
            else:
                messages.error(request, "Invalid user.")
                return redirect("profile")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Oauth2ImplicitTokenForm()

    return render(request=request, template_name="oauth2token.html", context={"oauth2_form": form})
