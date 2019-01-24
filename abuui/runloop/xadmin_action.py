import abupy

from django.db import connection

from abuui import settings
from base.models import Stock
from .models import Orders
from xadmin.plugins.actions import BaseActionView
from abupy import AbuFactorBuyBreak, AbuBenchmark, AbuCapital, AbuPickTimeWorker, ABuPickTimeExecute, ABuTradeExecute, AbuMetricsBase, AbuFactorSellBreak, AbuFactorAtrNStop, AbuFactorCloseAtrNStop, \
    AbuFactorPreAtrNStop

from django.db import connection

from django.conf import settings
import sqlalchemy
from sqlalchemy.engine.url import URL


class MyAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "change_sss"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = u'回测 %(verbose_name_plural)s'  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'

    abupy.env.disable_example_env_ipython()

    def do_action(self, queryset):
        for obj in queryset:
            obj.status = 'run...'
            obj.save()

            buy_factors = []

            for factor_buy in obj.factor_buys.all():
                buy_factors.append(eval(factor_buy.get_class_name_display()))

            """
                8.1.4 对多支股票进行择时
                :return:
            """
            sell_factor1 = eval("{'xd': 120, 'class': AbuFactorSellBreak}")
            sell_factor2 = {'stop_loss_n': 0.5, 'stop_win_n': 3.0, 'class': AbuFactorAtrNStop}
            sell_factor3 = {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.0}
            sell_factor4 = {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
            sell_factors = [sell_factor1, sell_factor2, sell_factor3, sell_factor4]
            benchmark = AbuBenchmark()
            buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
                           {'xd': 42, 'class': AbuFactorBuyBreak}]

            choice_symbols = ['002396']  # , '002230']
            capital = AbuCapital(1000000, benchmark)
            orders_pd, action_pd, all_fit_symbols_cnt = ABuPickTimeExecute.do_symbols_with_same_factors(choice_symbols,
                                                                                                        benchmark,
                                                                                                        buy_factors,
                                                                                                        sell_factors,
                                                                                                        capital,
                                                                                                        show=False)

            metrics = AbuMetricsBase(orders_pd, action_pd, capital, benchmark)
            metrics.fit_metrics()


            for symbol in choice_symbols:
                stock = Stock.objects.filter(symbol=symbol)
                orders_pd.loc[orders_pd['symbol'] == ('sz%s' % symbol), 'stock_id'] = stock[0].id

            orders_pd['run_loop_group_id'] = obj.id

            orders = Orders.objects.filter(run_loop_group_id=obj.id)
            if len(orders) > 0:
                orders.delete()

            for index, row in orders_pd.iterrows():
                dictObject = row.to_dict()
                Orders.objects.create(**dictObject)


            str = ''

            str += '买入后卖出的交易数量:%s \n' % metrics.order_has_ret.shape[0]
            str += '胜率:%f \n' % (metrics.win_rate * 100)

            # 其实我们做的只有这一部分 ********
            obj.status = 'done'
            obj.description = str
            obj.save()
        # return HttpResponse('{"status": "success", "msg": "error"}', content_type='application/json')
