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


@admin.register(Contrat)
class ContratAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = ('id','date_signature', 'libelle','tva','rabais','rg','montant_ht','montant_ttc')
    list_filter = (
        SafeDeleteAdminFilter,
    )

@admin.register(Parametres)
class ParametresAdmin(SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = ('id','saisie_automatique', 'port')
    list_filter = (
        SafeDeleteAdminFilter,
    )
    def has_delete_permission(self, request, obj=None):
        return False





@admin.register(DQE)
class ContratAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = ()
    list_filter = (
        SafeDeleteAdminFilter,
    )








