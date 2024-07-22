from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_gc.filters import *
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
            if(field_name not in ['']):
                obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                }

                if(field_name in ['id']):
                    obj['hide']=True

                if(field_name in ['montant_ht','montant_ttc','rg','tva','rabais']):
                    obj['cellRenderer'] = 'InfoRenderer'
                
                if(field_name in ['montant_ht','montant_ttc']):
                    obj['aggFunc']="sum"
                
                if(field_name in ['avenant']):
                    obj['cellRenderer'] = 'InfoRenderer'

                if(field_name in ['numero']):
                    obj['rowGroup'] = True
                    obj['hide']=True

                field_info.append(obj)
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)





class ContratFilterForm(APIView):
    def get(self,request):
        field_info = []

        for field_name, field_instance  in ContratFilter.base_filters.items():
            if(field_name  not in ['id']):

                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,

                }
                if str(field_instance.__class__.__name__) == 'ModelChoiceFilter':
                    anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                    serialized_data = anySerilizer(field_instance.queryset, many=True).data
                    filtered_data = []
                    for item in serialized_data:
                        filtered_item = {
                            'value': item['id'],
                            'label': item['libelle']
                        }
                        filtered_data.append(filtered_item)

                    obj['queryset'] = filtered_data

                field_info.append(obj)
            
            


        return Response({'fields': field_info},status=status.HTTP_200_OK)
class ContratFieldsAddUpdate(APIView):
    def get(self, request):
        serializer = ContratSerializer()
        fields = serializer.get_fields()
        field_info = []
        field_state = []
        state = {}
        contrat=None
        id=self.request.query_params.get('id',None)
        if(id):
            contrat=Contrat.objects.get(id=id)

        
        for field_name, field_instance in fields.items():
            if(field_name not in ['id','montant_ht','montant_ttc','validite']):
                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'required': field_instance.required,
                    'label': field_instance.label or field_name,
                }
                if(field_name in ['avenant']):
                    obj['disabled']=True
                else:
                    obj['disabled']=False
                if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                    anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                    serialized_data = anySerilizer(field_instance.queryset, many=True).data
                    if(field_name in ['client']):
                        filtered_data = []
                        for item in serialized_data:
                            filtered_item = {
                                'value': item['id'],
                                'label': item['libelle']
                            }
                            filtered_data.append(filtered_item)
                    if field_name in ['tva']:
                        filtered_data = []
                        for item in serialized_data:
                            filtered_item = {
                                'value': item['id'],
                                'label': str(item['id'])+'%'
                            }
                            filtered_data.append(filtered_item)

                    obj['queryset'] = filtered_data

                field_info.append(obj)

                default_value = None
                if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                    default_value=[]
                if str(field_instance.__class__.__name__) == 'BooleanField':
                    default_value = False
                if str(field_instance.__class__.__name__) in ['PositiveSmallIntegerField', 'DecimalField',
                                                              'PositiveIntegerField',
                                                              'IntegerField', ]:
                    default_value = 0
                field_state.append({
                    field_name: default_value,
                })
                for d in field_state:
                    state.update(d)
                
                if(contrat):
                    sd=ContratSerializer(contrat).data
                    for k,v in state.items():
                        state[k]=sd[k]

                    cli=Clients.objects.get(id=sd['client'])
                    state.__setitem__('client',[{'value':cli.id,'label':cli.libelle}])  

                    
                    tva=Tva.objects.get(id=sd['tva'])
                    state.__setitem__('tva',[{'value':tva.id,'label':f'{tva.id}%'}])

                    state.__setitem__('avenant',sd['avenant']+1)
                    

        return Response({'fields': field_info,'state':state},
                        status=status.HTTP_200_OK)






#--------------------------------------- client

class ClientFieldsList(APIView):
    def get(self, request):
        serializer = ClientSerilizer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            obj = {
                    'field': field_name,
                    'headerName': field_instance.label or field_name,


            }


            field_info.append(obj)
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)

class ClientFieldsAddUpdate(APIView):
    def get(self, request):
        serializer = ClientSerilizer()
        fields = serializer.get_fields()
        field_info = []
        field_state = []
        state = {}

        for field_name, field_instance in fields.items():
            if(field_name not in ['utilisateur']):
                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'required': field_instance.required,
                    'label': field_instance.label or field_name,
                }
                if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                    anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                    serialized_data = anySerilizer(field_instance.queryset, many=True).data
                    filtered_data = []
                    for item in serialized_data:
                        filtered_item = {
                            'value': item['id'],
                            'label': item['libelle'] or '----'
                        }
                        filtered_data.append(filtered_item)

                    obj['queryset'] = filtered_data

                field_info.append(obj)

                default_value = ''
                if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                    default_value=[]
                if str(field_instance.__class__.__name__) == 'BooleanField':
                    default_value = False
                if str(field_instance.__class__.__name__) in ['PositiveSmallIntegerField', 'DecimalField',
                                                              'PositiveIntegerField',
                                                              'IntegerField', ]:
                    default_value = 0
                field_state.append({
                    field_name: default_value,
                })
                for d in field_state:
                    state.update(d)

        return Response({'fields': field_info,'state':state},
                        status=status.HTTP_200_OK)



class ClientFilterForm(APIView):
    def get(self,request):


        field_info = []
        for field_name, field_instance  in ClientFilter().base_filters.items():

            if(field_name  not in ['']):

                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,

                }
                if str(field_instance.__class__.__name__) == 'ModelChoiceFilter':
                    anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                    serialized_data = anySerilizer(field_instance.queryset, many=True).data
                    filtered_data = []
                    for item in serialized_data:
                        filtered_item = {
                            'value': item['id'],
                            'label': item['libelle']
                        }
                        filtered_data.append(filtered_item)

                    obj['queryset'] = filtered_data

                field_info.append(obj)

        return Response({'fields': field_info},status=status.HTTP_200_OK)


#-------------------------------------------------------- DQE


class PrixProdFieldsList(APIView):
    def get(self, request):
        serializer = PrixProduitSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if(field_name not in ['',]):
                obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,


                }
                if(field_name in ['prix_unitaire']):
                    obj['cellRenderer'] = 'InfoRenderer'

                field_info.append(obj)
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)






class DQEFieldsList(APIView):
    def get(self, request):
        serializer = DQESerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if(field_name not in ['']):
                obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,


                }
                if(field_name in ['id','avenant','num_contrat','contrat','prixProduit']):
                    obj['hide']=True

                if(field_name in ['montant_qte','prix_unitaire']):
                    obj['cellRenderer'] = 'InfoRenderer'

                field_info.append(obj)
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)



class DQECumuleFieldsList(APIView):
    def get(self, request):
        serializer = DQECumuleSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if(field_name not in ['']):
                obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,


                }
                if(field_name in ['id','avenant','code_contrat','contrat_id','prixproduit_id']):
                    obj['hide']=True

                if(field_name in ['montant_qte','prix_transpor','prix_u']):
                    obj['cellRenderer'] = 'InfoRenderer'

                field_info.append(obj)
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)



class FactureFieldsList(APIView):
    def get(self, request):
        serializer = FactureSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if(field_name not in ['',]):
                obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,


                }
                if(field_name in ['montant_rg','montant_rb','montant','montant_cumule',
                                  'montant_ttc','montant_ht']):
                    obj['cellRenderer'] = 'InfoRenderer'

                field_info.append(obj)
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)


class DQEFilterForm(APIView):
    def get(self,request):
        field_info = []

        for field_name, field_instance  in DQEFilter.base_filters.items():
            if(field_name  not in ['id','contrat__numero','contrat__avenant']):

                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,

                }
                if str(field_instance.__class__.__name__) == 'ModelChoiceFilter':
                    anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                    serialized_data = anySerilizer(field_instance.queryset, many=True).data
                    filtered_data = []
                    for item in serialized_data:
                        filtered_item = {
                            'value': item['id'],
                            'label': item['libelle'],
                        }
                        filtered_data.append(filtered_item)

                    obj['queryset'] = filtered_data

                field_info.append(obj)

        return Response({'fields': field_info},status=status.HTTP_200_OK)




class DQECumuleFilterForm(APIView):
    def get(self,request):
        field_info = []

        for field_name, field_instance  in DQECumuleFilter.base_filters.items():
            if(field_name  not in ['code_contrat']):

                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,

                }
                if str(field_instance.__class__.__name__) == 'ModelChoiceFilter':
                    anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                    serialized_data = anySerilizer(field_instance.queryset, many=True).data
                    filtered_data = []
                    for item in serialized_data:
                        filtered_item = {
                            'value': item['id'],
                            'label': item['libelle'],
                        }
                        filtered_data.append(filtered_item)

                    obj['queryset'] = filtered_data

                field_info.append(obj)

        return Response({'fields': field_info},status=status.HTTP_200_OK)


class DQEFieldsAddUpdate(APIView):
    def get(self, request):
        fields = DQE._meta.get_fields()
        field_info = []
        field_state = []
        state = {}
        id = request.query_params.get('id', None) or None
        for field in fields:
            if(field.editable):
                if(field.name not in ['contrat']):

                    obj={
                        'name':field.name,
                        'type':field.get_internal_type(),
                        'label':field.verbose_name,    
                    }
                    related=field.related_model or None
                    filtered_data = []
                    if(related):
                        queryset=field.related_model.objects.all()
                        anySerilizer = create_dynamic_serializer(field.related_model)
                        serialized_data = anySerilizer(queryset, many=True).data
                        if(field.related_model in [PrixProduit]):
                            for item in serialized_data:
                                lib_prod=Produits.objects.get(id=item['produit']).libelle
                                code_prod=item['produit']
                                pu=item['prix_unitaire']
                                tp=item['type_prix']
                                
                                filtered_item = {
                                'value': item['id'],
                                'label': f'{code_prod} {pu}  ({tp})',
                                'lib_prod':f'{lib_prod}'
                                }
                                
                                filtered_data.append(filtered_item)
                        
                        obj['queryset']=filtered_data
                    field_info.append(obj)
                    if(id==None):
                        if(field.related_model):
                            state.__setitem__(field.name,[])
                        else:    
                            state.__setitem__(field.name,field.get_default())
                    else:
                        dqe=DQE.objects.get(id=id)
                        default_state = getattr(dqe, field.name)
                
                        if(field.related_model):
                            selected = [item for item in filtered_data if item['value'] == str(default_state)] 
                            state.__setitem__(field.name,selected)
                        else:
                            state.__setitem__(field.name,default_state)
        return Response({'fields': field_info,'state':state},
                        status=status.HTTP_200_OK)









class FactureFieldsAddUpdate(APIView):
    def get(self, request):

        serializer = FactureSerializer()
        fields = serializer.get_fields()
        field_info = []
        field_state = []
        state = {}

        for field_name, field_instance in fields.items():
            if(field_name not in ['date','contrat','montant','montant_rg','montant_rb','id','paye',
                                  'montant_facture_ht','montant_facture_ttc']):

                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'required': field_instance.required,
                    'label': field_instance.label or field_name,
                }

                field_info.append(obj)
                default_value = ''
                if str(field_instance.__class__.__name__) == 'BooleanField':
                    default_value = False
                if str(field_instance.__class__.__name__) in ['PositiveSmallIntegerField', 'DecimalField',
                                                              'PositiveIntegerField',
                                                              'IntegerField', ]:
                    default_value = 0

                field_state.append({
                    field_name: default_value,
                })

                for d in field_state:
                    state.update(d)

        return Response({'fields': field_info,'state':state},
                        status=status.HTTP_200_OK)


#----------------------------------------------------- Planing
class PlaningieldsAddUpdate(APIView):
    def get(self, request):
        fields = Planing._meta.get_fields()
        field_info = []
        field_state = []
        state = {}
        c=self.request.query_params.get('contrat', None)
        if(c):
            try:
                contrat=Contrat_Latest.objects.get(id=c)
            except:
                contrat=None
        else:
            contrat=None
        for field in fields:
            if(field.editable):
                if(field.name not in ['contrat','id']):
                    obj={
                        'name':field.name,
                        'type':field.get_internal_type(),
                        'label':field.verbose_name,    
                    }
                    related=field.related_model or None
                    filtered_data = []
                    if(related):
                        if(field.related_model in [DQECumule]):
                            queryset=field.related_model.objects.filter(contrat_id=contrat)
                            anySerilizer = create_dynamic_serializer(field.related_model)
                            serialized_data = anySerilizer(queryset, many=True).data
                            
                            for item in serialized_data:
                                code_prod=item['produit_id']
                                lib_prod= Produits.objects.get(id=code_prod).libelle
                                filtered_item = {
                                'value': item['id'],
                                'label': f'{code_prod}  {lib_prod}',
                                }
                                
                                filtered_data.append(filtered_item)
                            obj['queryset']=filtered_data
                    field_info.append(obj)
        return Response({'fields': field_info,'state':state},
                        status=status.HTTP_200_OK)





class PlaningFieldsList(APIView):
    def get(self, request):
        serializer = PlaningSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if(field_name not in ['']):
                obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,


                }
                if(field_name in ['id','contrat','dqe','date']):
                    obj['hide']=True
                
                if(field_name in ['mmaa']):
                    obj['rowGroup'] = True
                    obj['hide']=True


                if(field_name in ['qte_livre','qte_realise','ecart']):
                    obj['cellRenderer'] = 'InfoRenderer'
                    obj['aggFunc']="sum"

                field_info.append(obj)
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)




#----------------------------------------------------- Bon de livraison

class BLFilterForm(APIView):
    def get(self,request):
        field_info = []
        contrat = request.query_params.get('contrat', None)
        for field_name, field_instance  in BLFilter.base_filters.items():
            if(field_name  not in ['deleted','deleted_by_cascade','contrat','ptc','montant','qte']):

                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,

                }
                if str(field_instance.__class__.__name__) == 'ModelChoiceFilter':
                    if(field_name in ['dqe',]):
                        anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                        serialized_data = DQESerializer(field_instance.queryset.filter(contrat=contrat), many=True).data
                        filtered_data = []
                        for item in serialized_data:
                            filtered_item = {
                                  'value': item['id'],
                                    'label': item['produit'],
                            }
                            filtered_data.append(filtered_item)

                        obj['queryset'] = filtered_data
                    if (field_name in ['camion', ]):
                        anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                        serialized_data = anySerilizer(field_instance.queryset, many=True).data
                        filtered_data = []
                        for item in serialized_data:
                            filtered_item = {
                                'value': item['matricule'],
                                'label': item['matricule'],
                            }
                            filtered_data.append(filtered_item)

                        obj['queryset'] = filtered_data


                field_info.append(obj)

        return Response({'fields': field_info},status=status.HTTP_200_OK)



class BLFieldsList(APIView):
    def get(self, request):
        serializer = BonLivraisonSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if(field_name not in ['']):
                obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,


                }

                if(field_name in ['contrat','id','dqe']):
                    obj['hide'] =True

                if(field_name in ['date','montant','montant_cumule']):
                    obj['cellRenderer'] = 'InfoRenderer'

                field_info.append(obj)

        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)



class BLFieldsAddUpdate(APIView):
    def get(self, request):
        fields = BonLivraison._meta.get_fields()
        field_info = []
        field_state = []
        state = {}
        c=self.request.query_params.get('contrat', None)
        if(c):
            try:
                contrat=Contrat_Latest.objects.get(numero=c)
            except:
                contrat=None
        else:
            contrat=None
        for field in fields:
          
            if(field.editable):
                
                if(field.name not in ['contrat']):
                    obj={
                        'name':field.name,
                        'type':field.get_internal_type(),
                        'label':field.verbose_name,    
                    }
    
                    related=field.related_model or None
                    filtered_data = []
                    if(related):
                        if(field.related_model in [DQECumule]):
                            queryset=field.related_model.objects.filter(contrat_id=contrat)
                            anySerilizer = create_dynamic_serializer(field.related_model)
                            serialized_data = anySerilizer(queryset, many=True).data
                            print
                            for item in serialized_data:
                                code_prod=item['produit_id']
                                lib_prod= Produits.objects.get(id=code_prod).libelle
                                filtered_item = {
                                'value': item['id'],
                                'label': f'{code_prod}  {lib_prod}',
                                }
                                
                                filtered_data.append(filtered_item)
                            obj['queryset']=filtered_data
                        if(field.related_model in [Camion]):
                            queryset=field.related_model.objects.all()
                            anySerilizer = create_dynamic_serializer(field.related_model)
                            serialized_data = anySerilizer(queryset, many=True).data
                            
                            for item in serialized_data:
                                
                                filtered_item = {
                                'value': item['matricule'],
                                'label': f"{item['matricule']} ({item['tare']}{item['unite']})"
                                }
                                
                                filtered_data.append(filtered_item)
                            obj['queryset']=filtered_data
                    field_info.append(obj)
                    
                    if(field.related_model):
                        state.__setitem__(field.name,[])
                    else:
                        state.__setitem__(field.name,field.get_default())
                    

    
                    
        return Response({'fields': field_info,'state':state},
                        status=status.HTTP_200_OK)














#------------------------------------------------ Camion


class CamionFieldsList(APIView):
    def get(self, request):
        serializer = CamionSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if(field_name not in ['',]):
                obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,


                }



                field_info.append(obj)
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)


class CamionAddUpdate(APIView):
    def get(self, request):
        serializer = CamionSerializer()
        fields = serializer.get_fields()
        field_info = []
        field_state = []
        state = {}

        for field_name, field_instance in fields.items():
            obj = {
                'name': field_name,
                'type': str(field_instance.__class__.__name__),
                'required': field_instance.required,
                'label': field_instance.label or field_name,
            }
            if str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField":
                anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                serialized_data = anySerilizer(field_instance.queryset, many=True).data
                filtered_data = []
                for item in serialized_data:
                    filtered_item = {
                        'value': item['id'],
                        'label': item['libelle']
                    }
                    filtered_data.append(filtered_item)
                obj['queryset'] = filtered_data

            if (field_name in ['tare']):
                params = Configurations.objects.all().first()
                obj['readOnly'] = params.saisie_automatique

            field_info.append(obj)

            default_value = ''
            if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                default_value = []
            if str(field_instance.__class__.__name__) == 'BooleanField':
                default_value = False
            if str(field_instance.__class__.__name__) in ['PositiveSmallIntegerField', 'DecimalField',
                                                                  'PositiveIntegerField',
                                                                  'IntegerField', ]:
                if (field_name in ['tare']):
                    params = Configurations.objects.all().first()
                    if (params.saisie_automatique):
                        default_value = 150
                    else:
                        default_value = 0
                else:
                    default_value = 0
            field_state.append({
                    field_name: default_value,
            })
            for d in field_state:
                state.update(d)

        return Response({'fields': field_info, 'state': state},
                    status=status.HTTP_200_OK)



class CamionFilterForm(APIView):
    def get(self,request):
        field_info = []
        for field_name, field_instance  in CamionFilter.base_filters.items():
            if(field_name  not in ['',]):
                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,

                }
                field_info.append(obj)
        return Response({'fields': field_info},status=status.HTTP_200_OK)









class DetailFieldsList(APIView):
    def get(self, request):
        serializer = DetailFactureSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if(field_name not in ['detail','id']):
                obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,


                }

                if(field_name in ['facture']):
                    obj['hide'] = True


                if(field_name in ['date','montant','prix_u']):
                    obj['cellRenderer'] = 'InfoRenderer'

                field_info.append(obj)

        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)





class AvanceFieldsList(APIView):
    def get(self, request):
        serializer = AvanceSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if(field_name not in ['',]):
                obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,


                }

                if (field_name in ['id','contrat']):
                    obj['hide'] = True

                if(field_name in ['montant_avance','montant_restant']):
                    obj['cellRenderer'] = 'InfoRenderer'

                field_info.append(obj)

        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)




class AvanceFieldsAdd(APIView):
    def get(self, request):
        serializer = AvanceSerializer()
        fields = serializer.get_fields()
        field_info = []
        field_state = []
        state = {}
        for field_name, field_instance in fields.items():
            if(field_name not in ['montant_restant','id','contrat','num_avance']):
                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'required': field_instance.required,
                    'label': field_instance.label or field_name,
                }


                field_info.append(obj)

                default_value = ''
                if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                        default_value = []
                if str(field_instance.__class__.__name__) == 'BooleanField':
                    default_value = False
                if str(field_instance.__class__.__name__) in ['PositiveSmallIntegerField', 'DecimalField',
                                                                  'PositiveIntegerField',
                                                                  'IntegerField', ]:
                    default_value = 0
                field_state.append({
                        field_name: default_value,
                })
                for d in field_state:
                    state.update(d)


        return Response({'fields': field_info,'state':state},
                        status=status.HTTP_200_OK)


