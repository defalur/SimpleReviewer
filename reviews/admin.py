from django.contrib import admin

from .models import Review, File, Comment

# Register your models here.
admin.site.register(Review)
admin.site.register(File)
admin.site.register(Comment)

