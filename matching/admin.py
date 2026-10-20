from django.contrib import admin
from .models import SkillMatch, ConnectionRequest, Message, VideoSession
admin.site.register(SkillMatch)
admin.site.register(ConnectionRequest)
admin.site.register(Message)
admin.site.register(VideoSession)
