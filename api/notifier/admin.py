from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from notifier.models import Friend


class FriendInline(admin.TabularInline):
    model = Friend
    extra = 1


class UserAdminExtended(UserAdmin):
    inlines = (FriendInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdminExtended)
