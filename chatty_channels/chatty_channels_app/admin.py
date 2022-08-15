from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from chatty_channels_app.models import ChatRoom, Message

# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(Message)
