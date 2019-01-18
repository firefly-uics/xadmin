from django.http import HttpResponse
from xadmin.plugins.actions import BaseActionView
from abupy import AbuFactorBuyBreak,AbuBenchmark, AbuCapital, AbuKLManager, AbuPickTimeWorker, ABuTradeProxy,ABuPickTimeExecute,     ABuTradeExecute,AbuMetricsBase,AbuFactorSellBreak,AbuFactorAtrNStop,AbuFactorCloseAtrNStop,AbuFactorPreAtrNStop
import matplotlib.pyplot as plt

class MyAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "change_sss"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = u'Test selected %(verbose_name_plural)s'  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'

    def do_action(self, queryset):

        for obj in queryset:
            obj.status = 'run...'
            obj.save()

            """
                        8.1.4 对多支股票进行择时
                        :return:
                    """
            sell_factor1 = {'xd': 120, 'class': AbuFactorSellBreak}
            sell_factor2 = {'stop_loss_n': 0.5, 'stop_win_n': 3.0, 'class': AbuFactorAtrNStop}
            sell_factor3 = {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.0}
            sell_factor4 = {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
            sell_factors = [sell_factor1, sell_factor2, sell_factor3, sell_factor4]
            benchmark = AbuBenchmark()
            buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
                           {'xd': 42, 'class': AbuFactorBuyBreak}]

            choice_symbols = ['usTSLA', 'usNOAH']
            capital = AbuCapital(1000000, benchmark)
            orders_pd, action_pd, all_fit_symbols_cnt = ABuPickTimeExecute.do_symbols_with_same_factors(choice_symbols,
                                                                                                        benchmark,
                                                                                                        buy_factors,
                                                                                                        sell_factors,
                                                                                                        capital,
                                                                                                        show=False)

            metrics = AbuMetricsBase(orders_pd, action_pd, capital, benchmark)
            metrics.fit_metrics()

            str = ''

            str += '买入后卖出的交易数量:%s \n' % metrics.order_has_ret.shape[0]
            str += '胜率:%f \n' % (metrics.win_rate * 100)

            # 其实我们做的只有这一部分 ********
            obj.status = 'done'
            obj.description = str
            obj.save()
        # return HttpResponse('{"status": "success", "msg": "error"}', content_type='application/json')

