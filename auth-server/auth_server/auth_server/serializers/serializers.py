import math
from accounts.models import Player


def playerReputationSerializer(player, popped_scopes):
    """
    Used to provide a client with the skill and behaviour (reputation)
    of a player with a level N of anonymity, which is carried by the read_N
    token scope.

    :param player: player model
    :param popped_scopes: carries read_N scope
    :return: Dictionary with anonymized skill and behaviour
    """
    # Get protected attributes
    player_skill = player.skill
    player_behaviour = player.behaviour

    # Get anonymity authorized by the user (from token scope read_N)
    n_of_bins = int(popped_scopes[0].split('_')[1])

    # Limit user desired anonymity if it compromises other players anonymity
    total_players = Player.objects.filter(is_superuser=0).count()
    if total_players < 20:
        n_of_bins_max = math.ceil(total_players / 2)
        if n_of_bins > n_of_bins_max:
            n_of_bins = n_of_bins_max

    # Retrieve player ranks
    rank_skill = Player.objects.filter(skill__gt=player_skill).count() + 1
    rank_behaviour = Player.objects.filter(behaviour__gt=player_behaviour).count() + 1

    # Stretch ranks bins to provide anonymity
    rank_skill = math.ceil((rank_skill * n_of_bins) / total_players)
    rank_behaviour = math.ceil((rank_behaviour * n_of_bins) / total_players)

    return {'skill': f"{rank_skill}/{n_of_bins}", 'behaviour': f"{rank_behaviour}/{n_of_bins}"}
