from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')



# Create your models here.
@python_2_unicode_compatible
class FactorSell(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    factor_name = models.CharField(max_length=64, verbose_name=u'策略名称', editable=False)
    class_name = models.CharField(max_length=256, verbose_name=u'策略', editable=False)

    class Meta:
        verbose_name = u"卖策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '策略: %s, 名称: %s' % (self.factor_name, self.name)


@python_2_unicode_compatible
class FactorSellBreakXd(FactorSell):
    """
    海龟向上趋势突破买入策略:趋势突破定义为当天收盘价格超过N天内的最高价，超过最高价格作为买入信号买入股票持有
    """
    xd = models.CharField(verbose_name=u"周期", max_length=64)

    class Meta:
        verbose_name = u"海龟卖出"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'xd': %s, 'class': AbuFactorSellBreak}" % self.xd
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 周期: %s' % (self.name, self.xd)


@python_2_unicode_compatible
class FactorSellDoubleMa(FactorSell):
    """
    双均线卖出策略：
        双均线策略是量化策略中经典的策略之一，其属于趋势跟踪策略:
        1. 预设两条均线：如一个ma=5，一个ma=60, 5的均线被称作快线，60的均线被称作慢线
        2. 择时卖出策略中当快线下穿慢线（ma5下穿ma60）称为形成死叉卖点信号，卖出股票
    """
    slow_int = models.IntegerField(verbose_name=u"慢线")
    fast_int = models.IntegerField(verbose_name=u"快线")

    class Meta:
        verbose_name = u"双均线卖"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'slow': %d, 'fast': %d, 'class': AbuDoubleMaSell}" % (self.slow_int, self.fast_int)
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, 短周期: %s, 长周期: %s' % (self._meta.verbose_name, self.name, self.slow_int, self.fast_int)


