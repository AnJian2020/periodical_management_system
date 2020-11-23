import os
from celery import Celery

# 获取settings.py的配置信息
os.environ.setdefault('DJANGO_SETTINGS_MODULE','periodical_management_system.settings')

# 定义celery对象，并且将项目配置信息加载到对象中
app=Celery('periodical_management_system')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()