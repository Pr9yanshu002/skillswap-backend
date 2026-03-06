
from booking.models import Session, SessionSlot
from users import serializers


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
        userskill = data["userskill"]

        # Prevent duplicate pending
        existing = Session.objects.filter(
            learner=learner,
            userskill=userskill,
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
        userskill = validated_data["userskill"]

        mentor = userskill.user

        return Session.objects.create(
            mentor=mentor,
            learner=learner,
            **validated_data
        )