
# from django.core import serializers
from rest_framework import serializers
from booking.models import Session, SessionSlot
# from users import serializers


class SessionSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionSlot
        fields = ['id', 'start_time', 'end_time', 'is_selected']
        read_only_fields = ['is_selected']

class SessionSerializer(serializers.ModelSerializer):
    slots = SessionSlotSerializer(many=True, read_only=True)
    class Meta:
        model = Session
        fields = ['id', 'mentor', 'learner', 'userSkill', 'message', 'status', 'selected_slot', 'created_at', 'slots']
        read_only_fields = ['mentor', 'learner', 'status', 'selected_slot']

    def validate(self, data):
        request = self.context["request"]
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