from django.contrib import admin
from .models import *

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	exclude = ('created_at','updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	fiedls = '__all__'
