from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import University
from .serializers import UniversitySerializer01


@api_view(["GET"])
def get_universities_name_list(request):
    universities = University.objects.filter(is_active=True)
    serializer = UniversitySerializer01(universities, many=True)

    return Response(serializer.data)
