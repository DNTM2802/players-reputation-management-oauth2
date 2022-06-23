import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices


class Player(AbstractUser):
    pass
    AUTH_STATUS = Choices('NULL', 'CREDENTIALS', 'CMD')
    nic = models.CharField(default=None, max_length=128)  # Identifier from CMD
    skill = models.IntegerField(default=0)  # Skill attribute
    behaviour = models.IntegerField(default=0)  # Skill attribute
    auth_status = models.CharField(choices=AUTH_STATUS, default=AUTH_STATUS.NULL, max_length=11)  # Keep track of auth method

    def __str__(self):
        return self.username


class TempPlayer(models.Model):
    pass
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nic = models.CharField(default=None, max_length=128)  # Identifier from CMD

    def __str__(self):
        return [self.id, self.nic]
