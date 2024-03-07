from django.urls import path

import api_gc
from api_gc.views import *

urlpatterns = [
    path('adduser/', CreateUserView.as_view()),
    path('login/',Login.as_view()),
    path('logout/',Logout.as_view()),
    path('whoami/',WhoamiView.as_view()),
    path('getweight/',GetWeight.as_view()),
    path('getcontract/',ListContract.as_view()),
    path('addcontract/',AddContrat.as_view()),
    path('getclient/',ListClient.as_view()),
    path('addclient/',AddClient.as_view()),
    path('getdqe/',ListDQE.as_view()),
    path('adddqe/',AddDQE.as_view()),
    path('getimg/',ListImages.as_view()),
]
