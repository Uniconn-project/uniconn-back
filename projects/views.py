from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Market
from .serializers import MarketSerializer01


@api_view(["GET"])
def get_markets_name_list(request):
    markets = Market.objects.all()
    serializer = MarketSerializer01(markets, many=True)

    return Response(serializer.data)
