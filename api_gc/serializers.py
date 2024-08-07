from django.contrib.auth.models import User
from rest_framework import serializers

from api_gc.models import *

def create_dynamic_serializer(model_class):
    class DynamicModelSerializer(serializers.ModelSerializer):
        def get_fields(self, *args, **kwargs):
            fields = super().get_fields(*args, **kwargs)
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
        fields.pop('est_bloquer', None)
        fields.pop('user_id', None)
        fields.pop('date_modification', None)


        return fields


    class Meta:
        model = Contrat
        fields =['id','numero','avenant','libelle','tva','transport','rabais','rg','client','date_signature',
                 'date_expiration','validite','montant_ht','montant_ttc','validite']



class ImagesSerilizer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('est_bloquer', None)
        fields.pop('user_id', None)
        fields.pop('date_modification', None)


        return fields
    class Meta:
        model = Images
        fields = '__all__'

class ClientSerilizer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('est_bloquer', None)
        fields.pop('user_id', None)
        fields.pop('date_modification', None)

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
        fields.pop('est_bloquer', None)
        fields.pop('user_id', None)
        fields.pop('date_modification', None)

        return fields
    class Meta:
        model = PrixProduit
        fields = '__all__'




class CamionSerializer(serializers.ModelSerializer):

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('est_bloquer', None)
        fields.pop('user_id', None)
        fields.pop('date_modification', None)

        return fields
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['unite'] = instance.unite.libelle
        return representation
    class Meta:
        model = Camion
        fields = '__all__'





class DQESerializer(serializers.ModelSerializer):
    montant_qte=serializers.SerializerMethodField(label='Montant QTE')
    prix_unitaire=serializers.SerializerMethodField(label='Prix Unit')
    unite=serializers.SerializerMethodField(label='Unité')
    produit = serializers.SerializerMethodField(label='Produit')
    num_contrat=serializers.SerializerMethodField()
    avenant=serializers.SerializerMethodField()


    def get_montant_qte(self, obj):
        return obj.montant_qte

    def get_unite(self, obj):
        return Unite.objects.get(id=obj.prixProduit.unite).libelle or ''

    def get_produit(self, obj):
        return obj.prixProduit.produit.libelle

    def get_prix_unitaire(self, obj):
        return obj.prixProduit.prix_unitaire

    def get_num_contrat(self, obj):
        return obj.contrat.numero

    def get_avenant(self,obj):
        return obj.contrat.avenant



    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('est_bloquer', None)
        fields.pop('user_id', None)
        fields.pop('date_modification', None)


        return fields
    class Meta:
        model = DQE
        fields = [ 'id','contrat','produit','qte' ,'rabais' ,'prix_transport',
                  'prix_unitaire','montant_qte','unite','num_contrat','avenant','prixProduit']




class DQECumuleSerializer(serializers.ModelSerializer):
    libelle=serializers.SerializerMethodField(label='Libellé')
    prix_u=serializers.SerializerMethodField(label='Prix Unit')

    montant_qte=serializers.SerializerMethodField(label='Montant QTE')

    def get_libelle(self,obj):
        return obj.prixproduit_id.produit.libelle

    
    def get_prix_u(self,obj):
        return obj.prixproduit_id.prix_unitaire

    def get_montant_qte(self,obj):
        return obj.montant_qte
    
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)

        return fields
    class Meta:
        model = DQECumule
        fields = ['id','produit_id','libelle','prix_u','code_contrat','qte','avenant','contrat_id','prixproduit_id'
                  ,'rabais','prix_transport','montant_qte']










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


class EncaissementSerializer(serializers.ModelSerializer):
    montant_cumule=serializers.SerializerMethodField(label='Montant Cumulé')
    montant_creance=serializers.SerializerMethodField(label='Montant Créance')

    def get_montant_cumule(self,obj):
        return obj.montant_cumule
    def get_montant_creance(self,obj):
        return obj.montant_creance
    
    
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        return fields
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['mode_paiement'] = instance.mode_paiement.libelle
        representation['date_encaissement']= instance.date_encaissement.strftime('%Y-%m-%d %H:%M')
        return representation


    class Meta:
        model = Encaissement
        fields = ['id','facture','date_encaissement','mode_paiement','montant_encaisse','montant_cumule','montant_creance']

    
class InvNestedSerializer(serializers.ModelSerializer):
    enc=serializers.SerializerMethodField()
    def get_enc(self,obj):
        e=Encaissement.objects.filter(facture=obj)
        return EncaissementSerializer(e,many=True).data

    class Meta:
        model = Factures
        fields = '__all__'

class PlaningSerializer(serializers.ModelSerializer):
    
    lib_prod=serializers.SerializerMethodField(label='Libelle')
    code_prod=serializers.SerializerMethodField(label='Code Produit')
    unite_m=serializers.SerializerMethodField(label='Unité M')
    mmaa=serializers.SerializerMethodField(label='MMAA')
    qte_r=serializers.SerializerMethodField(label='Qte Livrée')

    def get_lib_prod(self,obj):
        try:
            return obj.dqe.produit_id.libelle
        except:
            return None
    def get_code_prod(self,obj):
        try:
            return obj.dqe.produit_id.id
        except:
            return None
        
    def get_unite_m(self,obj):
        try:
            return obj.dqe.produit_id.unite_m.id
        except:
            return None
        
        
    def get_mmaa(self,obj):
        return f'{obj.date.year}-{obj.date.month}'
    
    def get_qte_r(self,obj):
        return obj.qte_realise


    
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        return fields
    class Meta:
        model = Planing
        fields = ['contrat','mmaa','dqe','code_prod','lib_prod','date','qte_livre','qte_r','unite_m']
    


class BonLivraisonSerializer(serializers.ModelSerializer):
    montant_cumule = serializers.SerializerMethodField(label="Montant Cumule")
    libelle = serializers.SerializerMethodField(label='Libelle')
    prix_unitaire = serializers.SerializerMethodField(label='Prix Unitaire')
    qte_cumule = serializers.SerializerMethodField(label="Quantité Cumulée")
    tare= serializers.SerializerMethodField(label="Tare")
    
    def get_montant_cumule(self, obj):
        return obj.montant_cumule

    def get_libelle(self, obj):
        try:
            return obj.dqe.prixproduit_id.produit.libelle
        except Exception as e:
            return None

    def get_prix_unitaire(self, obj):
        try:
            return obj.dqe.prixproduit_id.prix_unitaire
        except Exception as e:
            return None
    def get_qte_cumule(self, obj):
        return obj.qte_cumule
    
    def get_tare(self,obj):
        return obj.camion.tare
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime('%Y-%m-%d %H:%M:%S')
        return representation


    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('est_bloquer', None)
        fields.pop('user_id', None)
        fields.pop('date_modification', None)


        return fields
    class Meta:
        model = BonLivraison
        fields = [ 'id','num_bl','libelle','conducteur','camion','numero_permis_c','contrat','dqe'
                  ,'prix_unitaire','ptc','tare','qte','qte_cumule','montant','montant_cumule','date']




class FactureSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('est_bloquer', None)
        fields.pop('user_id', None)
        fields.pop('date_modification', None)


        return fields
    class Meta:
        model = Factures
        fields = '__all__'







class AvanceSerializer (serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('est_bloquer', None)
        fields.pop('user_id', None)
        fields.pop('date_modification', None)

        return fields
    class Meta:
        model = Avances
        fields = '__all__'




class DetailFactureSerializer(serializers.ModelSerializer):
    produit = serializers.SerializerMethodField(label='Produit')
    qte=serializers.SerializerMethodField(label='Quantite')
    prix_u = serializers.SerializerMethodField(label='Prix Unitaire')
    montant=serializers.SerializerMethodField(label='Montant')
    date = serializers.SerializerMethodField(label='Date de livraison')

    def get_qte(self, obj):
        return str(obj.detail.qte)+' '+obj.detail.dqe.prixProduit.produit.unite.libelle

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
        fields.pop('est_bloquer', None)
        fields.pop('user_id', None)
        fields.pop('date_modification', None)

        return fields
    class Meta:
        model = DetailFacture
        fields = '__all__'


