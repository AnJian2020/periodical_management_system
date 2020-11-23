from .celery import app as celery_app

# 将celery框架加载到Django
__all__=['celery_app']