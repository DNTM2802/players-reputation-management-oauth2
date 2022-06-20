from django.views.decorators.csrf import csrf_exempt

# Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

# OAuth2
from oauth2_provider.decorators import protected_resource
from oauth2_provider.models import AccessToken
# Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Serializers
from auth_server.serializers.serializers import playerReputationSerializer

# Utils
from auth_server.utils.utils import pop_scopes


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
                player.skill += int(request.data['skill_update'])
                player.behaviour += int(request.data['behaviour_update'])
                player.save()
            except Exception as e:
                print(e)
                return Response({'detail': 'Could not update player\'s reputation.'}, status=500)
            return Response({'detail': 'Reputation updated.'}, status=200)
        else:
            return Response({'detail': 'Malformed reputation submitted.'}, status=400)
