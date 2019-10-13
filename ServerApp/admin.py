from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ServerApp.models import User, Server, ServerOption, Broker


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = [
        'date_joined',
        'token',
        'rank_current', 'rank_season',
        'cash', 'gold',
        'avatar_current', 'avatar_inventory'
    ]

    fieldsets = UserAdmin.fieldsets + (
        ("Secure Data", {'fields': (
            'token',
            'cash',
            'gold',
        )}),
        ("Game Information", {'fields': (
            'guild',
            'rank_current',
            'rank_season',
            )}),
        ("Avatars", {'fields': (
            'avatar_current',
            'avatar_inventory'
            )})
    )


class ServerOptionInline(admin.StackedInline):
    model = ServerOption

    readonly_fields = ['server']

    can_delete = False


class ServerInline(admin.TabularInline):
    extra = 0

    model = Server

    exclude = ['token', 'player_count', 'uuid']

    readonly_fields = []

    can_delete = False
    show_change_link = True


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'broker',
        'name',
        'bind_ip',
        'bind_port'
    ]

    list_filter = ['enable']

    search_fields = ['name', 'uuid']

    readonly_fields = [
        'uuid',
        'token'
    ]

    inlines = [ServerOptionInline]


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'name',
        'bind_ip',
        'bind_port'
    ]

    search_fields = ['name', 'uuid']

    readonly_fields = [
        'uuid',
        'token'
    ]

    inlines = [ServerInline]

