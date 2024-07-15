from django.contrib.auth import authenticate
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from api_gc.filters import *
from api_gc.models import *
from api_gc.serializers import *

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Login(APIView):
    permission_classes = []
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        app_name = 'api_sm'

        if user is not None:
            Token.objects.filter(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)
            app_permissions = self.get_app_permissions(user, app_name)
            response = Response(status=status.HTTP_200_OK)
            role = '|'.join(list(app_permissions))
            response.set_cookie('token', token.key)
            response.set_cookie('role', role)
            return response
        else:
            return Response({'message': 'Informations d’identification non valides'}, status=status.HTTP_400_BAD_REQUEST)

    def get_app_permissions(self, user, app_name):
        # Get all permissions for the specified app
        all_permissions = user.get_all_permissions()
        app_permissions = set()

        for permission in all_permissions:
            if permission.split('.')[0] == app_name:
                app_permissions.add(permission)

        return app_permissions



class Whoami(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'whoami':request.user.username}, status=status.HTTP_200_OK)

class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        Token.objects.get(user_id=request.user.id).delete()
        response=Response({'message': 'Vous etes déconnecté'}, status=status.HTTP_200_OK)
        response.delete_cookie('token')
        response.delete_cookie('role')
        return response

class ListImages(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Images.objects.all()
    serializer_class =ImagesSerilizer

class WhoamiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'whoami':request.user.username}, status=status.HTTP_200_OK)





class ListContract(generics.ListAPIView): # grouper par num contrat
    #permission_classes = [IsAuthenticated]
    queryset = Contrat.objects.all()
    serializer_class =ContratSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContratFilter



class ListPlaning(generics.ListAPIView):
    #permission_classes=[IsAuthenticated]
    queryset = Planing.objects.all()
    serializer_class = PlaningSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlaningFilter

class ListBL(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = BonLivraison.objects.all()
    serializer_class = BonLivraisonSerializer
    filter_backends = [DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        qt = 0
        mt = 0
        response_data = super().list(request, *args, **kwargs).data
        for q in queryset:
            qt = qt + q.qte
            mt = mt + q.montant

        return Response({'bl': response_data,
                         'extra': {
                             'qt': qt,
                             'mt': mt,


                         }}, status=status.HTTP_200_OK)



class AddBL(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset= BonLivraison.objects.all()
    serializer_class = BonLivraisonSerializer


class AddPlaning(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset= Planing.objects.all()
    serializer_class = PlaningSerializer

class ListDQE(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = DQE.objects.all()
    serializer_class =DQESerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DQEFilter
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        mt_ttc = 0
        mt_ht  = 0
        
        for q in queryset:
            mt_ht+=q.montant_qte
            mt_ttc+=q.montant_qte + (q.montant_qte* (q.contrat.tva.id/100))
        
        c=self.request.query_params.get('contrat__numero',None)
        a=self.request.query_params.get('contrat__avenant',None)
        contrat=Contrat.objects.get(numero=c,avenant=a)
        response_data = super().list(request, *args, **kwargs).data
        return Response({
            'dqe':response_data,
            'extra':{
                'ht': mt_ht,
                'ttc':mt_ttc,
                'tva': contrat.tva.id
            }
            
        }, status=status.HTTP_200_OK)


class ListDQECumule(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = DQECumule.objects.all()
    serializer_class =DQECumuleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DQECumuleFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        mt_ttc = 0
        mt_ht  = 0
        c=self.request.query_params.get('code_contrat',None)
        contrat=Contrat_Latest.objects.get(numero=c)
        
        for q in queryset:
            mt_ht+=q.montant_qte
            mt_ttc+=q.montant_qte + (q.montant_qte* (contrat.tva.id/100))
        
        response_data = super().list(request, *args, **kwargs).data
        return Response({
            'dqe':response_data,
            'extra':{
                'ht': mt_ht,
                'ttc':mt_ttc,
                'tva': contrat.tva.id
            }
            
        }, status=status.HTTP_200_OK)


class ListClient(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Clients.objects.all()
    serializer_class =ClientSerilizer
    filter_backends = [DjangoFilterBackend]
    filterset_class= ClientFilter



class ListPrixProduit(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = PrixProduit.objects.all()
    serializer_class =PrixProduitSerializer
    filter_backends = [DjangoFilterBackend]



class AddClient(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Clients.objects.all()
    serializer_class = ClientSerilizer
    

class AddDQE(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = DQE.objects.all()
    serializer_class = DQESerializer


class GetUnites(APIView):
    def get(self,request):
        try:
            u=Unite.objects.all().values('id','libelle')
            return Response(u,status=status.HTTP_200_OK)
        except Unite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GetProds(APIView):
    def get(self,request):
        try:
            u=Produits.objects.all().values('id','libelle')
            return Response(u,status=status.HTTP_200_OK)
        except Produits.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)





class AddContrat(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Contrat.objects.all()
    serializer_class = ContratSerializer






class AddCamion(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Camion.objects.all()
    serializer_class = CamionSerializer


class ListCamion(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Camion.objects.all()
    serializer_class =CamionSerializer
    filter_backends = [DjangoFilterBackend]





class contratKeys(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            keys=Contrat.objects.all().values_list('numero', flat=True).distinct()
            result=[str(k) for k in keys]
            return Response(result,status=status.HTTP_200_OK)
        except Contrat.DoesNotExist:
            return Response({'message':'Pas de contrat'},status=status.HTTP_404_NOT_FOUND)



class AvenantKeys(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self,request):
        num=self.request.query_params.get('num',None)
        try:
            keys=Contrat.objects.filter(numero=num).values_list('avenant', flat=True).distinct()
            result=[str(k) for k in keys]
            return Response(result,status=status.HTTP_200_OK)
        except Contrat.DoesNotExist:
            return Response({'message':'Pas d\' avenant'},status=status.HTTP_404_NOT_FOUND)


class LastAvenantKeys(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self,request):
        num=self.request.query_params.get('num',None)
        try:
            key=Contrat.objects.filter(numero=num).latest('avenant').avenant
            
            return Response(key,status=status.HTTP_200_OK)
        except Contrat.DoesNotExist:
            return Response({'message':'Pas d\' avenant'},status=status.HTTP_404_NOT_FOUND)




class AddFacture(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Factures.objects.all()
    serializer_class = FactureSerializer




class UpdateDQE(generics.UpdateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = DQE.objects.all()
    serializer_class = DQESerializer
    lookup_field = "pk"
    def get_object(self):
        pk = self.request.data.get(DQE._meta.pk.name)
        try:
            obj = DQE.objects.get(pk=pk)
        except DQE.DoesNotExist:
            raise NotFound("Object n'éxiste pas")
        self.check_object_permissions(self.request, obj)

        return obj


class DeleteDQE(generics.DestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = DQE.objects.all()
    serializer_class = DQESerializer

    def delete(self, request, *args, **kwargs):
        pk = request.data.get(DQE._meta.pk.name)
        if pk:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(pk__in=pk)
            self.perform_destroy(queryset)

        return Response({'Message': pk}, status=status.HTTP_200_OK)



class DeleteInvoice(generics.DestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Factures.objects.all()
    serializer_class = FactureSerializer

    def delete(self, request, *args, **kwargs):
        pk = request.data.get(Factures._meta.pk.name)
        if pk:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(pk__in=pk)
            self.perform_destroy(queryset)

        return Response({'Message': pk}, status=status.HTTP_200_OK)







class DeleteBL(generics.DestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = BonLivraison.objects.all()
    serializer_class = BonLivraisonSerializer

    def delete(self, request, *args, **kwargs):
        pk = request.data.get(BonLivraison._meta.pk.name)
        if pk:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(pk__in=pk)
            self.perform_destroy(queryset)

        return Response({'Message': pk}, status=status.HTTP_200_OK)





class ListFacture(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Factures.objects.all()
    serializer_class =FactureSerializer
    filter_backends = [DjangoFilterBackend]


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        rg_total = 0
        creance = 0
        response_data = super().list(request, *args, **kwargs).data
        for q in queryset:
            rg_total += q.montant_rg




        return Response({'facture': response_data,
                         'extra': {

                             'rg_total': rg_total,
                             'creance': creance,

                         }}, status=status.HTTP_200_OK)





class ListDetail(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = DetailFacture.objects.all()
    serializer_class =DetailFactureSerializer
    filter_backends = [DjangoFilterBackend]




class ListAvance(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Avances.objects.all()
    serializer_class =AvanceSerializer
    filter_backends = [DjangoFilterBackend]


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total = 0
        rst = 0
        response_data = super().list(request, *args, **kwargs).data
        for q in queryset:
            total = total + q.montant_avance
            rst = rst + q.montant_restant

        return Response({'avances': response_data,
                         'extra': {

                             'total': total,
                             'rst': rst,


                         }}, status=status.HTTP_200_OK)





class AddAvance(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset= Avances.objects.all()
    serializer_class = AvanceSerializer