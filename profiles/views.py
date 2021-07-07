import base64
import datetime

import pytz
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from jwt_auth.decorators import login_required
from projects.models import DiscussionStar, Market, Project, ProjectEnteringRequest
from projects.serializers import (
    DiscussionStarSerializer02,
    MarketSerializer01,
    ProjectEnteringRequestSerializer01,
    ProjectSerializer01,
    ProjectSerializer03,
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from universities.models import Major, University

from .models import Mentor, Profile, Student
from .serializers import ProfileSerializer01, ProfileSerializer02, ProfileSerializer03

User = get_user_model()


@api_view(["POST"])
def signup_view(request, user_type):
    if user_type not in ["student", "mentor"]:
        return Response("Tipo de usuário inválido!", status=status.HTTP_400_BAD_REQUEST)

    try:
        username = request.data["username"].strip().lower().replace(" ", "")
        email = request.data["email"].strip()
        password = request.data["password"].strip()
        passwordc = request.data["passwordc"].strip()
        first_name = request.data["first_name"].strip()
        last_name = request.data["last_name"].strip()
        birth_date = request.data["birth_date"]

        if user_type == "student":
            university_name = request.data["university"]
            major_name = request.data["major"]
            assert University.objects.filter(name=university_name).exists()
            assert Major.objects.filter(name=major_name).exists()
        elif user_type == "mentor":
            markets = request.data["markets"]
            assert Market.objects.filter(name__in=markets).exists()
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

    try:
        age = datetime.date.today() - datetime.date.fromisoformat(birth_date)

        if age <= datetime.timedelta(days=0) or age >= datetime.timedelta(weeks=7800):
            return Response(INVALID_BIRTH_DATE_ERR_MSG, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(INVALID_BIRTH_DATE_ERR_MSG, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(username=username.lower(), email=email)
    user.set_password(password)
    user.save()

    user.profile.first_name = first_name
    user.profile.last_name = last_name
    user.profile.birth_date = birth_date
    user.profile.save()

    if user_type == "student":
        university = university = University.objects.get(name=university_name)
        major = Major.objects.get(name=major_name.lower())
        Student.objects.create(profile=user.profile, university=university, major=major)

    elif user_type == "mentor":
        mentor = Mentor.objects.create(profile=user.profile)

        for market in Market.objects.filter(name__in=markets):
            market.mentors.add(mentor)

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

        if profile.type == "student":
            university = request.data["university"]
            major = request.data["major"]
            assert University.objects.filter(name=university).exists()
            assert Major.objects.filter(name=major).exists()
        elif profile.type == "mentor":
            markets = request.data["markets"]
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    if User.objects.exclude(pk=request.user.pk).filter(username=username).exists():
        return Response("Nome de usuário já utilizado!", status=status.HTTP_400_BAD_REQUEST)

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

    profile.user.username = username
    profile.first_name = first_name
    profile.last_name = last_name
    profile.bio = bio
    profile.linkedIn = linkedIn

    if profile.type == "student":
        profile.student.university = University.objects.get(name=university)
        profile.student.major = Major.objects.get(name=major)
        profile.student.save()
    elif profile.type == "mentor":
        profile.mentor.markets.set(Market.objects.filter(name__in=markets))
        profile.mentor.save()

    profile.user.save()
    profile.save()

    return Response("success")


@api_view(["GET"])
@login_required
def get_my_profile(request):
    profile = request.user.profile

    if profile.type == "student":
        serializer = ProfileSerializer01(profile)
    elif profile.type == "mentor":
        serializer = ProfileSerializer02(profile)

    return Response(serializer.data)


@api_view(["GET"])
def get_profile(request, slug):
    try:
        profile = Profile.objects.get(user__username=slug)

        if profile.type == "student":
            serializer = ProfileSerializer01(profile)
        elif profile.type == "mentor":
            serializer = ProfileSerializer02(profile)

        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response("There isn't any user with such username", status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_profile_projects(request, slug):
    try:
        profile = Profile.objects.get(user__username=slug)

        if profile.type == "student":
            projects = profile.student.projects.all()
        elif profile.type == "mentor":
            projects = profile.mentor.projects.all()

        serializer = ProjectSerializer01(projects, many=True)

        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response("There isn't any user with such username", status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_mentor_markets(request, slug):
    try:
        profile = Profile.objects.get(user__username=slug)
    except ObjectDoesNotExist:
        return Response("There isn't any user with such username", status=status.HTTP_404_NOT_FOUND)

    if profile.type != "mentor":
        return Response("Only mentors have markets", status=status.HTTP_400_BAD_REQUEST)

    serializer = MarketSerializer01(profile.mentor.markets, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_filtered_profiles(request, query):
    profiles = Profile.objects.filter(user__username__icontains=query)[:20]
    serializer = ProfileSerializer03(profiles, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_profile_list(request):
    profiles = Profile.objects.all()[:10]
    serializer = ProfileSerializer03(profiles, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@login_required
def get_notifications(request):
    profile = request.user.profile
    now = datetime.datetime.now()
    now = pytz.utc.localize(now)

    if profile.type == "student":
        projects_invitations = profile.student.pending_projects_invitations
        projects_entering_requests = ProjectEnteringRequest.objects.filter(project__students=profile.student)
    elif profile.type == "mentor":
        projects_invitations = profile.mentor.pending_projects_invitations
        projects_entering_requests = []
    else:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    discussions_stars = []

    for star in DiscussionStar.objects.filter(discussion__profile=request.user.profile):
        if not star.visualized:
            discussions_stars.append(star)
            continue

        if now - star.updated_at < datetime.timedelta(2):
            discussions_stars.append(star)

    projects_invitations_serializer = ProjectSerializer03(projects_invitations, many=True)
    projects_entering_requests_serializer = ProjectEnteringRequestSerializer01(projects_entering_requests, many=True)
    discussions_stars_serializer = DiscussionStarSerializer02(discussions_stars, many=True)

    return Response(
        {
            "projects_invitations": projects_invitations_serializer.data,
            "projects_entering_requests": projects_entering_requests_serializer.data,
            "discussions_stars": discussions_stars_serializer.data,
        }
    )


@api_view(["GET"])
@login_required
def get_notifications_number(request):
    profile = request.user.profile

    if profile.type == "student":
        project_invitations = profile.student.pending_projects_invitations.all()
        projects_entering_requests = ProjectEnteringRequest.objects.filter(project__students=profile.student).all()
    elif profile.type == "mentor":
        project_invitations = profile.mentor.pending_projects_invitations.all()
        projects_entering_requests = []
    else:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    unvisualized_stars = DiscussionStar.objects.filter(discussion__profile=request.user.profile, visualized=False)

    return Response(len(project_invitations) + len(projects_entering_requests) + len(unvisualized_stars))


@api_view(["PATCH"])
@login_required
def visualize_notifications(request):
    for star in DiscussionStar.objects.filter(discussion__profile=request.user.profile, visualized=False):
        star.visualized = True
        star.save()

    return Response("success")
