from jwt_auth.decorators import login_required
from profiles.models import Profile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from chats.models import Chat, Message

from .serializers import ChatSerializer01, MessageSerializer01


@api_view(["GET"])
@login_required
def get_chats_list(request):
    index = request.query_params.get("scroll-index", 0)
    batch_length = request.query_params.get("batch-length", 20)

    chats = Chat.objects.filter(members=request.user.profile).exclude(messages=None)

    ordered_chats = sorted(chats, key=lambda chat: chat.messages.last().created_at)
    ordered_chats.reverse()

    serializer = ChatSerializer01(ordered_chats[index * batch_length : (index + 1) * batch_length], many=True)
    response_data = serializer.data

    for serialized_chat in response_data:
        chat = Chat.objects.get(id=serialized_chat["id"])
        print(len(chat.last_messages))
        serialized_chat["unvisualized_messages_number"] = chat.get_unvisualized_messages_number(request.user.profile)

    return Response(response_data)


@api_view(["GET"])
@login_required
def get_chat_messages(request, chat_id):
    scroll_index = request.query_params.get("scroll-index", 0)
    batch_length = request.query_params.get("batch-length", 20)
    unvizualized_only = request.query_params.get("unvizualized-only", False)

    try:
        chat = Chat.objects.get(id=chat_id)
    except:
        return Response("Conversa não encontrada!", status=status.HTTP_404_NOT_FOUND)

    if request.user.profile not in chat.members.all():
        return Response("Você não está na conversa!", status=status.HTTP_400_BAD_REQUEST)

    messages = (
        chat.messages.all() if not unvizualized_only else chat.messages.exclude(visualized_by=request.user.profile)
    )

    messages = sorted(messages, key=lambda message: -message.created_at.timestamp())
    messages = list(messages[scroll_index * batch_length : (scroll_index + 1) * batch_length])

    serializer = MessageSerializer01(messages, many=True)

    return Response(serializer.data)


@api_view(["PATCH"])
@login_required
def visualize_chat_messages(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
    except:
        return Response("Conversa não encontrada!", status=status.HTTP_404_NOT_FOUND)

    if request.user.profile not in chat.members.all():
        return Response("Você não está na conversa!", status=status.HTTP_400_BAD_REQUEST)

    for message in chat.messages.exclude(visualized_by=request.user.profile):
        message.visualized_by.add(request.user.profile)
        message.save()

    return Response("success")


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

    message = Message.objects.create(chat=chat, sender=request.user.profile, content=content)
    message.visualized_by.add(request.user.profile)
    message.save()

    serializer = MessageSerializer01(message)

    return Response(serializer.data)


@api_view(["POST"])
@login_required
def create_chat(request):
    try:
        other_members_usernames = request.data["members"]
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    try:
        other_members = list(
            map(lambda username: Profile.objects.get(user__username=username), other_members_usernames)
        )
    except:
        return Response("Nome de usuário inválido!", status=status.HTTP_404_NOT_FOUND)

    chat = Chat.objects.create()
    chat.members.set([request.user.profile, *other_members])
    chat.save()

    serializer = ChatSerializer01(chat)

    return Response(serializer.data)
