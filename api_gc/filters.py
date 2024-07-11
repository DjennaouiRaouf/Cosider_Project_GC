import django_filters
from django.db.models import Q

from api_gc.models import *
from api_gc.serializers import *


class ContratFilter(django_filters.FilterSet):
    clientID = django_filters.CharFilter(label="Code Client",field_name='client__id',lookup_expr='exact')
    clientLib = django_filters.CharFilter(field_name='client__libelle',label='Libelle Client',lookup_expr='icontains')
    
    class Meta:
        model = Contrat
        fields = ['numero','avenant']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass



class ClientFilter(django_filters.FilterSet):
    clientID = django_filters.CharFilter(label="Code Client",field_name='id',lookup_expr='exact')
    clientLib = django_filters.CharFilter(field_name='libelle',label='Libelle',lookup_expr='icontains')
    ville= django_filters.CharFilter(field_name='ville',label='Ville',lookup_expr='icontains')
  
    class Meta:
        model = Clients
        fields=['clientID','clientLib','ville','type','act']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass





class DQEFilter(django_filters.FilterSet):
    code_produit=django_filters.ModelChoiceFilter(field_name='prixProduit__produit',label='Code Produit',queryset=Produits.objects.all())
    type_prix=django_filters.ModelChoiceFilter(field_name='prixProduit__type_prix',label='Type de Prix',queryset=TypePrix.objects.all())
    class Meta:
        model = DQE
        fields = ['contrat__numero','contrat__avenant','code_produit','type_prix']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass


class DQECumuleFilter(django_filters.FilterSet):
    class Meta:
        model = DQECumule
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass
