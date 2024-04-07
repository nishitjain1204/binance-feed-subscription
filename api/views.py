from rest_framework.views import APIView
from .serializers import UserSerializer,SubscriptionSerializer
from rest_framework.response import Response
from rest_framework import generics,permissions
from .models import Subscription


# view for registering users
class RegisterView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class SubscriptionView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)