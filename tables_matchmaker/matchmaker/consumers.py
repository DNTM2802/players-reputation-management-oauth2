import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core import serializers

from logger import Logger
from .models import Room

l = Logger()

number_of_users = 0


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        global number_of_users
        number_of_users += 1

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id
        self.scope['url_route']['kwargs']

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_players',
                'message': 'cool beans'
            }
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_room_match_status',
                'message': 'cool beans'
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        global number_of_users
        number_of_users -= 1

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        self.received_data = json.loads(text_data)
        global number_of_users

        if self.received_data['message'] == 'get-room-players' and len(self.received_data) == 1:
            players = await database_sync_to_async(self.get_players)()

            await self.send(text_data=json.dumps({
                'message': {'message-type': 'get-room-players', 'message-body': players}
            }))

            status = await database_sync_to_async(self.get_room_match_status)()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_room_match_status',
                    'message': status
                }
            )

            current_num_players = await database_sync_to_async(self.get_current_num_players)()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_current_num_players',
                    'message': current_num_players
                }
            )
        else:
            pass

    # CURRENT NUM PLAYERS UPDATES
    def get_current_num_players(self):
        return Room.objects.get(id=self.room_id).current_num_players

    async def update_current_num_players(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': {'message-type': 'update-current-num-players', 'message-body': message}
        }))

    # MATCH STATUS UPDATES
    def get_room_match_status(self):
        return "MATCHED" if Room.objects.get(id=self.room_id).match_ready else "NO MATCH"

    async def update_room_match_status(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': {'message-type': 'update-room-match-status', 'message-body': message}
        }))

    # PLAYER UPDATES
    def get_players(self):
        # if room exists get messages
        room = Room.objects.get(id=self.room_id)
        players = room.player_set.all()
        data = serializers.serialize("json", players)
        return data

    async def update_players(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': {'message-type': 'update-players'}
        }))
