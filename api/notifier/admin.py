from django.contrib import admin

from notifier.models import Friend

# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin


# User = get_user_model()


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ("user", "__str__", "date_of_birth")
    list_filter = ["date_of_birth"]
    search_fields = ["date_of_birth__month", "date_of_birth__day"]
    date_hierarchy = "date_of_birth"


class FriendInline(admin.TabularInline):
    model = Friend
    extra = 1


# class UserAdminExtended(UserAdmin):
#     inlines = (FriendInline,)


# admin.site.unregister(User)
# admin.site.register(User, UserAdminExtended)
