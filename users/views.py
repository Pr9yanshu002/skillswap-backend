# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
