from django.db import models


class Stock(models.Model):
    """
    株式銘柄
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code = models.TextField()
    name = models.TextField()

    class Meta:
        ordering = ['name']


class TradingRecord(models.Model):
    """
    取引記録
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    trader = models.ForeignKey('Trader', on_delete=models.CASCADE)
    bought_price = models.DecimalField(decimal_places=2, max_digits=10)
    bought_at = models.DateTimeField()
    sold_price = models.DecimalField(decimal_places=2, max_digits=10)
    sold_at = models.DateTimeField()

    class Meta:
        ordering = ['updated_at']
        # HACK: インデックスはこう設定できます。
        # indexes = [
        #     models.Index(fields=['last_name', 'first_name']),
        #     models.Index(fields=['first_name'], name='first_name_idx'),
        # ]


class Trader(models.Model):
    """
    トレーダーの情報
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.TextField()

    class Meta:
        ordering = ['updated_at']
