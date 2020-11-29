from django.contrib import admin

from notifier.models import Event

# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin


# User = get_user_model()


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("user", "__str__", "annual_date")
    list_filter = ["annual_date"]
    search_fields = ["annual_date__month", "annual_date__day"]
    date_hierarchy = "annual_date"


class EventInline(admin.TabularInline):
    model = Event
    extra = 1


# class UserAdminExtended(UserAdmin):
#     inlines = (EventInline,)


# admin.site.unregister(User)
# admin.site.register(User, UserAdminExtended)
