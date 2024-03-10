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
