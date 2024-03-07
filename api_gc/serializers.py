from django.contrib.auth.models import User
from rest_framework import serializers

from api_gc.models import *

def create_dynamic_serializer(model_class):
    class DynamicModelSerializer(serializers.ModelSerializer):
        def get_fields(self, *args, **kwargs):
            fields = super().get_fields(*args, **kwargs)
            fields.pop('deleted', None)
            fields.pop('deleted_by_cascade', None)

            return fields
        class Meta:
            model = model_class
            fields = '__all__'

    return DynamicModelSerializer


class ContratSerializer(serializers.ModelSerializer):
    utilisateur=serializers.SerializerMethodField()
    montant_ht = serializers.SerializerMethodField()
    montant_ttc = serializers.SerializerMethodField()

    def get_utilisateur(self,obj):
        user_fullname = obj.historique.latest().history_user.username
        return user_fullname

    def get_montant_ht(self,obj):
        return  obj.montant_ht

    def get_montant_ttc(self, obj):
        return obj.montant_ttc

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields


    class Meta:
        model = Contrat
        fields ='__all__'



class DQESerializer(serializers.ModelSerializer):
    utilisateur = serializers.SerializerMethodField()

    def get_utilisateur(self, obj):
        user_fullname = obj.historique.latest().history_user.get_full_name()
        return user_fullname

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields



    class Meta:
        model = DQE
        fields = '__all__'


class ImagesSerilizer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields
    class Meta:
        model = Images
        fields = '__all__'


class ClientSerilizer(serializers.ModelSerializer):
    utilisateur = serializers.SerializerMethodField()
    def get_utilisateur(self, obj):
        user_fullname = obj.historique.latest().history_user.username
        return user_fullname
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields
    class Meta:
        model = Clients
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('id', None)
        return fields
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=False

        )
        return user