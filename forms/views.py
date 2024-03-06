from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_gc.serializers import *


# Create your views here.


#--------------------------------------- user
class SignupFields(APIView):
    def get(self, request):

        serializer = UserSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            obj = {
                    'name': field_name,
                        'type': str(field_instance.__class__.__name__),
                        'required': field_instance.required,
                        'label': field_instance.label or field_name,
                }

            field_info.append(obj)
            if (field_name == "password"):
                field_info.append({
                    'name': 'confirme' + field_name,
                    'type': str(field_instance.__class__.__name__),
                    'required':True,
                    'label': 'Confirmer le mot de passe',
                })
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)

class SignupFieldsDS(APIView):
    def get(self, request):
        serializer = UserSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            default_value = ''
            field_info.append({
                field_name:default_value ,

            })
            state = {}

            for d in field_info:
                state.update(d)
        return Response({'state': state}, status=status.HTTP_200_OK)



#--------------------------------------- contrat

class ContratFieldsList(APIView):
    def get(self, request):
        serializer = ContratSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            obj = {
                    'field': field_name,
                    'headerName': field_instance.label or field_name,
                    'info': str(field_instance.__class__.__name__),

            }
            if(field_name in ['montant_ht','montant_ttc']):
                obj['cellRenderer'] = 'InfoRenderer' 


            field_info.append(obj)
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)

class ContratFieldsAdd(APIView):
    def get(self, request):
        serializer = ContratSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if(field_name not in ['utilisateur','montant_ht','montant_ttc','validite']):
                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,
                }

                field_info.append(obj)
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)
