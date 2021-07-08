from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "PATCH", "PUT", "POST", "DELETE"])
def http_404_not_found(request):
    return Response("Rota não encontrada!", status=status.HTTP_404_NOT_FOUND)
