from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from api_gc.models import *
from api_gc.serializers import *
import serial
import serial.tools.list_ports
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




class GetWeight(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self, request):
        port=Parametres.objects.all().first().port
        print(port)
        baudrate = 9600
        data=None
        try:
            ser = serial.Serial(port, baudrate)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                cpt=1
                while data == None:
                    data = ser.readline().decode().strip()
                    cpt+=1
                    if(cpt==3):
                        break
                if(data == None and cpt==3):
                    return Response({'message': 'Impossible de capturer le poids'}, status=status.HTTP_404_NOT_FOUND)
                return Response({'data': data}, status=status.HTTP_200_OK)
            except :
                return Response({'message': 'Erreur'}, status=status.HTTP_400_BAD_REQUEST)


class ListContract(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Contrat.objects.all()
    serializer_class =ContratSerializer


class ListClient(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Clients.objects.all()
    serializer_class =ClientSerilizer

class AddClient(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Clients.objects.all()
    serializer_class = ClientSerilizer


class AddContrat(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Contrat.objects.all()
    serializer_class = ContratSerializer

class ListDQE(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = DQE.objects.all()
    serializer_class =DQESerializer
















