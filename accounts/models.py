from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

LANGUAGE_CHOICES = [
    ('en', 'English'), ('hi', 'Hindi'), ('te', 'Telugu'), ('ta', 'Tamil'),
    ('fr', 'French'), ('de', 'German'), ('es', 'Spanish'), ('zh', 'Chinese'),
    ('ja', 'Japanese'), ('ar', 'Arabic'), ('pt', 'Portuguese'), ('ru', 'Russian'),
    ('ko', 'Korean'), ('bn', 'Bengali'), ('mr', 'Marathi'), ('gu', 'Gujarati'),
]

GENDER_CHOICES = [
    ('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('P', 'Prefer not to say'),
]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    preferred_language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    location = models.CharField(max_length=200, blank=True)
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            dob = self.date_of_birth
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return None

    def __str__(self):
        return self.email


class UserStreak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity = models.DateField(null=True, blank=True)
    total_xp = models.IntegerField(default=0)
    total_sessions = models.IntegerField(default=0)

    def update_streak(self):
        today = timezone.now().date()
        if self.last_activity is None:
            self.current_streak = 1
        elif self.last_activity == today:
            return
        elif (today - self.last_activity).days == 1:
            self.current_streak += 1
        else:
            self.current_streak = 1
        self.last_activity = today
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        self.save()

    def add_xp(self, points):
        self.total_xp += points
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.current_streak} day streak"


class Notification(models.Model):
    NOTIF_TYPES = [
        ('request', 'Skill Request'),
        ('accepted', 'Request Accepted'),
        ('message', 'New Message'),
        ('session', 'Session Reminder'),
        ('achievement', 'Achievement Unlocked'),
        ('streak', 'Streak Milestone'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']
