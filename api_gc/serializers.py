from django.contrib.auth.models import User
from rest_framework import serializers

from api_gc.models import *


class ContratSerializer(serializers.ModelSerializer):
    utilisateur=serializers.SerializerMethodField()

    def get_utilisateur(self,obj):
        user_fullname = obj.historique.latest().history_user.get_full_name()
        return user_fullname
    class Meta:
        model = Contrat
        fields ='__all__'