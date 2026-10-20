from django.db import models
from django.conf import settings

SKILL_CATEGORIES = [
    ('tech', 'Technology'), ('music', 'Music'), ('art', 'Art & Design'),
    ('language', 'Languages'), ('cooking', 'Cooking'), ('fitness', 'Fitness'),
    ('business', 'Business'), ('science', 'Science'), ('math', 'Mathematics'),
    ('writing', 'Writing'), ('photography', 'Photography'), ('craft', 'Crafts'),
    ('dance', 'Dance'), ('sports', 'Sports'), ('other', 'Other'),
]

LEVEL_CHOICES = [
    ('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('expert', 'Expert'),
]


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-star')
    color = models.CharField(max_length=7, default='#6366f1')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UserSkill(models.Model):
    SKILL_RELATION = [('have', 'I Have This Skill'), ('want', 'I Want to Learn This')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    relation = models.CharField(max_length=10, choices=SKILL_RELATION)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, blank=True)
    verified = models.BooleanField(default=False)
    years_experience = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'skill', 'relation']

    def __str__(self):
        return f"{self.user.username} - {self.skill.name} ({self.relation})"


class SkillTest(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='tests')
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    passing_score = models.IntegerField(default=70)
    time_limit_minutes = models.IntegerField(default=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.skill.name} - {self.level} Test"


class Question(models.Model):
    QUESTION_TYPES = [('mcq', 'Multiple Choice'), ('true_false', 'True/False')]
    test = models.ForeignKey(SkillTest, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='mcq')
    explanation = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)


class TestAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(SkillTest, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)
    time_taken_seconds = models.IntegerField(default=0)

    class Meta:
        ordering = ['-completed_at']
