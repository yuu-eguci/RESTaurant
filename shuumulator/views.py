from rest_framework import viewsets, permissions, status
from shuumulator.models import Stock, TradingRecord, Trader
from shuumulator.serializers import (
    StockSerializer,
    TradingRecordSerializer,
    TraderSerializer
)
from rest_framework.decorators import api_view
from rest_framework.response import Response


class StockViewSet(viewsets.ModelViewSet):
    """
    株式銘柄
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]


class TradingRecordViewSet(viewsets.ModelViewSet):
    """
    取引記録
    """
    queryset = TradingRecord.objects.all()
    serializer_class = TradingRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class TraderViewSet(viewsets.ModelViewSet):
    """
    トレーダーの情報
    """
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def call_executetrade(request):

    # python manage.py executetrade と同じコールを行います。
    from django.core import management
    result = management.call_command('executetrade')

    return Response({'result': result}, status=status.HTTP_200_OK)
