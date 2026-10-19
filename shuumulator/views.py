from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from shuumulator.models import Stock, Trader, TradingRecord
from shuumulator.serializers import (
    StockSerializer,
    TraderSerializer,
    TradingRecordSerializer,
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


# NOTE: 誰でも command を叩けないよう、管理ユーザ (staff) 限定にしています。
#       リンクを開いただけで動かないよう (CSRF 対策)、 POST にしています。
@api_view(["POST"])
@permission_classes([permissions.IsAdminUser])
def call_executetrade(request):

    # python manage.py executetrade と同じコールを行います。
    from django.core import management

    result = management.call_command("executetrade")

    return Response({"result": result}, status=status.HTTP_200_OK)
