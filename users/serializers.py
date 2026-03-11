from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Skill, UserSkill
User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'bio', 'profile_image']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']

class UserSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    category = serializers.CharField(source='skill.category', read_only=True)
    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'level', 'can_learn', 'can_teach', 'skill_name', 'category']
        
    def validate(self, data):
        if not data.get('can_learn') and not data.get('can_teach'):
            raise serializers.ValidationError("User must either teach or learn the skill.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        skill = validated_data["skill"]

        if UserSkill.objects.filter(user=user, skill=skill).exists():
            raise serializers.ValidationError("Skill already added.")

        return UserSkill.objects.create(user=user, **validated_data)


class MentorSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    class Meta:
        model = UserSkill
        fields = ['id', 'user', 'skill', 'level', 'skill_name', 'username', 'user_email']

class MentorSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name')
    class Meta:
        model = UserSkill
        fields = ['id', 'skill_name', 'level']

class MentorProfileSerializer(serializers.ModelSerializer):
    mentor = serializers.SerializerMethodField()
    skill = serializers.SerializerMethodField()
    other_skills = serializers.SerializerMethodField()

    class Meta:
        model = UserSkill
        fields = ['id','mentor','skill','other_skills']

    def get_mentor(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'bio': obj.user.bio,
        }

    def get_skill(self, obj):
        return {
            'name': obj.skill.name,
            'category': obj.skill.category,
            'level': obj.level,
        }

    def get_other_skills(self, obj):
        skills = UserSkill.objects.filter(user=obj.user, can_teach=True).exclude(id=obj.id)
        return MentorSkillSerializer(skills, many=True).data
                

"""
Serializer lifecycle:
    Frontend sends JSON
            ↓
    Serializer receives initial_data
            ↓
    Field validation happens
            ↓
    validate_<field>() runs
            ↓
    validate() runs
            ↓
    cleaned data becomes validated_data
            ↓
    create() or update() runs
"""