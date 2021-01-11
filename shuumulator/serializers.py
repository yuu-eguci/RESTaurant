from rest_framework import serializers
from shuumulator.models import Stock, TradingRecord, Trader


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ['id', 'created_at', 'updated_at', 'code', 'name']


class TradingRecordSerializer(serializers.ModelSerializer):
    stock = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Stock.objects.all())
    trader = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Trader.objects.all())

    class Meta:
        model = TradingRecord
        fields = ['id',
                  'created_at',
                  'updated_at',
                  'stock',
                  'trader',
                  'bought_price',
                  'bought_at',
                  'sold_price',
                  'sold_at', ]


class TraderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trader
        fields = ['id', 'created_at', 'updated_at', 'name']
