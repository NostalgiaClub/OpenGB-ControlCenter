from django.db import models
from django.utils.translation import ugettext_lazy as _


def new_uuid():
    from uuid import uuid4
    return uuid4()


def new_token():
    from random import random
    from hashlib import shake_256

    return shake_256("{}".format(random()).encode('utf-8')).hexdigest(20)


class BrokerManager(models.Manager):
    ...


class Broker(models.Model):
    objects = BrokerManager()

    uuid = models.UUIDField(
        _("UUID"),
        unique=True,
        help_text=_("Unique Identifier"),
        default=new_uuid
    )

    token = models.CharField(
        _("Token"),
        max_length=40,
        help_text=_("Authorization Token"),
        unique=True,
        default=new_token
    )

    name = models.CharField(
        _("Name"),
        max_length=20,
        help_text=_("Display Name of the Broker."
                    "This will be displayed as Region in the Launcher."),
        unique=True
    )

    bind_ip = models.GenericIPAddressField(
        _("Server IP"),
        help_text=_("IP Address to Bind")
    )

    bind_port = models.IntegerField(
        _("Server Port"),
        help_text=_("Port to Bind (Default: 8372"),
        default=8372
    )

    def __str__(self):
        return self.name


class Server(models.Model):
    broker = models.ForeignKey(
        Broker,
        on_delete=models.CASCADE
    )

    uuid = models.UUIDField(
        _("UUID"),
        unique=True,
        help_text=_("Unique Identifier"),
        default=new_uuid
    )

    token = models.CharField(
        _("Token"),
        max_length=40,
        help_text=_("Authorization Token"),
        unique=True,
        default=new_token
    )

    name = models.CharField(
        _("Name"),
        max_length=40
    )

    description = models.CharField(
        _("Description"),
        max_length=40,
    )

    bind_ip = models.GenericIPAddressField(
        _("IP"),
        help_text=_("IP Address to Bind")
    )

    bind_port = models.IntegerField(
        _("Port"),
        help_text=_("Port to Bind (Default: 8370"),
        default=8370
    )

    capacity = models.IntegerField(
        _("Capacity"),
        default=20,
        help_text=_("Define max number of player that can join to the server")
    )

    player_count = models.IntegerField(
        _("Actual Player Count"),
        default=0,
        help_text=_("This will be automatically updated every time a player join/leave")
    )

    enable = models.BooleanField(
        _("Enabled"),
        default=True,
        help_text=_("Enable/Disable the join to the server. Useful for maintenance")
    )

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        super().save(**kwargs)

        if not hasattr(self, 'options'):
            ServerOption.objects.create(server=self)

    @staticmethod
    def get_user(username):
        from ServerApp.models.user import User
        try:
            u = User.objects.get(username=username)
            return u.as_dict
        except Exception as e:
            print(e)
            return None


class ServerOption(models.Model):
    server = models.OneToOneField(
        Server,
        related_name='options',
        on_delete=models.CASCADE
    )

    avatar_enabled = models.BooleanField(
        _("Avatar"),
        default=True,
    )

    effect_force = models.BooleanField(
        _("Force Effect"),
        default=True
    )

    effect_tornado = models.BooleanField(
        _("Tornado Effect"),
        default=False,
    )

    effect_lightning = models.BooleanField(
        _("Lightning Effect"),
        default=True,
    )

    effect_wind = models.BooleanField(
        _("Wind Effect"),
        default=False,
    )

    effect_thor = models.BooleanField(
        _("Thor Effect"),
        default=True,
    )

    effect_moon = models.BooleanField(
        _("Moon Effect"),
        default=True,
    )

    effect_eclipse = models.BooleanField(
        _("Eclipse Effect"),
        default=False,
    )

    event1_enable = models.BooleanField(
        _("Event 1"),
        default=False,
    )

    event2_enable = models.BooleanField(
        _("Event 2"),
        default=False,
    )

    event3_enable = models.BooleanField(
        _("Event 3"),
        default=False,
    )

    event4_enable = models.BooleanField(
        _("Event 4"),
        default=False,
    )

    def __str__(self):
        return "for {}".format(self.server.name)

    @property
    def as_dict(self):
        response = dict()
        for field in self._meta.get_fields(include_parents=False):
            if field.name in ['id', 'server']:
                pass
            else:
                response[field.name] = getattr(self, field.name)

        return response




