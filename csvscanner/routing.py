from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/channel/(?P<id_proceso>[\w\-]+)/$", consumers.LogConsumer.as_asgi()),
]