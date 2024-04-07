from rest_framework.views import APIView
from api.serializers.user_serializer import UserSerializer
from rest_framework.response import Response

class RegisterView(APIView):
    """
    View for registering users
    """
    permission_classes = []
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)