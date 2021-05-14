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
def get_project_list(request):
    projects = Project.objects.all()[:30]
    serializer = ProjectSerializer01(projects, many=True)

    return Response(serializer.data)
