from django.db import models
from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.db.models.manager import EmptyManager
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, ugettext

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

FACTOR_TYPES = (
    ('buy', u"买"),
    ('sell', u"卖"),
)


# Create your models here.
@python_2_unicode_compatible
class IDC(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    contact = models.CharField(max_length=32)
    telphone = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    customer_id = models.CharField(max_length=128)
    groups = models.ManyToManyField(Group)  # many

    create_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"IDC"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class Param(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Param"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class Factor(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    factor_type = models.CharField(max_length=32, choices=FACTOR_TYPES)

    create_time = models.DateField(auto_now=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_(u"user"), blank=True, null=True)
    params = models.ManyToManyField(
        Param, verbose_name=u'Params', blank=True, related_name='factors')

    def __str__(self):
        return self.name

    # @property
    # def factor_params(self):
    #     return self._factor_params

    class Meta:
        verbose_name = u"Factor"
        verbose_name_plural = verbose_name
