
# from django.core import serializers
from rest_framework import serializers
from booking.models import Session, SessionSlot
from users.models import UserSkill
# from users import serializers


class SessionSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionSlot
        fields = ['id', 'start_time', 'end_time', 'is_selected']
        read_only_fields = ['is_selected']

class SessionSerializer(serializers.ModelSerializer):
    slots = SessionSlotSerializer(many=True, read_only=True)

    mentor = serializers.SerializerMethodField()
    learner = serializers.SerializerMethodField()
    userSkill = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'mentor', 'learner', 'userSkill', 'message', 'status', 'selected_slot', 'created_at', 'slots', 'meet_link']
        read_only_fields = ['mentor', 'learner', 'status', 'selected_slot', 'meet_link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # SerializerMethodField is read-only; POST must accept userSkill (pk) as input.
        if self.instance is None:
            self.fields["userSkill"] = serializers.PrimaryKeyRelatedField(
                queryset=UserSkill.objects.select_related("user", "skill")
            )

    def get_mentor(self, obj):
        return {
            "id": obj.mentor.id,
            "username": obj.mentor.username,
        }
    
    def get_learner(self, obj):
        return {
            "id": obj.learner.id,
            "username": obj.learner.username,
        }

    def get_userSkill(self, obj):
        return {
            "id": obj.userSkill.id,
            "skill": obj.userSkill.skill.name,
            "level": obj.userSkill.level,
        }

    def validate(self, data):
        request = self.context["request"]
        if request.method != "POST":
            return data

        learner = request.user
        userSkill = data["userSkill"]

        # Prevent duplicate pending
        existing = Session.objects.filter(
            learner=learner,
            userSkill=userSkill,
            status="pending"
        ).exists()

        if existing:
            raise serializers.ValidationError(
                "You already have a pending request for this mentor and skill."
            )

        return data
    
    def create(self, validated_data):
        request = self.context["request"]
        learner = request.user
        userSkill = validated_data["userSkill"]

        mentor = userSkill.user

        return Session.objects.create(
            mentor=mentor,
            learner=learner,
            **validated_data
        )