from django.db import models


# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_num_players = models.IntegerField()

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    # Create your models here.


class Room(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    match_ready = models.BooleanField(default=False)

    @property
    def current_num_players(self):
        return self.player_set.all().count()

    @property
    def is_full(self):
        return self.player_set.all().count() == self.game.max_num_players

    def __str__(self):
        return self.id + " " + self.game


class Player(models.Model):
    player_id = models.CharField(max_length=100, unique=True)
    skill = models.CharField(max_length=10)
    behaviour = models.CharField(max_length=10)
    skill_preference = models.CharField(max_length=10)
    behaviour_preference = models.CharField(max_length=10)
    granularity_preference = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    game = models.CharField(max_length=50)

    def __str__(self):
        return f'room_id {self.room}| player_id {self.player_id}| game {self.game} | skill {self.skill}| behaviour {self.behaviour}| skill_preference {self.skill_preference}| behaviour_preference {self.behaviour_preference}| granularity_preference {self.granularity_preference}'
