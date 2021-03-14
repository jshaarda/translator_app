from django.contrib import admin
from .models import Word

class WordAdmin(admin.ModelAdmin):
    """Administration object for Dict model.
    Defines:
     - fields to be displayed in list view (list_display)
    """
    list_display = ('german', 'english', 'count')
    
# Register your models here.
admin.site.register(Word, WordAdmin)