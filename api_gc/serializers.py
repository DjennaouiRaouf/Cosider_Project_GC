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
    montant_ht = serializers.SerializerMethodField()
    montant_ttc = serializers.SerializerMethodField()
    validite = serializers.SerializerMethodField()

    def get_validite(self, obj):
        return obj.validite


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
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)
        return fields
    class Meta:
        model = Clients
        fields = '__all__'

class PrixProduitSerializer(serializers.ModelSerializer):
    libelle_prod=serializers.SerializerMethodField(label='libelle du produit')
    def get_libelle_prod(self, obj):
        return obj.produit.libelle
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields
    class Meta:
        model = PrixProduit
        fields = '__all__'




class CamionSerializer(serializers.ModelSerializer):

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['unite'] = instance.unite.libelle
        return representation
    class Meta:
        model = Camion
        fields = '__all__'





class DQESerializer(serializers.ModelSerializer):
    montant_qte=serializers.SerializerMethodField()
    prix_unitaire=serializers.SerializerMethodField()
    unite=serializers.SerializerMethodField()
    produit = serializers.SerializerMethodField()
    def get_montant_qte(self, obj):
        return obj.montant_qte

    def get_unite(self, obj):
        return obj.prixProduit.unite.libelle

    def get_produit(self, obj):
        return obj.prixProduit.produit.libelle

    def get_prix_unitaire(self, obj):
        return obj.prixProduit.prix_unitaire


    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields
    class Meta:
        model = DQE
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




class BonLivraisonSerializer(serializers.ModelSerializer):
    montant_cumule = serializers.SerializerMethodField(label="Montant Cumule")
    libelle = serializers.SerializerMethodField(label='Libelle')
    prix_unitaire = serializers.SerializerMethodField(label='Prix Unitaire')
    qte_cumule = serializers.SerializerMethodField(label="Quantité Cumulée")

    def get_montant_cumule(self, obj):
        return obj.montant_cumule

    def get_libelle(self, obj):
        return obj.dqe.prixProduit.produit.libelle

    def get_prix_unitaire(self, obj):
        return obj.dqe.prixProduit.prix_unitaire

    def get_qte_cumule(self, obj):
        return obj.qte_cumule
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields
    class Meta:
        model = BonLivraison
        fields = '__all__'





class FactureSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields
    class Meta:
        model = Factures
        fields = '__all__'





class ODSSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)
        return fields
    class Meta:
        model = ODS
        fields = '__all__'


class DetailFactureSerializer(serializers.ModelSerializer):
    qte=serializers.SerializerMethodField()
    date=serializers.SerializerMethodField()
    montant=serializers.SerializerMethodField()
    prix_u = serializers.SerializerMethodField()
    produit = serializers.SerializerMethodField()

    def get_qte(self, obj):
        return obj.detail.qte

    def get_date(self, obj):
        return  obj.detail.date

    def get_montant(self, obj):
        return  obj.detail.montant

    def get_prix_u(self,obj):
        return obj.detail.dqe.prixProduit.prix_unitaire

    def get_produit(self, obj):
        return obj.detail.dqe.prixProduit.produit.libelle

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)
        return fields
    class Meta:
        model = DetailFacture
        fields = '__all__'


