from jwt_auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from chats.models import Chat, Message

from .serializers import ChatSerializer01, MessageSerializer01


@api_view(["GET"])
@login_required
def get_chats_list(request):
    chats = Chat.objects.filter(members=request.user.profile)
    serializer = ChatSerializer01(chats, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@login_required
def get_chat_messages(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
    except:
        return Response("Conversa não encontrada!", status=status.HTTP_404_NOT_FOUND)

    if request.user.profile not in chat.members.all():
        return Response("Você não está na conversa!", status=status.HTTP_400_BAD_REQUEST)

    serializer = MessageSerializer01(chat.messages.all(), many=True)

    return Response(serializer.data)


@api_view(["POST"])
@login_required
def create_message(request, chat_id):
    try:
        content = request.data["content"].strip()
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    try:
        chat = Chat.objects.get(id=chat_id)
    except:
        return Response("Conversa não encontrada!", status=status.HTTP_404_NOT_FOUND)

    if request.user.profile not in chat.members.all():
        return Response("Você não está na conversa!", status=status.HTTP_400_BAD_REQUEST)

    Message.objects.create(chat=chat, sender=request.user.profile, content=content)

    return Response("success")
