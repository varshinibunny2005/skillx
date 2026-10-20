from django.urls import path
from . import views

urlpatterns = [
    path('', views.find_matches, name='find_matches'),
    path('requests/', views.manage_requests, name='manage_requests'),
    path('send/<int:user_id>/', views.send_request, name='send_request'),
    path('accept/<int:req_id>/', views.accept_request, name='accept_request'),
    path('decline/<int:req_id>/', views.decline_request, name='decline_request'),
    path('connections/', views.connections, name='connections'),
    path('chat/<int:user_id>/', views.chat, name='chat'),
    path('video/start/<int:user_id>/', views.start_video_session, name='start_video'),
    path('video/<int:session_id>/', views.video_room, name='video_room'),
]
