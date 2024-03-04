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
    list_display = [field.name for field in Unite._meta.fields  if field.name not in ['deleted', 'deleted_by_cascade']]

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
    save_as = True
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
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in PrixProduit._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]


    list_filter = (
        SafeDeleteAdminFilter,
    )


@admin.register(Planing)
class UniteMesureAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Planing._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]+['cumule',]
    list_filter = (
        SafeDeleteAdminFilter,
    )

    def cumule(self, obj):
        return obj.cumule


@admin.register(BonLivraison)
class BonLivraisonAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in BonLivraison._meta.fields if field.name not in ['qte_mois','deleted', 'deleted_by_cascade']]+['qte_precedente','qte_mois','qte_cumule',
                                                                                                                               'montant_precedent','montant_mois',
                                                                                                                               'montant_cumule']


    list_filter = (
        SafeDeleteAdminFilter,
    )
    def qte_precedente(self, obj):
        return obj.qte_precedente

    def qte_cumule(self, obj):
        return obj.qte_cumule

    def montant_mois(self, obj):
        return obj.montant_mois
    montant_mois.short_description = 'montant courant'
    def montant_precedent(self,obj):
        return obj.montant_precedent
    def montant_cumule(self,obj):
        return obj.montant_cumule
@admin.register(Factures)
class FacturesAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Factures._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]+['montant_precedent','montant_mois',
                                                                                                                               'montant_cumule']

    list_filter = (
        SafeDeleteAdminFilter,
    )

    def montant_mois(self, obj):
        return obj.montant_mois

    montant_mois.short_description = 'montant courant'
    def montant_precedent(self,obj):
        return obj.montant_precedent
    def montant_cumule(self,obj):
        return obj.montant_cumule

@admin.register(DetailFacture)
class DetailFactureAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in DetailFacture._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]

    list_filter = (
        SafeDeleteAdminFilter,
    )
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False










