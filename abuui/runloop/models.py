from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, ugettext

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# Create your models here.
@python_2_unicode_compatible
class FactorBuy(models.Model):
    name = models.TextField(max_length=64, verbose_name=u'名称')

    class Meta:
        verbose_name = u"买策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '策略名称: %s' % self.name

@python_2_unicode_compatible
class FactorBuyBreakXd(FactorBuy):
    xd = models.CharField(verbose_name=u"周期", max_length=64)

    class Meta:
        verbose_name = u"海龟策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '策略名称: %s, 周期: %s' % (self.name, self.xd)


@python_2_unicode_compatible
class RunLoopGroup(models.Model):
    name = models.TextField(max_length=64)
    description = models.TextField()
    factor_buys = models.ManyToManyField(
        FactorBuy, verbose_name=u'FactorBuys', blank=True, related_name='factor_buy_groups')

    class Meta:
        verbose_name = u"RunLoopGroup"
        verbose_name_plural = verbose_name
