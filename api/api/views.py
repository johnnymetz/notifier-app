from django.http import HttpResponse


def welcome(request):
    return HttpResponse("<h3>Welcome to the Notifier application</h3>")
