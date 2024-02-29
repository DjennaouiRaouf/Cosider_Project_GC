from django.urls import path

import api_gc
from api_gc.views import GetWeight

urlpatterns = [

    path('getweight/',GetWeight.as_view()),
]