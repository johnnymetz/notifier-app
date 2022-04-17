from django.contrib import admin

from notifier.models import Event

# from users.models import User

# from django.contrib.auth.admin import UserAdmin


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("user", "__str__", "annual_date", "type")
    list_filter = ["annual_date", "type"]
    search_fields = ["annual_date__month", "annual_date__day", "type"]
    date_hierarchy = "annual_date"


class EventInline(admin.TabularInline):
    model = Event
    extra = 1


# class UserAdminExtended(UserAdmin):
#     inlines = (EventInline,)


# admin.site.unregister(User)
# admin.site.register(User, UserAdminExtended)
