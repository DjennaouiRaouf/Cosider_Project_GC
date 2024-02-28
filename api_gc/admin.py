from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter
from simple_history.admin import SimpleHistoryAdmin

from api_gc.models import *


# Register your models here.
lp=20
@admin.register(Unite)
class UniteAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = ('id', 'libelle','date_ouverture','date_cloture')
    list_filter = (
        SafeDeleteAdminFilter,
    )






