from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter
from simple_history.admin import SimpleHistoryAdmin

from api_gc.models import *


# Register your models here.
lp=20


@admin.register(Images)
class ImagesAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Images._meta.fields  if field.name not in ['deleted', 'deleted_by_cascade']]

    list_filter = (
        SafeDeleteAdminFilter,
    )

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
    list_display = [field.name for field in Contrat._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]+['montant_ht','montant_ttc',]

    list_filter = (
        SafeDeleteAdminFilter,
    )

    def montant_ttc(self,obj):
        return obj.montant_ttc
    def montant_ht(self,obj):
        return obj.montant_ht

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
    list_display = [field.name for field in DQE._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]+['prix_unitaire','montant_qte',
                                                                                                                      ]


    list_filter = (
        SafeDeleteAdminFilter,
    )
    def montant_qte(self,obj):
        return obj.montant_qte
    def prix_unitaire(self,obj):
        return obj.prixProduit.prix_unitaire

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




@admin.register(Camion)
class CamionAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Camion._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]


    list_filter = (
        SafeDeleteAdminFilter,
    )

@admin.register(BonLivraison)
class BonLivraisonAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in BonLivraison._meta.fields if field.name not in ['qte','deleted', 'deleted_by_cascade']]+['qte','qte_cumule',
                                                                                                                               'montant',
                                                                                                                               'montant_cumule']


    list_filter = (
        SafeDeleteAdminFilter,
    )
    def qte(self, obj):
        return obj.qte

    def qte_cumule(self, obj):
        return obj.qte_cumule

    def montant(self, obj):
        return obj.montant
    def montant_cumule(self,obj):
        return obj.montant_cumule
@admin.register(Factures)
class FacturesAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Factures._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]+['montant_precedent','montant',
                                                                                                                               'montant_cumule','montant_rb',
                                                                                                                           'montant_rg','montant_facture_ht',
                                                                                                                           'montant_facture_ttc']

    list_filter = (
        SafeDeleteAdminFilter,
    )

    def montant(self, obj):
        return obj.montant
    def montant_rg(self, obj):
        return obj.montant_rg

    def montant_rb(self, obj):
        return obj.montant_rb

    def montant_facture_ht(self,obj):
        return obj.montant_facture_ht

    def montant_facture_ttc(self, obj):
        return obj.montant_facture_ttc

    montant.short_description = 'montant courant'
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










