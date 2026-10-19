from rest_framework import serializers

from shuumulator.models import Stock, Trader, TradingRecord


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id", "created_at", "updated_at", "code", "name"]


class TradingRecordSerializer(serializers.ModelSerializer):
    # NOTE: stock と trader は ForeignKey なので、 ModelSerializer が自動で
    #       PrimaryKeyRelatedField (many=False) を作ってくれます。

    class Meta:
        model = TradingRecord
        fields = [
            "id",
            "created_at",
            "updated_at",
            "stock",
            "trader",
            "bought_price",
            "bought_at",
            "sold_price",
            "sold_at",
        ]


class TraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = ["id", "created_at", "updated_at", "name"]
