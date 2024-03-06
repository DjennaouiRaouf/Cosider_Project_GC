import django_filters
from django.db.models import Q

from api_gc.models import *


class ContratFilter(django_filters.FilterSet):
    class Meta:
        model = Contrat
        fields = ['id','tva','rabais','transport','rg',]


class ClientsFilter(django_filters.FilterSet):
    class Meta:
        model = Clients
        fields = ['id', 'type_client', 'est_client_cosider', 'sous_client', ]

