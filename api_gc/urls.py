from django.urls import path

import api_gc
from api_gc.views import *

urlpatterns = [

    path('getweight/',GetWeight.as_view()),
    path('getcontract/',ListContract.as_view()),
    path('getdqe/',ListDQE.as_view()),
    path('getimg/',ListImages.as_view()),
]