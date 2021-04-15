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
    data = request.data
    username = data["username"]
    password = data["password"]
    passwordc = data["passwordc"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    birth_date = data["birth_date"]
    email = data["email"]

    if not (
        len(username)
        or len(password)
        or len(passwordc)
        or len(first_name)
        or len(last_name)
        or len(birth_date)
        or len(email)
    ):
        return Response("Todos os campos devem ser preenchidos!")

    if password != passwordc:
        return Response("As senhas devem ser iguais!")

    if User.objects.filter(username=username).exists():
        return Response("Nome de usuário já utilizado!")

    if Profile.objects.filter(email=email).exists():
        return Response("Email já utilizado!")

    age = datetime.date.today() - datetime.date.fromisoformat(birth_date)

    if age <= datetime.timedelta(days=0) or age >= datetime.timedelta(days=54750):
        return Response("Data de nascimento inválida!")

    user = User.objects.create(username=username.lower(), password=password)

    user.profile.first_name = first_name
    user.profile.last_name = last_name
    user.profile.birth_date = birth_date
    user.profile.save()

    if user_type == "student":
        university_name = data["university"]
        major_name = data["major"]

        try:
            university = University.objects.get(name=university_name)
        except ObjectDoesNotExist:
            return Response("Universidade não registrada!")

        major, created = Major.objects.get_or_create(name=major_name)

        Student.objects.create(profile=user.profile, university=university, major=major)

        return Response("success")

    elif user_type == "mentor":
        markets = data["markets"]
        mentor = Mentor.objects.create(profile=user.profile)

        for market_name in markets:
            market, created = Market.objects.get_or_create(name=market_name.lower())
            market.mentors.add(mentor)

        return Response("success")

    return Response("Ocorreu um erro, por favor tente novamente.")
