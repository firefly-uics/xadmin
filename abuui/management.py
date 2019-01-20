from django.db.models.signals import post_syncdb
from base import models as base_app
from base.models import *

def setup_base(sender, **kwargs):
    Stock(co_name="锐捷网络", symbol="002735", market="SZ").save()

    post_syncdb.connect(setup_base, sender=base_app)
