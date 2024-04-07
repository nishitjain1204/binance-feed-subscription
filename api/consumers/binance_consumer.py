from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio,json
import websockets
from urllib.parse import parse_qs

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from rest_framework_simplejwt.tokens import AccessToken



class BinanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        query_params = parse_qs(self.scope['query_string'].decode())
        jwt_token = query_params.get('token')[0] if 'token' in query_params else None
        print(self.channel_layer)
        if not jwt_token:
            await self.close()
            return
        try:
            access_token = AccessToken(jwt_token)
        except Exception as e:
            print(f"JWT token error: {e}")
            await self.close()
            return
        
        channel_layer = get_channel_layer()
        print(channel_layer)
        await self.channel_layer.group_add(
            "newchannel",
            self.channel_name
        )
        await self.accept()

        # Start subscribing to Binance WebSocket API
        async def subscribe_to_binance():
            channel_layer = get_channel_layer()
            print(channel_layer)
            async with websockets.connect("wss://dstream.binance.com/stream?streams=btcusd_perp@bookTicker") as ws:
                while True:
                    response = await ws.recv()
                    print(response)
                    await channel_layer.group_send(
                                "newchannel",
                                json.loads(response)
                            )

        asyncio.create_task(subscribe_to_binance())
