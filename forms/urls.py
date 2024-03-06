from django.urls import path

from forms.views import *

urlpatterns = [

    path('signupform/',SignupFields.as_view()),
    path('signupformds/',SignupFieldsDS.as_view()),
    path('contratlistform/',ContratFieldsList.as_view()),
    path('contrataddform/',ContratFieldsAdd.as_view()),

]