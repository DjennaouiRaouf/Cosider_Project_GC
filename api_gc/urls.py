from django.urls import path

from api_gc.views import *

urlpatterns = [
    path('adduser/', CreateUserView.as_view()),
    path('login/',Login.as_view()),
    path('logout/',Logout.as_view()),
    path('whoami/',WhoamiView.as_view()),

    path('getcontract/',ListContract.as_view()),
    path('addcontract/',AddContrat.as_view()),
    path('getclient/',ListClient.as_view()),
    path('addclient/',AddClient.as_view()),
    path('getdqe/',ListDQE.as_view()),
    path('getcumuledqe/',ListDQECumule.as_view()),
    path('contractkeys/',contratKeys.as_view()),
    path("avenant/",AvenantKeys.as_view()),
    path('getpprod/',ListPrixProduit.as_view()),
    path('adddqe/',AddDQE.as_view()),
    path('getimg/',ListImages.as_view()),


    path('delbl/',DeleteBL.as_view()),
    path('getunite/',GetUnites.as_view()),
    path('getprod/',GetProds.as_view()),
    path('getbl/',ListBL.as_view()),
    path('addbl/', AddBL.as_view()),



    path('addcamion/',AddCamion.as_view()),
    path('getcamion/',ListCamion.as_view()),

    path('addfacture/', AddFacture.as_view()),
    path('getfacture/', ListFacture.as_view()),




    path('updatedqe/',UpdateDQE.as_view()),
    path('deldqe/',DeleteDQE.as_view()),

    path('delinvoice/',DeleteInvoice.as_view()),

    path('getdet/',ListDetail.as_view()),

    path('getavance/',ListAvance.as_view()),

    path('addavance/',AddAvance.as_view()),


]
