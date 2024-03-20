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
    validite = serializers.SerializerMethodField()

    def get_validite(self, obj):
        return obj.validite
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
    montant = serializers.SerializerMethodField(label="Montant")
    montant_cumule = serializers.SerializerMethodField(label="Montant Cumule")
    libelle = serializers.SerializerMethodField(label='Libelle')
    prix_unitaire = serializers.SerializerMethodField(label='Prix Unitaire')
    qte=serializers.SerializerMethodField(label="Quantité")
    qte_cumule = serializers.SerializerMethodField(label="Quantité Cumulée")

    def get_montant(self, obj):
        return obj.montant

    def get_montant_cumule(self, obj):
        return obj.montant_cumule

    def get_libelle(self, obj):
        return obj.dqe.prixProduit.produit.libelle

    def get_prix_unitaire(self, obj):
        return obj.dqe.prixProduit.prix_unitaire

    def get_qte(self,obj):
        return obj.qte

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
    montant = serializers.SerializerMethodField(label="Montant")
    montant_cumule = serializers.SerializerMethodField(label="Montant Cumule")
    montant_ttc= serializers.SerializerMethodField(label="Montant TTC")
    montant_ht = serializers.SerializerMethodField(label="Montant HT")
    montant_rb = serializers.SerializerMethodField(label="Montant Rabais")
    montant_rg = serializers.SerializerMethodField(label="Montant Retenue de Garantie")


    def get_montant(self, obj):
        return obj.montant

    def get_montant_cumule(self, obj):
        return obj.montant_cumule

    def get_montant_ttc(self, obj):
        return  obj.montant_facture_ttc

    def get_montant_ht(self, obj):
        return obj.montant_facture_ht

    def get_montant_rb(self, obj):
        return obj.montant_rb
    def get_montant_rg(self, obj):
        return obj.montant_rg
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields
    class Meta:
        model = Factures
        fields = '__all__'
