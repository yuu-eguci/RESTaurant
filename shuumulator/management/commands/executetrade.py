from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Shuumulator executetrade'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        iso = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        tzinfo = now.tzinfo
        self.stdout.write(f'timezone.now(): {iso}, tzinfo: {tzinfo}')

        return main()


def main():

    # 銘柄の情報を収集します。

    # 買うかどうかを判断します。(2,000円以下とかを考えています。)

    # Stock マスタになければ追加します。(Stock 追加)

    # 現在持っていないものは購入します。(TradingRecord 追加)

    # 現在の勝率を計算し、利確ラインと損切りラインを算出します。

    # ラインを超えている Stock があれば売却します。(TradingRecord 更新)

    return
