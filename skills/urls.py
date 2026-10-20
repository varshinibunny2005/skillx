from django.urls import path
from . import views

urlpatterns = [
    path('setup/', views.skill_setup, name='skill_setup'),
    path('save/', views.save_skills, name='save_skills'),
    path('tests/', views.skill_tests, name='skill_tests'),
    path('test/<int:test_id>/', views.take_test, name='take_test'),
    path('my-skills/', views.my_skills, name='my_skills'),
]
