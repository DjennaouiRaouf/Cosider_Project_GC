
from rest_framework import serializers

from api_gc.models import *


class ContratSerializer(serializers.ModelSerializer):
    utilisateur=serializers.SerializerMethodField()

    def get_utilisateur(self,obj):
        latest_username = obj.historique.latest().history_user
        return latest_username.id
    class Meta:
        model = Contrat
        fields ='__all__'