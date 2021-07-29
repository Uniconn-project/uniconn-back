import base64
import datetime

import pytz
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from jwt_auth.decorators import login_required
from projects.models import DiscussionReply, DiscussionStar, Field, ProjectRequest
from projects.serializers import (
    DiscussionReplySerializer02,
    DiscussionStarSerializer02,
    FieldSerializer01,
    ProjectRequestSerializer01,
    ProjectSerializer01,
    ProjectSerializer03,
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from universities.models import Major, University

from .models import Profile, Skill
from .serializers import ProfileSerializer01, ProfileSerializer03, SkillSerializer01

User = get_user_model()


@api_view(["POST"])
def signup_view(request):
    try:
        username = request.data["username"].strip().lower().replace(" ", "")
        email = request.data["email"].strip()
        password = request.data["password"].strip()
        passwordc = request.data["passwordc"].strip()
        first_name = request.data["first_name"].strip()
        last_name = request.data["last_name"].strip()
        birth_date = request.data["birth_date"]
        is_attending_university = request.data["is_attending_university"]
        if is_attending_university:
            university_name = request.data["university_name"]
            major_name = request.data["major_name"]
        skills_names = request.data["skills_names"]
        skills = Skill.objects.filter(name__in=skills_names)
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    # error messages that repeat in the code
    BLANK_FIELD_ERR_MSG = "Todos os campos devem ser preenchidos!"
    INVALID_BIRTH_DATE_ERR_MSG = "Data de nascimento inválida!"

    if (
        username == ""
        or email == ""
        or password == ""
        or passwordc == ""
        or first_name == ""
        or last_name == ""
        or birth_date == ""
    ):
        return Response(BLANK_FIELD_ERR_MSG, status=status.HTTP_400_BAD_REQUEST)

    if len(username) > 25 or len(email) > 50 or len(password) > 50 or len(first_name) > 30 or len(last_name) > 30:
        return Response("Respeite os limites de caracteres de cada campo!", status=status.HTTP_400_BAD_REQUEST)

    if password != passwordc:
        return Response("As senhas devem ser iguais!", status=status.HTTP_400_BAD_REQUEST)

    if len(password) < 6:
        return Response("A senha deve ter pelo menos 6 caracteres!", status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response("Nome de usuário já utilizado!", status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response("Email já utilizado!", status=status.HTTP_400_BAD_REQUEST)

    if not skills.exists():
        return Response("Selecione pelo menos uma habilidade válida!", status=status.HTTP_400_BAD_REQUEST)

    try:
        age = datetime.date.today() - datetime.date.fromisoformat(birth_date)

        if age <= datetime.timedelta(days=0) or age >= datetime.timedelta(weeks=7800):
            return Response(INVALID_BIRTH_DATE_ERR_MSG, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(INVALID_BIRTH_DATE_ERR_MSG, status=status.HTTP_400_BAD_REQUEST)

    if is_attending_university:
        try:
            university = University.objects.get(name=university_name)
        except:
            return Response("Universidade inválida!", status=status.HTTP_400_BAD_REQUEST)

        try:
            major = Major.objects.get(name=major_name)
        except:
            return Response("Curso inválido!", status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(username=username.lower(), email=email)
    user.set_password(password)
    user.save()

    user.profile.first_name = first_name
    user.profile.last_name = last_name
    user.profile.birth_date = birth_date
    user.profile.skills.set(skills)
    user.profile.is_attending_university = is_attending_university
    if is_attending_university:
        user.profile.university = university
        user.profile.major = major
    user.profile.save()

    return Response("success")


@api_view(["PUT"])
@login_required
def edit_my_profile(request):
    profile = request.user.profile

    try:
        username = request.data["username"].strip()
        photo = request.data["photo"]
        first_name = request.data["first_name"].strip()
        last_name = request.data["last_name"].strip()
        bio = request.data["bio"].strip()
        linkedIn = request.data["linkedIn"].strip()
        is_attending_university = request.data["is_attending_university"]
        if is_attending_university:
            university_name = request.data["university_name"]
            major_name = request.data["major_name"]
        skills_names = request.data["skills_names"]
        skills = Skill.objects.filter(name__in=skills_names)
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    if User.objects.exclude(pk=request.user.pk).filter(username=username).exists():
        return Response("Nome de usuário já utilizado!", status=status.HTTP_400_BAD_REQUEST)

    if not skills.exists():
        return Response("Selecione pelo menos uma habilidade válida!", status=status.HTTP_400_BAD_REQUEST)

    if username == "" or first_name == "" or last_name == "" or bio == "":
        return Response(
            "Os campos nome de usuário, nome, sobrenome e bio são obrigatórios!", status=status.HTTP_400_BAD_REQUEST
        )

    if (
        (username and len(username) > 25)
        or (first_name and len(first_name) > 30)
        or (last_name and len(last_name) > 30)
        or (bio and len(bio) > 150)
        or (linkedIn and len(linkedIn) > 50)
    ):
        return Response("Respeite os limites de caracteres de cada campo!", status=status.HTTP_400_BAD_REQUEST)

    if photo is not None:
        format, photostr = photo.split(";base64,")
        photo_format = format.split("/")[-1]
        profile_photo = ContentFile(base64.b64decode(photostr), name=f"{profile.user.username}.{photo_format}")
        profile.photo = profile_photo

    if is_attending_university:
        try:
            university = University.objects.get(name=university_name)
        except:
            return Response("Universidade inválida!", status=status.HTTP_400_BAD_REQUEST)

        try:
            major = Major.objects.get(name=major_name)
        except:
            return Response("Curso inválido!", status=status.HTTP_400_BAD_REQUEST)

        profile.university = university
        profile.major = major

    profile.user.username = username
    profile.first_name = first_name
    profile.last_name = last_name
    profile.bio = bio
    profile.linkedIn = linkedIn
    profile.skills.set(skills)

    profile.user.save()
    profile.save()

    return Response("success")


@api_view(["GET"])
@login_required
def get_my_profile(request):
    profile = request.user.profile
    serializer = ProfileSerializer01(profile)

    return Response(serializer.data)


@api_view(["GET"])
def get_profile(request, slug):
    try:
        profile = Profile.objects.get(user__username=slug)

        serializer = ProfileSerializer01(profile)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response("Usuário não encontrado", status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_profile_projects(request, slug):
    try:
        profile = Profile.objects.get(user__username=slug)
        serializer = ProjectSerializer01(profile.projects, many=True)

        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response("Usuário não encontrado", status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_filtered_profiles(request, query):
    profiles = Profile.objects.filter(user__username__icontains=query)[:20]
    serializer = ProfileSerializer03(profiles, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_profile_list(request):
    profiles = Profile.objects.exclude(user__is_superuser=True)[:25]
    serializer = ProfileSerializer03(profiles, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_skills_name_list(request):
    skills = Skill.objects.all()
    serializer = SkillSerializer01(skills, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@login_required
def get_notifications(request):
    profile = request.user.profile
    now = datetime.datetime.now()
    now = pytz.utc.localize(now)

    projects_invitations = ProjectRequest.objects.filter(profile=profile, type="invitation")
    projects_entry_requests = [
        request
        for request in ProjectRequest.objects.filter(project__members__profile=profile, type="entry_request")
        if request.project.members.get(profile=profile).role == "admin"
    ]

    discussions_stars = []

    for star in DiscussionStar.objects.filter(discussion__profile=profile).exclude(profile=profile):
        if not star.visualized:
            discussions_stars.append(star)
            continue

        if now - star.updated_at < datetime.timedelta(days=2):
            discussions_stars.append(star)

    discussions_replies = []

    for reply in DiscussionReply.objects.filter(discussion__profile=profile).exclude(profile=profile):
        if not reply.visualized:
            discussions_replies.append(reply)
            continue

        if now - reply.updated_at < datetime.timedelta(days=2):
            discussions_replies.append(reply)

    projects_invitations_serializer = ProjectRequestSerializer01(projects_invitations, many=True)
    projects_entry_requests_serializer = ProjectRequestSerializer01(projects_entry_requests, many=True)
    discussions_stars_serializer = DiscussionStarSerializer02(discussions_stars, many=True)
    discussions_replies_serializer = DiscussionReplySerializer02(discussions_replies, many=True)

    return Response(
        {
            "projects_invitations": projects_invitations_serializer.data,
            "projects_entry_requests": projects_entry_requests_serializer.data,
            "discussions_stars": discussions_stars_serializer.data,
            "discussions_replies": discussions_replies_serializer.data,
        }
    )


@api_view(["GET"])
@login_required
def get_notifications_number(request):
    profile = request.user.profile

    projects_invitations = ProjectRequest.objects.filter(profile=profile, type="invitation")
    projects_entry_requests = [
        request
        for request in ProjectRequest.objects.filter(project__members__profile=profile, type="entry_request")
        if request.project.members.get(profile=profile).role == "admin"
    ]

    unvisualized_discussions_stars = DiscussionStar.objects.filter(discussion__profile=profile, visualized=False)
    unvisualized_replies = DiscussionReply.objects.filter(discussion__profile=profile, visualized=False)

    return Response(
        len(projects_invitations)
        + len(projects_entry_requests)
        + len(unvisualized_discussions_stars)
        + len(unvisualized_replies)
    )


@api_view(["PATCH"])
@login_required
def visualize_notifications(request):
    for star in DiscussionStar.objects.filter(discussion__profile=request.user.profile, visualized=False):
        star.visualized = True
        star.save()

    for reply in DiscussionReply.objects.filter(discussion__profile=request.user.profile, visualized=False):
        reply.visualized = True
        reply.save()

    return Response("success")
