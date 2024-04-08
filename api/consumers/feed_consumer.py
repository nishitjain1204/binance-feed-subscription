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

class FeedConsumer(AsyncJsonWebsocketConsumer):
    
    
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
       
        
  
    async def ethusd_perp(self, event):
        """
        Handles data coming from the channel group with type `binance_data`
        """
        message = event

        # Send the message to the client
        await self.send(text_data=json.dumps({
            'channel_message': message
        }))
    
    async def btcusd_perp(self, event):
        """
        Handles data coming from the channel group with type `binance_data`
        """
        message = event

        # Send the message to the client
        await self.send(text_data=json.dumps({
            'channel_message': message
        }))

    
    
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
            
        