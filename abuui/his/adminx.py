from __future__ import absolute_import
import xadmin
from xadmin import views
from .models import IDC
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction



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

# xadmin.sites.site.register(HostGroup, HostGroupAdmin)
# xadmin.sites.site.register(MaintainLog, MaintainLogAdmin)
# xadmin.sites.site.register(IDC, IDCAdmin)
# xadmin.sites.site.register(AccessRecord, AccessRecordAdmin)
