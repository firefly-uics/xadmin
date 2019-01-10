from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, ugettext

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# Create your models here.
class FactorBuy(models.Model):
    _name_default = ''
    name = models.TextField(max_length=64, default=_name_default, editable=False)
    xd = models.TextField(verbose_name=u"周期")

    create_time = models.DateField(auto_now=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_(u"user"), blank=True, null=True)

    def set_name_default(self, name_default):
        self._name_default = name_default

    class Meta:
        abstract = True


class FactorBuyBreak(models.Model):
    """
    正向突破买入择时类
    """

    class Meta:
        abstract = True


# Create your models here.
@python_2_unicode_compatible
class FactorBuyBreakXd(FactorBuyBreak, FactorBuy):
    super.set_name_default('hai')
    name = models.TextField(max_length=64, default='海龟策略', editable=False)

    class Meta:
        verbose_name = u"海龟策略"
        verbose_name_plural = verbose_name
