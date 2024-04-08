# chat/routing.py
from django.urls import re_path

from .consumers import binance_consumer , feed_consumer

websocket_urlpatterns = [
    re_path(r"ws/feed", binance_consumer.BinanceConsumer.as_asgi()),
    re_path(r"ws/data", feed_consumer.FeedConsumer.as_asgi()),
]