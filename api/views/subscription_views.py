
from api.serializers.subscription_serializer import SubscriptionSerializer
from rest_framework.response import Response
from rest_framework import generics,permissions
from api.models import Subscription
from rest_framework import status


class SubscriptionView(generics.CreateAPIView):

    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # Extract user from JWT token
        user = request.user

        # Create subscription with user and channel_group from request data
        data = {'user': user.id, 'channel_group': request.data.get('channel_group')}
        serializer = SubscriptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteSubscriptionView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    
    def delete(self, request):
        # Extract user from JWT token
        try:
            user = request.user
            sub  = Subscription.objects.get(user_id=user.id)
            sub.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

        