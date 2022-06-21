import random
import string

from logger import Logger
from matchmaker.models import Room

l = Logger()

available_preferences = ["l", "le", "eq", "ge", "g", "any"]


def match_player(player) -> str:
    global l
    rooms = Room.objects.all()
    for room in rooms:
        # if player is already in a room:
        if player in room.player_set.all():
            # l.log("Player is already in a room...")
            return room
            # meaning, it was already assigned a room and is waiting for a match

    for room in rooms:
        # checks if the room has the game player wants to play
        # and checks if there is space in the room
        if room.game.__eq__(player.game) and not room.is_full:
            if check_existence_of_opponents(room) and check_player_fitness(player, room):
                # l.log(f"Great! We found a match!")
                room.player_set.add(player)  # add the player to the matched room with other players
                room.save()

                room.match_ready = True if room.is_full else False
                room.save()

                return room
            else:
                continue

    # if code has gotten this far it means there is no match for the player
    # so we will create a new room for him

    # l.log(f"No match found... Creating new room...")

    new_room = generate_new_room(player.game)
    new_room.player_set.add(player)
    new_room.save()
    # l.log(new_room.player_set.all())

    return player.room


def check_player_fitness(player, room):
    """
    checks if a given player is a good fit for a room
    """

    # preference validation
    if are_player_preferences_valid(player):
        for opponent in room.player_set.all():
            # checks if preferences of player match with opponent and if opponent preferences match with player joining the room
            if preferences_are_matchable(player, opponent) and preferences_are_matchable(opponent, player):
                # l.log(f"Preferences match for player and opponent!")
                continue
            else:
                # l.log(f"Preferences DO NOT match for player and opponent!")
                return False

        # the player matched with all opponents
        return True

    return False


def preferences_are_matchable(player1, player2):
    """
    for skill or behaviour checks if player preferences are a match with the opponent's preferences
    """

    # SKILL
    player_pref = player1.skill_preference
    player2_skill = player2.skill.split("/")
    player1_skill = player1.skill.split("/")

    if player_pref == "l":
        if not are_reputations_matchable(player1_skill, "l", player2_skill):
            return False
    elif player_pref == "le":
        if not are_reputations_matchable(player1_skill, "le", player2_skill):
            return False
    elif player_pref == "eq":
        if not are_reputations_matchable(player1_skill, "eq", player2_skill):
            return False
    elif player_pref == "ge":
        if not are_reputations_matchable(player1_skill, "ge", player2_skill):
            return False
    elif player_pref == "g":
        if not are_reputations_matchable(player1_skill, "g", player2_skill):
            return False
    else:
        pass

    # Behaviour
    player_pref = player1.behaviour_preference
    player2_behaviour = player2.behaviour.split("/")
    player1_behaviour = player1.behaviour.split("/")

    if player_pref == "l":
        if not are_reputations_matchable(player1_behaviour, "l", player2_behaviour):
            return False
    elif player_pref == "le":
        if not are_reputations_matchable(player1_behaviour, "le", player2_behaviour):
            return False
    elif player_pref == "eq":
        if not are_reputations_matchable(player1_behaviour, "eq", player2_behaviour):
            return False
    elif player_pref == "ge":
        if not are_reputations_matchable(player1_behaviour, "ge", player2_behaviour):
            return False
    elif player_pref == "g":
        if not are_reputations_matchable(player1_behaviour, "g", player2_behaviour):
            return False
    else:
        pass

    return True


def are_reputations_matchable(rep1, condition, rep2):
    # Strech bins
    factor1 = 10 / rep1[1]
    max_1 = (rep1[0] * 10) / rep1[1]
    min_1 = (rep1[0] - 1) * factor1

    factor2 = 10 / rep2[1]
    max_2 = (rep2[0] * 10) / rep2[1]
    min_2 = (rep2[0] - 1) * factor2

    # If intersect, all possible conditions are met
    if max_1 > min_2 and min_1 < max_2:
        return True

    if condition == 'g':
        return max_1 < min_2

    if condition == 'ge':
        return max_1 <= min_2

    if condition == 'eq':
        return max_1 == min_2

    if condition == 'le':
        return max_2 <= min_1

    if condition == 'l':
        return max_2 < min_1

    return False


def generate_new_room(game) -> Room:
    """
        Create a new room
        returns room id
    """

    room_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    # failsafe unique room ids
    while Room.objects.filter(id=room_id).exists():
        room_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    new_room = Room(id=room_id, game=game)
    new_room.save()

    return new_room


def are_player_preferences_valid(player):
    # check if preferences are valid
    if not (
            player.skill_preference in available_preferences and player.behaviour_preference in available_preferences):
        # l.log(player.skill_preference)
        # l.log(player.behaviour_preference)
        # l.log(f"Invalid preferences...")
        return False
    return True


def check_existence_of_opponents(room):
    return True if room.player_set.all() else False

    # l.log(f"Checking if there are any players in this room... YES!") if ret else l.log(
