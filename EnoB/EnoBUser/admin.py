from django.contrib import admin
from .models import EnoB_user
# Register your models here.

class EnoB_userAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'birth', 'sex', )

admin.site.register(EnoB_user, EnoB_userAdmin)