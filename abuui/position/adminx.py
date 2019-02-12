from __future__ import absolute_import

from django.utils.translation import ugettext as _

import xadmin
from .models import KellyPosition

ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}


@xadmin.sites.register(KellyPosition)
class KellyPositionAdmin(object):
    list_display = ("name", "win_rate", "gains_mean", "losses_mean")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True