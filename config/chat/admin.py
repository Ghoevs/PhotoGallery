from django.contrib import admin
from .models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('photo', 'buyer', 'seller', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('photo__title', 'buyer__username', 'seller__username')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'text', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'text')