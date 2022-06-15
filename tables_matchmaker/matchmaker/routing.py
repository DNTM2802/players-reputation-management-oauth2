# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
  re_path(r'ws/matchmaker/(?P<room_id>\w+)/$', consumers.Consumer.as_asgi()),
]