from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Market, Project
from .serializers import MarketSerializer01, ProjectSerializer01


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
    readable_categories = request.query_params["categories"].split(";")
    markets = request.query_params["markets"].split(";")

    categories = Project.get_project_categories_values_from_readable(readable_categories)

    projects = Project.objects.filter(category__in=categories, markets__name__in=markets).distinct()
    projects = sorted(projects, key=lambda project: project.id)
    serializer = ProjectSerializer01(projects, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_projects_categories_list(request):
    return Response(Project.get_project_categories_choices())
