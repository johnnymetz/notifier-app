from django.http import JsonResponse


def welcome(request):
    return JsonResponse({"ping": "pong"})
