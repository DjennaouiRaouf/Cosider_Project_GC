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
    list_display = [field.name for field in Unite._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]

    list_filter = (
        SafeDeleteAdminFilter,
    )


@admin.register(Contrat)
class ContratAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Contrat._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]

    list_filter = (
        SafeDeleteAdminFilter,
    )

@admin.register(Parametres)
class ParametresAdmin(SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Parametres._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]

    list_filter = (
        SafeDeleteAdminFilter,
    )
    def has_delete_permission(self, request, obj=None):
        return False




@admin.register(Clients)
class ClientsAdmin(SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Clients._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]

    list_filter = (
        SafeDeleteAdminFilter,
    )






@admin.register(DQE)
class ContratAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in DQE._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]


    list_filter = (
        SafeDeleteAdminFilter,
    )


@admin.register(UniteMesure)
class UniteMesureAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in UniteMesure._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]


    list_filter = (
        SafeDeleteAdminFilter,
    )


@admin.register(Produits)
class UniteMesureAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Produits._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]


    list_filter = (
        SafeDeleteAdminFilter,
    )

@admin.register(PrixProduit)
class UniteMesureAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in PrixProduit._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]


    list_filter = (
        SafeDeleteAdminFilter,
    )










