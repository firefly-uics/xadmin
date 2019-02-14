from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

import numpy as np

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# Create your models here.
@python_2_unicode_compatible
class PickStock(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    pick_stock_name = models.CharField(max_length=64, verbose_name=u'择股因子名称', editable=False)
    class_name = models.CharField(max_length=256, verbose_name=u'择股因子策略', editable=False)

    xd = models.SmallIntegerField(verbose_name=u"周期",
                                  choices=[(i, "%s " % i) for i in range(1, 252, 1)],
                                  validators=[MinValueValidator(1), MaxValueValidator(252), ], default=252)

    REVERSED_SELECT = (
        (True, u"反转选股结果"),
        (False, u"不反转"),
    )

    reversed = models.BooleanField(verbose_name=u"反转结果", choices=REVERSED_SELECT, )

    class Meta:
        verbose_name = u"择股因子"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '择股因子: %s, 名称: %s' % (self.pick_stock_name, self.name)

    def delegate_class(self):
        """子类因子所委托的具体因子类"""
        pass


@python_2_unicode_compatible
class PriceMinMaxPickStock(PickStock):
    PRICE_MIN_CK_SELECT = (
        (True, u"否"),
        (False, u"是"),
    )

    """
    价格选股因子策略：
      根据交易目标的一段时间内收盘价格的最大，最小值进行选股，选中规则：
      1. 交易目标最小价格 > 最小价格阀值
      2. 交易目标最大价格 < 最大价格阀值
    """
    price_min = models.FloatField(verbose_name=u"最小:", default=15)
    price_min_ck = models.BooleanField(verbose_name=u"使用最小阀值", choices=PRICE_MIN_CK_SELECT,)
    price_max = models.FloatField(verbose_name=u"最大:", default=50)
    price_max_ck = models.BooleanField(verbose_name=u"使用最大阀值", choices=PRICE_MIN_CK_SELECT, )

    class Meta:
        verbose_name = u"价格选股"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        price_min_str = self.price_min if self.price_min_ck else -np.inf
        price_max_str = self.price_max if self.price_max_ck else np.inf

        self.class_name = "{'xd': %d,'reversed': %s,'threshold_price_min': %f,'threshold_price_max': %s, 'class': %s}" % (
            self.xd, self.reversed, price_min_str, price_max_str, self.delegate_class())
        self.pick_stock_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 价格选股最大:%s 最小:%s ,周期:%s ,反转:%s ' % (
            self.name, self.price_max, self.price_min, self.xd, self.reversed)

    def delegate_class(self):
        return 'AbuPickStockPriceMinMax'
