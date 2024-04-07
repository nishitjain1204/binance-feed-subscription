# chat/routing.py
from django.urls import re_path

from .consumers import binance_consumer

websocket_urlpatterns = [
    re_path(r"ws/feed", binance_consumer.BinanceConsumer.as_asgi()),
]