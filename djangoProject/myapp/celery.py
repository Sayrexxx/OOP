from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# установите настройки по умолчанию Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

app = Celery('myapp')


# используйте строку конфигурации, чтобы настроить Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# автоматически обнаруживайте задачи в файлах tasks.py всех приложений
app.autodiscover_tasks()
