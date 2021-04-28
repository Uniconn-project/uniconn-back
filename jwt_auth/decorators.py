from rest_framework import status
from rest_framework.response import Response


def login_required(func):
    def wrap(*args, **kwargs):
        user = args[0].user
        if user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return Response("Login required view", status=status.HTTP_401_UNAUTHORIZED)

    return wrap
