import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from projects.models import Market
from rest_framework.decorators import api_view
from rest_framework.response import Response
from universities.models import Major, University

from .models import Mentor, Profile, Student

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
def get_is_auth(request):
    return Response({"is_auth": request.user.is_authenticated})
