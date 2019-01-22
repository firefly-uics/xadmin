# 快速使用
## 安装
```
// 下载源码
git clone https://github.com/sshwsfc/xadmin.git

cd xadmin

// 切换分支 支持 django2
git checkout django2

// 安装依赖
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

// 安装 xadmin
python setup.py install
```

## 启动demo
```
cd demo_app

// 创建 超级用户
./manage.py createsuperuser
// 更新 数据库
./manage.py makemigrations
// 更新 数据
./manage.py migrate
// 启动服务
./manage.py runserver
// 初始化数据
./manage.py loaddata initial_data.json
```

## 配置
### 配置文件
> {app}/settings.py
```
// 中文

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

```

## 创建 新项目
```
// 创建项目
django-admin startproject {project_name} 

cd {project_name}
```
### 修改 urls
> 文件 {project_name}/urls.py

#### 内容参考

``` python
# -*- coding: utf-8 -*-
# from django.conf.urls import include, url
from django.urls import include, path

# Uncomment the next two lines to enable the admin:
import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

from django.contrib import admin

urlpatterns = [
    path(r'', xadmin.site.urls)
]


// 创建 module
django-admin startapp {app_name}

cd {app_name}
```
### 修改 settings.py
> 文件 {project_name}/settings.py

#### 内容参考

``` python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'xadmin',
    'crispy_forms',
    'reversion',

    '{new_app}'
]
```


## 创建 app
```
// 创建 app
django-admin startapp {app_name} 

cd {app_name}
```

### 创建 module
#### 修改 models.py
> 文件 {app_name}/models.py

##### 内容参考

``` python
from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

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
```
#### 创建 adminx.py
> 文件 {app_name}/adminx.py

##### 内容参考
```
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

```

### 启动 project
> 参考 [启动demo](##启动demo)