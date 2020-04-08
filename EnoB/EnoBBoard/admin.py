from django.contrib import admin
from .models import EnoB_Board

# Register your models here.
class EnoB_BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'registered_dttm', )

admin.site.register(EnoB_Board, EnoB_BoardAdmin)

