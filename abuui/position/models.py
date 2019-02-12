from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# Create your models here.
@python_2_unicode_compatible
class Position(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    position_name = models.CharField(max_length=64, verbose_name=u'仓位策略名称', editable=False)
    class_name = models.CharField(max_length=256, verbose_name=u'仓位策略', editable=False)

    class Meta:
        verbose_name = u"仓位策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '仓位策略: %s, 名称: %s' % (self.position_name, self.name)


@python_2_unicode_compatible
class KellyPosition(Position):
    """
    kelly仓位管理类 通过kelly公司计算仓位, fit_position计算的结果是买入多少个单位（股，手，顿，合约）
    """
    win_rate = models.FloatField(verbose_name=u"默认kelly仓位胜率0.50")
    gains_mean = models.FloatField(verbose_name=u"默认平均获利期望0.10")
    losses_mean = models.FloatField(verbose_name=u"默认平均亏损期望0.05")

    class Meta:
        verbose_name = u"kelly仓位管理"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'win_rate': %s,'gains_mean': %s,'losses_mean': %s, 'class': AbuKellyPosition}" % (self.win_rate, self.gains_mean, self.losses_mean)
        self.position_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 胜率: %s, 平均获利期望: %s, 平均亏损期望: %s' % (self.name, self.win_rate, self.gains_mean, self.losses_mean)
