from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from notifier.models import Friend


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ("user", "__str__", "date_of_birth")
    list_filter = ["date_of_birth"]
    search_fields = ["date_of_birth__month", "date_of_birth__day"]
    date_hierarchy = "date_of_birth"


class FriendInline(admin.TabularInline):
    model = Friend
    extra = 1


class UserAdminExtended(UserAdmin):
    inlines = (FriendInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdminExtended)
