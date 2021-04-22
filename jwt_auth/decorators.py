def login_required(func):
    def wrap(*args, **kwargs):
        user = args[0].user
        if user.is_authenticated:
            func(*args, **kwargs)
        else:
            return Response("Login required view", status=status.HTTP_401_UNAUTHORIZED)

    return wrap
