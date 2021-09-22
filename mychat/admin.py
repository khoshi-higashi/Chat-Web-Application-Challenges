from django.contrib import admin

# Register your models here.

from mychat.models import User

admin.site.register(User)

from mychat.models import Chatroom

admin.site.register(Chatroom)

from mychat.models import ChatLog

admin.site.register(ChatLog)

# from mychat.models import AccessLog

# admin.site.register(AccessLog)