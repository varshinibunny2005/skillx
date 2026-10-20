from django.db import models
from django.conf import settings

GENDER_FILTER = [('any', 'Any'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
REQUEST_STATUS = [('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined'), ('blocked', 'Blocked')]


class SkillMatch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matches_as_user')
    matched_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matches_as_match')
    skill_to_learn = models.ForeignKey('skills.Skill', on_delete=models.CASCADE, related_name='learn_matches', null=True)
    skill_to_teach = models.ForeignKey('skills.Skill', on_delete=models.CASCADE, related_name='teach_matches', null=True)
    score = models.FloatField(default=0)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('contacted', 'Contacted')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'matched_user']
        ordering = ['-score']


class ConnectionRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
    skill_to_learn = models.ForeignKey('skills.Skill', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['sender', 'receiver']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"


class VideoSession(models.Model):
    SESSION_STATUS = [('scheduled', 'Scheduled'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_sessions')
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='joined_sessions')
    skill = models.ForeignKey('skills.Skill', on_delete=models.SET_NULL, null=True)
    room_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=15, choices=SESSION_STATUS, default='scheduled')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session: {self.host.username} & {self.participant.username}"
