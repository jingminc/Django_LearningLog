from django.contrib import admin

import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'learning_log.settings')
django.setup()

from learning_logs.models import Topic, Entry
admin.site.register(Entry)
admin.site.register(Topic)

