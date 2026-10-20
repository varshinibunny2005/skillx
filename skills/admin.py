from django.contrib import admin
from .models import Skill, UserSkill, SkillTest, Question, Answer, TestAttempt

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2
    inlines = [AnswerInline]

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name']

@admin.register(SkillTest)
class SkillTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'skill', 'level', 'passing_score']
    inlines = [QuestionInline]

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'relation', 'level', 'verified']

admin.site.register(TestAttempt)
