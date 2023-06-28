from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    list_per_page = 30


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ('user', 'author')
    list_filter = ('author',)
    list_per_page = 30
