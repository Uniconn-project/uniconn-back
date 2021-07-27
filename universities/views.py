from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Major, University
from .serializers import MajorSerializer01, UniversitySerializer01


@api_view(["GET"])
def get_universities_name_list(request):
    universities = University.objects.all()
    serializer = UniversitySerializer01(universities, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_majors_name_list(request):
    majors = Major.objects.all()
    serializer = MajorSerializer01(majors, many=True)

    return Response(serializer.data)
