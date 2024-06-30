from django.contrib import admin


from api_gc.models import *



# Register your models here.
lp=20


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Images._meta.fields  if field.name not in ['deleted', 'deleted_by_cascade']]

    


@admin.register(Avances)
class AvancesAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Avances._meta.fields  if field.name not in ['deleted', 'deleted_by_cascade']]
    


@admin.register(Unite)
class UniteAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Unite._meta.fields  if field.name not in ['deleted', 'deleted_by_cascade']]

    




@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Contrat._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]+['montant_ht','montant_ttc',]

    

    def montant_ttc(self,obj):
        return obj.montant_ttc
    def montant_ht(self,obj):
        return obj.montant_ht

@admin.register(Configurations)
class ParametresAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Configurations._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]

    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ModePaiement)
class ModePaiementAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in ModePaiement._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]

    



@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Clients._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]

    


@admin.register(Encaissement)
class EncaissementAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in Encaissement._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]+['montant_creance',
                                                                                                                        ]


    
    def montant_creance(self,obj):
        return obj.montant_creance








@admin.register(DQE)
class ContratAdmin(admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in DQE._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]+['prix_unitaire','montant_qte',
                                                                                                                      ]


    
    def montant_qte(self,obj):
        return obj.montant_qte
    def prix_unitaire(self,obj):
        return obj.prixProduit.prix_unitaire

@admin.register(UniteMesure)
class UniteMesureAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = [field.name for field in UniteMesure._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]


    


@admin.register(Produits)
class UniteMesureAdmin(admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Produits._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]


    

@admin.register(PrixProduit)
class UniteMesureAdmin(admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in PrixProduit._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]


    


@admin.register(Planing)
class UniteMesureAdmin(admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Planing._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]+['cumule',]
    

    def cumule(self, obj):
        return obj.cumule




@admin.register(Camion)
class CamionAdmin(admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Camion._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]


    

@admin.register(BonLivraison)
class BonLivraisonAdmin(admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in BonLivraison._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]+['montant_cumule','qte_cumule']


    

    def qte_cumule(self, obj):
        return obj.qte_cumule


    def montant_cumule(self,obj):
        return obj.montant_cumule
@admin.register(Factures)
class FacturesAdmin(admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in Factures._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]+['montant_cumule',]

    

    def montant_cumule(self,obj):
        return obj.montant_cumule

@admin.register(DetailFacture)
class DetailFactureAdmin(admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    list_display = [field.name for field in DetailFacture._meta.fields if field.name not in ['deleted', 'deleted_by_cascade']]

    
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True

