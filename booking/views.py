from django.db import transaction
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from booking.models import Session, SessionSlot
from booking.serializers import SessionSerializer, SessionSlotSerializer
from django.db.models import Prefetch
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied, ValidationError

# Create your views here.

class SessionListCreateView(generics.ListCreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = self.request.query_params.get("role")

        queryset = Session.objects.all().prefetch_related("slots")

        if role == "mentor":
            return queryset.filter(mentor=user)

        if role == "learner":
            return queryset.filter(learner=user)

        return queryset.filter(
            Q(mentor=user) | Q(learner=user)
        )

class SessionUpdateView(generics.UpdateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Session.objects.all()

    def perform_update(self, serializer):
        session = serializer.instance
        user = self.request.user
        new_status = self.request.data.get("status")

        # Only mentor can update
        if session.mentor != user:
            raise PermissionDenied("Only mentor can update session status.")

        # Status transition rules
        if new_status == "accepted":
            if session.status != "pending":
                raise ValidationError("Only pending sessions can be accepted.")

        elif new_status == "rejected":
            if session.status != "pending":
                raise ValidationError("Only pending sessions can be rejected.")

        elif new_status == "completed":
            if session.status != "scheduled":
                raise ValidationError("Only scheduled sessions can be completed.")

        else:
            raise ValidationError("Invalid status update.")
        serializer.save(status=new_status)

class SessionSlotCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        session = get_object_or_404(Session, id=pk)
        
        if (session.mentor!=request.user):
            raise PermissionDenied("Only mentor can propose slots.")
    
        if session.status != "accepted":
            raise ValidationError("Slots can only be added to accepted sessions.")

        # Limit to 5 slots
        if session.slots.count() >= 5:
            raise ValidationError("Maximum 5 slots allowed.")

        serializer = SessionSlotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(session=session, proposed_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SlotSelectView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, pk):
        slot = get_object_or_404(SessionSlot, id=pk)
        session = slot.session
        user = request.user

        # Only learner can select
        if session.learner != user:
            raise PermissionDenied("Only learner can select a slot.")

        # Session must be accepted
        if session.status != "accepted":
            raise ValidationError("Slot can only be selected for accepted sessions.")

        # Prevent re-selection
        if session.selected_slot:
            raise ValidationError("A slot has already been selected.")

        slot.is_selected = True
        slot.save()

        session.selected_slot = slot
        session.status = "scheduled"
        session.save()

        SessionSlot.objects.filter(session=session).exclude(pk=slot.pk).delete()

        return Response({"detail": "Slot selected successfully."})
        

'''
Why We Added @transaction.atomic

This is VERY important.

Without it:

If something fails after:

slot.is_selected = True

session updated

but before deletion completes,

You could end up with inconsistent state.

With @transaction.atomic:

Everything succeeds OR everything rolls back.

This is database integrity protection.
'''