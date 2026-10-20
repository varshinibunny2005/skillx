from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_list, name='community_list'),
    path('create/', views.create_community, name='create_community'),
    path('<int:pk>/', views.community_detail, name='community_detail'),
    path('<int:pk>/join/', views.join_community, name='join_community'),
    path('<int:pk>/leave/', views.leave_community, name='leave_community'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),
    path('groups/<int:pk>/join/', views.join_group, name='join_group'),
]
