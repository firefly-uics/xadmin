from __future__ import absolute_import

from django.forms import ModelMultipleChoiceField

import xadmin
from xadmin import views
from .models import IDC, Factor, Param
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction
from django.utils.translation import ugettext as _

ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


@xadmin.sites.register(IDC)
class IDCAdmin(object):
    list_display = ("name", "description", "create_time", "contact", "telphone", "address", "customer_id")
    list_display_links = ("name",)
    wizard_form_list = [
        ("First's Form", ("name", "description")),
        ("Second Form", ("contact", "telphone", "address")),
        ("Thread Form", ("customer_id",))
    ]
    search_fields = ["name", "description", "contact", "telphone", "address"]
    list_filter = [
        "name"
    ]
    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]
    relfield_style = "fk-select"
    reversion_enable = True

    actions = [BatchChangeAction, ]
    batch_fields = ("contact", "description", "address", "customer_id")


@xadmin.sites.register(Factor)
class FactorAdmin(object):
    list_display = ("name", "description", "create_time")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    style_fields = {'params': 'checkbox-inline'}

    reversion_enable = True


@xadmin.sites.register(Param)
class ParamAdmin(object):
    list_display = ("name", "description")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]
    relfield_style = "fk-select"

    reversion_enable = True

# xadmin.sites.site.register(HostGroup, HostGroupAdmin)
# xadmin.sites.site.register(MaintainLog, MaintainLogAdmin)
# xadmin.sites.site.register(IDC, IDCAdmin)
# xadmin.sites.site.register(AccessRecord, AccessRecordAdmin)
