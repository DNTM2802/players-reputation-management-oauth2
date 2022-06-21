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
    global l

    # SKILL
    player1_skill_pref = player1.skill_preference
    player1_skill = player1.skill.split("/")
    player2_skill = player2.skill.split("/")

    skill_result = False
    behaviour_result = False

    if player1_skill_pref == "l":
        skill_result = compare_reputations(player2_skill, "l", player1_skill)
    elif player1_skill_pref == "g":
        skill_result = compare_reputations(player2_skill, "g", player1_skill)
    elif player1_skill_pref == "eq":
        skill_result = compare_reputations(player2_skill, "eq", player1_skill)
    elif player1_skill_pref == "le":
        skill_result = compare_reputations(player2_skill, "l", player1_skill) \
                       or compare_reputations(player2_skill, "eq", player1_skill)
    elif player1_skill_pref == "ge":
        skill_result = compare_reputations(player2_skill, "g", player1_skill) \
                       or compare_reputations(player2_skill, "eq", player1_skill)
    else:
        pass

    # Behaviour
    player1_behaviour_pref = player1.behaviour_preference
    player1_behaviour = player1.behaviour.split("/")
    player2_behaviour = player2.behaviour.split("/")

    if player1_behaviour_pref == "l":
        behaviour_result = compare_reputations(player2_behaviour, "l", player1_behaviour)
    elif player1_behaviour_pref == "g":
        behaviour_result = compare_reputations(player2_behaviour, "g", player1_behaviour)
    elif player1_behaviour_pref == "eq":
        behaviour_result = compare_reputations(player2_behaviour, "eq", player1_behaviour)
    elif player1_behaviour_pref == "le":
        behaviour_result = compare_reputations(player2_behaviour, "l", player1_behaviour) \
                           or compare_reputations(player2_behaviour, "eq", player1_behaviour)
    elif player1_behaviour_pref == "ge":
        behaviour_result = compare_reputations(player2_behaviour, "g", player1_behaviour) \
                           or compare_reputations(player2_behaviour, "eq", player1_behaviour)
    else:
        pass

    l.log(f"{player1.player_id} skill: {player1_skill}")
    l.log(f"{player1.player_id} behaviour: {player1_behaviour}")
    l.log(f"{player2.player_id} skill: {player2_skill}")
    l.log(f"{player2.player_id} behaviour: {player2_behaviour}")
    l.log(f"{player1.player_id} wants {player1.skill_preference} skill.")
    l.log(f"{player1.player_id} wants {player1.behaviour_preference} behaviour.")
    l.log(f"{player1.player_id} matches with {player2.player_id} in terms of skill? {skill_result}")
    l.log(f"{player1.player_id} matches with {player2.player_id} in terms of behaviour? {behaviour_result}")
    return skill_result and behaviour_result


def compare_reputations(rep1, condition, rep2):
    # Stretch bins
    l.log(rep1)
    rep1[1] = int(rep1[1])
    rep1[0] = int(rep1[0])
    rep2[1] = int(rep2[1])
    rep2[0] = int(rep2[0])

    factor1 = 10 / rep1[1]
    max_1 = (rep1[0] * 10) / rep1[1]
    min_1 = (rep1[0] - 1) * factor1

    factor2 = 10 / rep2[1]
    max_2 = (rep2[0] * 10) / rep2[1]
    min_2 = (rep2[0] - 1) * factor2

    # If intersected in more than one point, all possible conditions are met
    if max_1 > min_2 and min_1 < max_2:
        return True

    # If don't intersect or intersect in only one point, then r1 > r2 only if r1 ends before r2 starts.
    if condition == 'g':
        return max_1 < min_2

    # If don't intersect or intersect in only one point, then r1 < r2 only if r2 ends before r1 starts.
    if condition == 'l':
        return max_2 < min_1

    # Intersect in one point (extremes of both reputations)? Then they may be equal
    if condition == 'eq':
        return max_1 == min_2 or min_1 == max_2

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
