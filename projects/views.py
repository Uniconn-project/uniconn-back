import base64

from django.core.files.base import ContentFile
from jwt_auth.decorators import login_required
from profiles.models import Mentor, Student
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Market, Project
from .serializers import MarketSerializer01, ProjectSerializer01, ProjectSerializer02


@api_view(["GET"])
def get_markets_name_list(request):
    markets = Market.objects.all()
    serializer = MarketSerializer01(markets, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_projects_list(request):
    projects = Project.objects.all()[:30]
    serializer = ProjectSerializer01(projects, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_filtered_projects_list(request):
    categories = request.query_params["categories"].split(";")
    markets = request.query_params["markets"].split(";")

    projects = Project.objects.filter(category__in=categories, markets__name__in=markets).distinct()
    projects = sorted(projects, key=lambda project: project.id)
    serializer = ProjectSerializer01(projects, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_projects_categories_list(request):
    categories = [
        {"value": category[0], "readable": category[1]} for category in Project.get_project_categories_choices()
    ]
    return Response(categories)


@api_view(["POST"])
@login_required
def create_project(request):
    profile = request.user.profile

    if profile.type != "student":
        return Response("Somente universitários podem criar projetos!", status=status.HTTP_401_UNAUTHORIZED)

    try:
        category = request.data["category"]
        name = request.data["name"].strip()
        slogan = request.data["slogan"].strip()
        markets = request.data["markets"]
    except:
        return Response("Os dados enviados são inválidos!", status=status.HTTP_400_BAD_REQUEST)

    if name == "":
        return Response("O nome do projeto não pode estar em branco!", status=status.HTTP_400_BAD_REQUEST)

    if slogan == "":
        return Response("O slogan do projeto não pode estar em branco!", status=status.HTTP_400_BAD_REQUEST)

    if len(markets) == 0:
        return Response("Selecione pelo menos um mercado!", status=status.HTTP_400_BAD_REQUEST)

    if category not in Project.get_project_categories_choices(index=0):
        return Response("Categoria do projeto inválida!", status=status.HTTP_400_BAD_REQUEST)

    project = Project.objects.create(category=category, name=name, slogan=slogan)
    project.markets.set(Market.objects.filter(name__in=markets))
    project.students.add(profile.student)
    project.save()

    return Response("Project created with success")


@api_view(["GET"])
def get_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Project not found", status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer02(project)

    return Response(serializer.data)


@api_view(["PUT"])
@login_required
def edit_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Project not found", status=status.HTTP_404_NOT_FOUND)

    if request.user.profile.type != "student":
        return Response("Only students are allowed to edit the project!", status=status.HTTP_401_UNAUTHORIZED)

    if not request.user.profile.student in project.students.all():
        return Response("Only project members can edit it!", status=status.HTTP_401_UNAUTHORIZED)

    try:
        image = request.data["image"]
        name = request.data["name"]
        category = request.data["category"]
        slogan = request.data["slogan"]
        markets = request.data["markets"]
    except:
        return Response("Invalid data!", status=status.HTTP_400_BAD_REQUEST)

    if image is not None:
        format, imgstr = image.split(";base64,")
        img_format = format.split("/")[-1]
        project_image = ContentFile(base64.b64decode(imgstr), name=project.name + img_format)
        project.image = project_image

    project.name = name
    project.category = category
    project.slogan = slogan
    project.markets.set(Market.objects.filter(name__in=markets))

    project.save()

    return Response("Project edited with success")


@api_view(["PUT"])
@login_required
def invite_students_to_project(request, type, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Project not found", status=status.HTTP_404_NOT_FOUND)

    if request.user.profile.type != "student":
        return Response(
            "Only students are allowed to invite users to the project!", status=status.HTTP_401_UNAUTHORIZED
        )

    if not request.user.profile.student in project.students.all():
        return Response("Only project members can invite users to it!", status=status.HTTP_401_UNAUTHORIZED)

    try:
        usernames = request.data[type]
    except:
        return Response("Invalid data!", status=status.HTTP_400_BAD_REQUEST)

    if type == "students":
        students = Student.objects.filter(profile__user__username__in=usernames)
        project.pending_invited_students.add(*students)
    elif type == "mentors":
        mentors = Mentor.objects.filter(profile__user__username__in=usernames)
        project.pending_invited_mentors.add(*mentors)
    else:
        return Response("Invalid data!", status=status.HTTP_400_BAD_REQUEST)

    project.save()

    return Response("Users invited to project with success!")
