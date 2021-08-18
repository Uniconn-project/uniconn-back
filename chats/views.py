from jwt_auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from chats.models import Chat

from .serializers import ChatSerializer01


@api_view(["GET"])
@login_required
def get_chats_list(request):
    chats = Chat.objects.filter(members=request.user.profile)
    serializer = ChatSerializer01(chats, many=True)

    return Response(serializer.data)
