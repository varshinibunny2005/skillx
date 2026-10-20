from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserStreak, Notification

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'full_name', 'is_email_verified', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('SkillX Info', {'fields': ('bio', 'avatar', 'date_of_birth', 'gender', 'preferred_language', 'location', 'is_email_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('SkillX Info', {'fields': ('email', 'first_name', 'last_name', 'bio')}),
    )

admin.site.register(UserStreak)
admin.site.register(Notification)
