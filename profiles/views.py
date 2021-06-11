import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from jwt_auth.decorators import login_required
from projects.models import Market
from projects.serializers import ProjectSerializer01, ProjectSerializer03
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from universities.models import Major, University

from .models import Mentor, Profile, Student
from .serializers import ProfileSerializer01, ProfileSerializer02, ProfileSerializer03

User = get_user_model()


@api_view(["POST"])
def signup_view(request, user_type):
    """
    All user types constrains:
    -no empty field
    -password length must be at least 5
    -age can't be less than 0 or more than 150
    -username and email can't already be in use

    Student user type constrains:
    -university and major must already be in the database

    Mentor user type constrains:
    -all markets submited must already be in the database
    """

    if user_type not in ["student", "mentor"]:
        return Response("Tipo de usuário inválido!")

    data = request.data

    username = data["username"]
    email = data["email"]
    password = data["password"]
    passwordc = data["passwordc"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    birth_date = data["birth_date"]

    # user_type == student
    university_name = data["university"] if "university" in data.keys() else ""
    major_name = data["major"] if "major" in data.keys() else ""

    # user_type == mentor
    markets_name = data["markets"] if "markets" in data.keys() else []

    # error messages that repeat in the code
    BLANK_FIELD_ERR_MSG = "Todos os campos devem ser preenchidos!"
    INVALID_BIRTH_DATE_ERR_MSG = "Data de nascimento inválida!"

    if not (
        len(username)
        and len(email)
        and len(password)
        and len(passwordc)
        and len(first_name)
        and len(last_name)
        and len(birth_date)
    ):
        return Response(BLANK_FIELD_ERR_MSG)

    if password != passwordc:
        return Response("As senhas devem ser iguais!")

    if len(password) < 5:
        return Response("A senha deve ter pelo menos 5 caracteres!")

    if User.objects.filter(username=username).exists():
        return Response("Nome de usuário já utilizado!")

    if User.objects.filter(email=email).exists():
        return Response("Email já utilizado!")

    try:
        age = datetime.date.today() - datetime.date.fromisoformat(birth_date)

        if age <= datetime.timedelta(days=0) or age >= datetime.timedelta(weeks=7800):
            return Response(INVALID_BIRTH_DATE_ERR_MSG)
    except:
        return Response(INVALID_BIRTH_DATE_ERR_MSG)

    if user_type == "student":
        if not (len(university_name) or len(major_name)):
            return Response(BLANK_FIELD_ERR_MSG)
        if not University.objects.filter(name=university_name).exists():
            return Response("Universidade não registrada na base de dados!")
        if not Major.objects.filter(name=major_name.lower()).exists():
            return Response("Curso não registrado na base de dados!")
    elif user_type == "mentor":
        if not len(markets_name):
            return Response(BLANK_FIELD_ERR_MSG)

        markets = []

        for market_name in markets_name:
            try:
                market = Market.objects.get(name=market_name.lower())
                markets.append(market)
            except ObjectDoesNotExist:
                return Response("Mercado não registrado na base de dados!")

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

        return Response("success")

    elif user_type == "mentor":
        mentor = Mentor.objects.create(profile=user.profile)

        for market in markets:
            market.mentors.add(mentor)

        return Response("success")

    return Response("Ocorreu um erro, por favor tente novamente.")


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
        return Response("There isn't any user with such username")


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

    if profile.type == "student":
        project_invitations = profile.student.pending_projects_invitations
    elif profile.type == "mentor":
        project_invitations = profile.mentor.pending_projects_invitations

    serializer = ProjectSerializer03(project_invitations, many=True)

    return Response({"projects": serializer.data})


@api_view(["GET"])
@login_required
def get_notifications_number(request):
    profile = request.user.profile

    if profile.type == "student":
        project_invitations = profile.student.pending_projects_invitations.all()
    elif profile.type == "mentor":
        project_invitations = profile.mentor.pending_projects_invitations.all()

    return Response(len(project_invitations))
