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
    historique = serializers.SerializerMethodField()

    def get_utilisateur(self,obj):
        user_fullname = obj.historique.latest().history_user.get_full_name()
        return user_fullname

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields

    def get_historique(self, obj):
        history = []
        for historical_instance in obj.historique.all():

            anySerilizer = create_dynamic_serializer(historical_instance.instance)
            serilizedData=anySerilizer(historical_instance.instance, many=False).data
            serilizedData['utilisateur']=historical_instance.history_user.username
            serilizedData['date_modification']=historical_instance.history_date
            if (historical_instance.history_type == '~'):
                serilizedData['type']= 'Modification'
            elif (historical_instance.history_type=='+'):
                serilizedData['type']='Création'


            serilizedData['version_id'] = historical_instance.history_id
            history.append(serilizedData)
        return history
    class Meta:
        model = Contrat
        fields ='__all__'



class DQESerializer(serializers.ModelSerializer):
    utilisateur = serializers.SerializerMethodField()
    historique = serializers.SerializerMethodField()

    def get_utilisateur(self, obj):
        user_fullname = obj.historique.latest().history_user.get_full_name()
        return user_fullname

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields

    def get_historique(self, obj):
        history = []
        for historical_instance in obj.historique.all():
            anySerilizer = create_dynamic_serializer(historical_instance.instance)
            serilizedData = anySerilizer(historical_instance.instance, many=False).data
            serilizedData['utilisateur'] = historical_instance.history_user.username
            serilizedData['date_modification'] = historical_instance.history_date
            if (historical_instance.history_type == '~'):
                serilizedData['type'] = 'Modification'
            elif (historical_instance.history_type == '+'):
                serilizedData['type'] = 'Création'

            serilizedData['version_id'] = historical_instance.history_id
            history.append(serilizedData)
        return history

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