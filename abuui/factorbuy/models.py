from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# Create your models here.
@python_2_unicode_compatible
class FactorBuy(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    factor_name = models.CharField(max_length=64, verbose_name=u'策略名称', editable=False)
    class_name = models.CharField(max_length=256, verbose_name=u'策略', editable=False)

    class Meta:
        verbose_name = u"买策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '策略: %s, 名称: %s' % (self.factor_name, self.name)

@python_2_unicode_compatible
class FactorBuyBreakXd(FactorBuy):
    """
    海龟向上趋势突破买入策略:趋势突破定义为当天收盘价格超过N天内的最高价，超过最高价格作为买入信号买入股票持有
    """
    xd = models.IntegerField(verbose_name=u"周期")

    class Meta:
        verbose_name = u"海龟买入"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'xd': %s, 'class': AbuFactorBuyBreak}" % self.xd
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 周期: %s' % (self.name, self.xd)


@python_2_unicode_compatible
class FactorBuyDoubleMa(FactorBuy):
    """
    动态自适应双均线买入策略：
    双均线策略是量化策略中经典的策略之一，其属于趋势跟踪策略:
        1. 预设两条均线：如一个ma=5，一个ma=60, 5的均线被称作快线，60的均线被称作慢线
        2. 择时买入策略中当快线上穿慢线（ma5上穿ma60）称为形成金叉买点信号，买入股票
        3. 自适应动态慢线，不需要输入慢线值，根据走势震荡套利空间，寻找合适的ma慢线
        4. 自适应动态快线，不需要输入快线值，根据慢线以及大盘走势，寻找合适的ma快线
    """
    slow_int = models.IntegerField(verbose_name=u"慢线(-1:为自动)")
    fast_int = models.IntegerField(verbose_name=u"快线(-1:为自动)")

    class Meta:
        verbose_name = u"双均线买"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'slow': %d, 'fast': %d, 'class': AbuDoubleMaBuy}" % (self.slow_int, self.fast_int)
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, 短周期: %s, 长周期: %s' % (self._meta.verbose_name, self.name, self.slow_int, self.fast_int)

@python_2_unicode_compatible
class FactorBuySDBreak(FactorBuyBreakXd):
    """
    参照大盘走势向上趋势突破买入策略：
        在海龟突破基础上，参照大盘走势，进行降低交易频率，提高系统的稳定性处理，当大盘走势震荡时封锁交易，
        当大盘走势平稳时再次打开交易，每一个月计算一次大盘走势是否平稳
    """
    poly = models.IntegerField(verbose_name=u"拟合")

    class Meta:
        verbose_name = u"平稳突破买"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'poly': %d, 'xd': %d, 'class': AbuSDBreak}" % (self.poly, self.xd)
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, %s 拟合 %s 天趋势突破参照大盘' % (self._meta.verbose_name, self.name, self.poly, self.xd)

