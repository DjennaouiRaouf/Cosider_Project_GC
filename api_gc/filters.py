import django_filters
from django.db.models import Q

from api_gc.models import *
from api_gc.serializers import *


class ContratFilter(django_filters.FilterSet):
    duree_validite = django_filters.NumberFilter(label='Durée de validité',method='filter_duree_validite')

    def filter_duree_validite(self, queryset, name, value):
        if value:
            return queryset.filter(pk__in=[obj.pk for obj in queryset if obj.validite ==value])
        else:
            return queryset

    class Meta:
        model = Contrat
        fields = '__all__'
class ClientsFilter(django_filters.FilterSet):
    class Meta:
        model = Clients
        fields = ['id', 'type_client', 'est_client_cosider', 'sous_client', ]

