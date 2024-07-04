import django_filters
from django.db.models import Q

from api_gc.models import *
from api_gc.serializers import *


class ContratFilter(django_filters.FilterSet):
    class Meta:
        model = Contrat
        fields = ['numero','avenant','client__id']

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
        fields = ['contrat__numero','contrat__avenant']

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
        model = DQE
        fields = ['contrat__numero']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.base_filters.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_instance.label = model_field.verbose_name
            except:
                pass
