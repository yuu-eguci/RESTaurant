from rest_framework import viewsets, permissions
from shuumulator.models import Stock, TradingRecord, Trader
from shuumulator.serializers import (
    StockSerializer,
    TradingRecordSerializer,
    TraderSerializer
)


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
