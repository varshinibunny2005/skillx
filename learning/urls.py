from django.urls import path
from . import views
urlpatterns = [
    path('', views.learning_home, name='learning_home'),
]
