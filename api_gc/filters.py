import django_filters
from django.db.models import Q

from api_gc.models import *
from api_gc.serializers import *


class ContratFilter(django_filters.FilterSet):
    duree_validite = django_filters.NumberFilter(label='Durée de validité',method='filter_duree_validite')
    est_client_cosider = django_filters.BooleanFilter(label='Est client cosider',field_name='client__est_client_cosider')
    def filter_duree_validite(self, queryset, name, value):
        if value:
            return queryset.filter(pk__in=[obj.pk for obj in queryset if obj.validite ==value])
        else:
            return queryset

    class Meta:
        model = Contrat
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass

class ClientsFilter(django_filters.FilterSet):
    class Meta:
        model = Clients
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass




class DQEFilter(django_filters.FilterSet):
    unite = django_filters.ModelChoiceFilter(field_name='prixProduit__unite', queryset=Unite.objects.all(),label='Unité')
    produit=django_filters.ModelChoiceFilter(field_name='prixProduit__produit', queryset=Produits.objects.all(),label='Produit')


    class Meta:
        model = DQE
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass




class PrixProduitFilter(django_filters.FilterSet):
    class Meta:
        model = PrixProduit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass





class BLFilter(django_filters.FilterSet):
    class Meta:
        model = BonLivraison
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass





class ItemBLFilter(django_filters.FilterSet):
    class Meta:
        model = DetailBonLivraison
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass



class CamionFilter(django_filters.FilterSet):
    class Meta:
        model = Camion
        fields = ['matricule',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass
