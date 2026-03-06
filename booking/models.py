from django.db import models
from django.conf import settings
from users.models import UserSkill

# Create your models here.
class Session(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
    ]
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentor_sessions")
    learner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learner_sessions")
    userSkill = models.ForeignKey(UserSkill, on_delete=models.CASCADE)
    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    selected_slot = models.ForeignKey(
        "SessionSlot",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.learner} → {self.mentor} ({self.status})"


class SessionSlot(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="slots")
    proposed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_selected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
    