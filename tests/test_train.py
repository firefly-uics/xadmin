from abuui.abupy import AbuBenchmark, AbuFactorAtrNStop, AbuFactorPreAtrNStop, AbuFactorCloseAtrNStop, \
    AbuFactorBuyBreak, \
    AbuCapital, ABuPickTimeExecute, AbuMetricsBase, AbuFactorSellBreak, ABuSymbolPd, EMarketDataSplitMode, Symbol, \
    EMarketTargetType, EMarketSubType, AbuKellyPosition
import numpy as np
import pandas as pd


def train():
    """
        8.1.4 对多支股票进行择时
        :return:
    """
    sell_factor1 = {'xd': 15, 'class': AbuFactorSellBreak}
    sell_factor2 = {'stop_loss_n': 1, 'stop_win_n': 3.0, 'class': AbuFactorAtrNStop}
    sell_factor3 = {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.0}
    sell_factor4 = {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
    sell_factors = [sell_factor1, sell_factor2, sell_factor3, sell_factor4]

    benchmark_kl_pd = ABuSymbolPd.make_kl_df('002396', data_mode=EMarketDataSplitMode.E_DATA_SPLIT_SE,

                                             start='2018-12-01')

    # benchmark_kl_pd = pd.read_csv('/Users/bailijiang/abu/data/csv/sz002396_20160104_20190203')

    print(benchmark_kl_pd)

    benchmark = AbuBenchmark(benchmark_kl_pd=benchmark_kl_pd)

    buy = {'xd': 7, 'class': AbuFactorBuyBreak}
    position = {'position': AbuKellyPosition}

    buy.update(**position)

    print('buy', buy)

    buy_factors = [buy]

    capital = AbuCapital(100000, benchmark)
    orders_pd, action_pd, all_fit_symbols_cnt = ABuPickTimeExecute.do_symbols_with_same_factors(['002396'],
                                                                                                benchmark,
                                                                                                buy_factors,
                                                                                                sell_factors,
                                                                                                capital,
                                                                                                show=True)

    metrics = AbuMetricsBase(orders_pd, action_pd, capital, benchmark)
    metrics.fit_metrics()

    print(orders_pd)

    metrics.plot_returns_cmp()


train()
