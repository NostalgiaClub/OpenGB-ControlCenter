
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import json

from ServerApp.serializers import broker_serializer, server_serializer


class CustomAsyncConsumer(AsyncWebsocketConsumer):
    room_name = None
    room_group_name = None

    async def connect(self):
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, data):
        print("Receiving JSON Data {}".format(data))
        if data.get('type') and not data['type'].startswith('_') and getattr(self, data['type']):
            func = getattr(self, data.pop('type'))
            return await func(data)


class BrokerConsumer(CustomAsyncConsumer):
    async def connect(self):
        self.room_name = "{}".format(self.scope['broker'].uuid)
        self.room_group_name = "BrokerChannel_{}".format(self.room_name)

        await super().connect()

        await self.send_broker_info()

    async def receive(self, text_data=None, binary_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            return await self.receive_json(text_data_json)

    async def send_broker_info(self):
        await self.send(text_data=json.dumps({
            'type': 'update_info',
            'broker': await self.get_broker_info()
        }))

    async def update_server_list(self, data):
        await self.send(text_data=json.dumps({
            'type': 'server_list',
            'servers': await self.get_updated_server_list()
        }))

    @database_sync_to_async
    def get_broker_info(self):
        return broker_serializer(self.scope['broker'])

    @database_sync_to_async
    def get_updated_server_list(self):
        return [
            server_serializer(server) for server in self.scope['broker'].server_set.all()
        ]


class ServerConsumer(CustomAsyncConsumer):
    async def connect(self):
        self.room_name = "{}".format(self.scope['server'].uuid)
        self.room_group_name = "ServerChannel_{}".format(self.room_name)

        await super().connect()

        await self.send_server_info()

    async def receive(self, text_data=None, binary_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            return await self.receive_json(text_data_json)

    async def send_server_info(self):
        await self.send(text_data=json.dumps({
            'type': 'update_info',
            'server': await self.get_server_info()
        }))

    async def get_user(self, data):
        print("Sending User Info")
        return await self.send(text_data=json.dumps({
            'type': 'user_info',
            'user_info': {
                data['username']: await self._get_user(data['username'])
            }
        }))

    async def login_user(self, data):
        await self._login_user(data['username'])

    async def logout_user(self, data):
        await self._logout_user(data['username'])

    @database_sync_to_async
    def get_server_info(self):
        return server_serializer(self.scope['server'])

    @database_sync_to_async
    def _get_user(self, username):
        print("Getting User")
        return self.scope['server'].get_user(username)

    @database_sync_to_async
    def _login_user(self, username):
        user = self.scope['server'].get_user(username)
        user.current_server = self.scope['server']
        user.save()
        user.current_server.player_count += 1
        user.current_server.save()

        return True

    @database_sync_to_async
    def _logout_user(self, username):
        user = self.scope['server'].get_user(username)
        if user.current_server != self.scope['server']:
            return False

        user.current_server.player_count -= 1
        user.current_server.save()
        user.current_server = None
        user.save()

        return True



