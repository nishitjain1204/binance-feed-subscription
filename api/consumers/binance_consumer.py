import asyncio,json
import websockets

from rest_framework_simplejwt.tokens import AccessToken
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async

from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer,
)
from channels.layers import get_channel_layer

from api.models import Subscription

class BinanceConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        
        """
        Connect to the websocket
        """
        
        query_params = parse_qs(self.scope['query_string'].decode())
        jwt_token = query_params.get('token')[0] if 'token' in query_params else None
        
        if not jwt_token:
            await self.close()
            return
        
        # checks if user is subscribed to that channel group
        await self.check_subscription(jwt_token)
        
        
        await self.channel_layer.group_add(
            "newchannel",
            self.channel_name
        )
        
        await self.accept()
       
        asyncio.create_task(self.send_data_to_group())
  
    async def binance_data(self, event):
        """
        Handles data coming from the channel group with type `binance_data`
        """
        message = event

        # Send the message to the client
        await self.send(text_data=json.dumps({
            'channel_message': message
        }))

    async def send_data_to_group(self):
        
        """
        Sends data to group
        """
        
        channel_layer = get_channel_layer()
        url = "wss://dstream.binance.com/stream?streams=btcusd_perp@bookTicker"
        async with websockets.connect(url) as ws:
            while True:
                try:
                    response = await ws.recv()
                    await channel_layer.group_send(
                                "newchannel",
                                {"message" : json.loads(response),
                                    "type" : "binance_data"}
                            )
                except Exception as e:
                    
                    await channel_layer.group_send(
                                "newchannel",
                                {"message" : {
                                    "error": "Connection Error",},
                                    "type" : "binance_data"}
                            )
                    await self.close()
    
    async def check_subscription(self,jwt_token):
        
        try:
            
            access_token = (AccessToken(jwt_token))
            
            user_id = access_token['user_id']
            
            subscription = await sync_to_async(Subscription.objects.get)(user_id=user_id)
            
            if subscription.channel_group != "newchannel":
                await self.close()
            
            return True
        
        except Exception as e:
            
            await self.send_json(
                {
                    "error" : "User is not subscribed to this channel group"
                }
            )
            await self.close()
            return False
            
        