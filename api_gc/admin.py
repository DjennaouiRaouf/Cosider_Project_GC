from django.contrib import admin
from import_export.admin import ImportExportMixin
from api_gc.forms import *
from api_gc.models import *
from api_gc.resources import *

# Register your models here.
lp=20


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Images._meta.fields  if field.name not in ['']]



@admin.register(Tva)
class TvaAdmin(ImportExportMixin,admin.ModelAdmin):
    list_per_page = lp

    list_display = [field.name for field in Tva._meta.fields  if field.name not in ['']]


@admin.register(Avances)
class AvancesAdmin(ImportExportMixin, admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Avances._meta.fields  if field.name not in ['']]+['montant_cumule']

    def montant_cumule(self,obj):
        return obj.montant_cumule


@admin.register(Unite)
class UniteAdmin(ImportExportMixin, admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Unite._meta.fields  if field.name not in ['']]

    




@admin.register(Contrat)
class ContratAdmin(ImportExportMixin, admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Contrat._meta.fields if field.name not in ['']]+['montant_ht','montant_ttc',]

    

    def montant_ttc(self,obj):
        return obj.montant_ttc
    def montant_ht(self,obj):
        return obj.montant_ht

@admin.register(Config)
class ParametresAdmin(ImportExportMixin, admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Config._meta.fields if field.name not in ['']]

    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register( ModePaiement)
class ModePaiementAdmin(ImportExportMixin,admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in ModePaiement._meta.fields if field.name not in ['']]


@admin.register(TypePrix)
class TypePrixAdmin(ImportExportMixin, admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in TypePrix._meta.fields if field.name not in ['']]


@admin.register(Clients)
class ClientsAdmin(ImportExportMixin, admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Clients._meta.fields if field.name not in ['']]

    


@admin.register(Encaissement)
class EncaissementAdmin(ImportExportMixin, admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Encaissement._meta.fields if field.name not in ['']]+['montant_creance',
                                                                                                                        ]


    
    def montant_creance(self,obj):
        return obj.montant_creance








@admin.register(DQE)
class ContratAdmin(ImportExportMixin, admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in DQE._meta.fields if field.name not in ['']]+['prix_unitaire','montant_qte',
                                                                                         'montant_at'
                                                                                                                      ]


    
    def montant_qte(self,obj):
        return obj.montant_qte
    def prix_unitaire(self,obj):
        return obj.prixProduit.prix_unitaire
    def montant_at(self,obj): # montant + transport
        return obj.montant_qte_t

@admin.register(UniteMesure)
class UniteMesureAdmin(ImportExportMixin, admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in UniteMesure._meta.fields if field.name not in ['']]


    


@admin.register(Produits)
class UniteMesureAdmin(ImportExportMixin, admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Produits._meta.fields if field.name not in ['']]


    

@admin.register(PrixProduit)
class UniteMesureAdmin(ImportExportMixin, admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in PrixProduit._meta.fields if field.name not in ['']]+['index_prix']

    def index_prix(self, obj):
        return obj.index_prix,


    


@admin.register(Planing)
class UniteMesureAdmin(ImportExportMixin, admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Planing._meta.fields if field.name not in ['']]+['cumule',]
    

    def cumule(self, obj):
        return obj.cumule




@admin.register(Camion)
class CamionAdmin(ImportExportMixin, admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Camion._meta.fields if field.name not in ['']]


    

@admin.register(BonLivraison)
class BonLivraisonAdmin(ImportExportMixin, admin.ModelAdmin):
    form = NumBLForm
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in BonLivraison._meta.fields if field.name not in ['']]+['montant_cumule','qte_cumule']

    def save_model(self, request, obj, form, change):
        num_bl=form.cleaned_data['num_bl']
        obj.save(num_bl=num_bl)

    

    def qte_cumule(self, obj):
        return obj.qte_cumule


    def montant_cumule(self,obj):
        return obj.montant_cumule
@admin.register(Factures)
class FacturesAdmin(ImportExportMixin, admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Factures._meta.fields if field.name not in ['']]+['montant_cumule',]

    

    def montant_cumule(self,obj):
        return obj.montant_cumule

@admin.register(DetailFacture)
class DetailFactureAdmin(ImportExportMixin, admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in DetailFacture._meta.fields if field.name not in ['']]

    
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True

