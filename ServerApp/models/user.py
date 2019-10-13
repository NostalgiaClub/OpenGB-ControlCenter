from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


from ServerApp.models.server import Server


def new_token():
    from random import random
    from hashlib import shake_256

    return shake_256("{}".format(random()).encode('utf-8')).hexdigest(6)


class Guild(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=20,
        unique=True,
    )


class Avatar(models.Model):
    name = models.CharField(
        _("Avatar Name"),
        unique=True,
        max_length=50,
    )

    value = models.CharField(
        max_length=16,
        unique=True,
    )


class User(AbstractUser):
    guild = models.ForeignKey(
        Guild,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True
    )

    rank_current = models.SmallIntegerField(
        _("Rank (Current)"),
        default=19,
    )

    rank_season = models.SmallIntegerField(
        _("Rank (Season)"),
        default=19
    )

    cash = models.IntegerField(
        _("Cash"),
        default=0
    )

    gold = models.IntegerField(
        _("Gold"),
        default=0
    )

    avatar_current = models.ForeignKey(
        Avatar,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="avatar_current"
    )

    avatar_inventory = models.ManyToManyField(
        Avatar,
        default=None,
        blank=True,
        related_name="avatar_inventory"
    )

    token = models.CharField(
        "Auth Token",
        max_length=12,
        default=new_token
    )

    current_server = models.ForeignKey(
        Server,
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        blank=True
    )

    @property
    def as_dict(self):
        return {
            'username': self.username,
            'token': self.token,
            'guild': "" if not self.guild else self.guild.name,
            'rank_current': self.rank_current,
            'rank_season': self.rank_season,
            'avatar_current': None if not self.avatar_current else self.avatar_current.value,
            'avatar_inventory': [],
            'cash': self.cash,
            'gold': self.gold,
        }
