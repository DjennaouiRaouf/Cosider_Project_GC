from django.contrib import admin
from safedelete.admin import SafeDeleteAdmin

from api_gc.models import *


# Register your models here.
lp=20
@admin.register(Unite)
class OptionImpressionAdmin(SafeDeleteAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = ('id', 'libelle','date_ouverture','date_cloture')