from django.contrib import admin
from .models import User

admin.site.site_header = "Academy Admin"
admin.site.register(User)
