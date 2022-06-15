from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from django.shortcuts import render, redirect

from django.contrib import messages

# Forms
from auth_server.forms import *

# Serializers
from auth_server.serializers.serializers import playerProfileSerializer


@login_required
def profile_view(request):
    """
    Allows a logged in player to interact with his personal reputation profile.
    The player can see his skill and behaviour rankings (with 0 anonymity), the
    total number of players enrolled, and has buttons to change his password or
    log out.

    :param request:
    :return:
    """
    skill_rank, behaviour_rank, total_players = playerProfileSerializer(request.user)

    return render(request=request, template_name="profile.html",
                  context={'skill_rank': skill_rank, 'behaviour_rank': behaviour_rank, 'total_players': total_players})


@login_required
def change_password_view(request):
    """
    Allows a logged in player to change his password, with the condition
    of being logged in with the CMD (external IdP).

    :param request:
    :return:
    """
    if request.user.auth_status != Player.AUTH_STATUS.CMD:
        messages.warning(request, "You need to login with CMD to change the password.")
        return redirect("profile")
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,
                             'Your password was successfully updated!',
                             extra_tags='alert-success')
            return redirect('profile')
    form = PasswordChangeForm(request.user)
    return render(request=request, template_name='change_password.html', context={'change_password_form': form})


@login_required
def logout_view(request):
    """
    Allows a logged in player to log out. Also changes the
    player state in the database to not authenticated.

    :param request:
    :return:
    """
    if request.user.is_authenticated:
        request.user.auth_status = Player.AUTH_STATUS.NULL
        request.user.save()
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("profile")
