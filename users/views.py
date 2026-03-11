# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import MentorProfileSerializer, MentorSerializer, RegistrationSerializer, UserSerializer, SkillSerializer, UserSkillSerializer
from .models import Skill, UserSkill
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class SkillListView(generics.ListAPIView):
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Skill.objects.filter(is_active=True)

        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset.order_by("name")[:10]

class AddUserSkillView(generics.CreateAPIView):
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]

class MyUserSkillView(generics.ListAPIView):
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)

class MentorListView(generics.ListAPIView):
    serializer_class = MentorSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        skillid = self.request.query_params.get('skill')
        queryset = UserSkill.objects.filter(can_teach=True)

        if skillid:
            queryset = queryset.filter(skill_id=skillid)

        return queryset.select_related("user", "skill")

class MentorProfileView(generics.RetrieveAPIView):
    serializer_class = MentorProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return UserSkill.objects.filter(can_teach=True).select_related("user", "skill")
    