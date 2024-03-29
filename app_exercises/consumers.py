import json
import re

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.datetime_safe import datetime

from django.utils.timesince import timesince

from app_accounts.models import UserExerciseConversation, CustomUser, Room
from .models import Exercise
from .templatetags.chatextras import initials

from .gpt_utils import get_chatgpt_response


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.get_room()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']
        agent = text_data_json.get('agent', '')

        print('Receive: ', type)

        if type == 'message':
            exercise_id = await self.get_exercise_id()
            new_message = await self.create_message(name, message, agent, exercise_id)

            # Send message to group / room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name': name,
                    'agent': agent,
                    'initials': initials(name),
                    'created_at': timesince(new_message.created_at),
                }
            )

            # Fetch task description from the exercise
            exercise_description = await self.get_exercise_description(exercise_id)

            # Send the user message and exercise description to ChatGPT and get a response
            chat_gpt_response = await sync_to_async(get_chatgpt_response)(message, exercise_description)

            # Store ChatGPT's response in the database
            await self.create_message('ChatGPT', chat_gpt_response, None, exercise_id)

            # Send ChatGPT's response to the group/room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': chat_gpt_response,
                    'name': 'ChatGPT',
                    'agent': None,
                    'initials': 'CG',
                    'created_at': timesince(datetime.now()),  # Adjust as needed
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket (front end)
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'name': event['name'],
            'agent': event['agent'],
            'initials': event['initials'],
            'created_at': event['created_at'],
        }))

    @sync_to_async
    def get_exercise_id(self):
        match = re.search(r'/exercises/(\d+)/', self.room.url)
        if match:
            return int(match.group(1))
        else:
            return None

    @sync_to_async
    def get_exercise_description(self, exercise_id):
        if exercise_id is not None:
            try:
                exercise = Exercise.objects.get(pk=exercise_id)
                return exercise.description
            except Exercise.DoesNotExist:
                print(f"Exercise with id {exercise_id} does not exist.")
                return ""
        else:
            return ""

    @sync_to_async
    def get_room(self):
        self.room = Room.objects.get(uuid=self.room_name)

    @sync_to_async
    def create_message(self, sent_by, message, agent, exercise_id):
        if exercise_id is not None:
            exercise = Exercise.objects.get(pk=exercise_id)
        else:
            return None

        user = CustomUser.objects.get(pk=agent) if agent else None

        new_message = UserExerciseConversation.objects.create(
            exercise=exercise,
            body=message,
            sent_by=sent_by,
            created_by=user
        )

        self.room.messages.add(new_message)

        return new_message
