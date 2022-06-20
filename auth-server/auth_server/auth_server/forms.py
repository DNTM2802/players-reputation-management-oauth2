from django import forms
from django.contrib.auth.forms import UserCreationForm

# Create your forms here.
from accounts.models import Player, TempPlayer


class NewPlayerForm(UserCreationForm):

    # Identifies the TempPlayer (Player that has completed phase 1 of registration process)
    id = forms.UUIDField(widget=forms.HiddenInput())

    class Meta:
        model = Player
        fields = ("username", "id", "password1", "password2")

    def save(self, commit=True):
        player = super(NewPlayerForm, self).save(commit=False)

        # If id is from a known TempPlayer, then both registration phases (CMD + credentials)
        # completed successfully, and so we can create a new Player
        if commit and TempPlayer.objects.filter(id=self.cleaned_data['id']).exists():
            tmp_player = TempPlayer.objects.get(id=self.cleaned_data['id'])
            player.nic = tmp_player.nic
            tmp_player.delete()  # TempPlayer is no longer needed
            player.save()
        return player


class Oauth2ImplicitTokenForm(forms.Form):
    oauth2_token = forms.CharField(label='token', widget=forms.HiddenInput(), max_length=100)
