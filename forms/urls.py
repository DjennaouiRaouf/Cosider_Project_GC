from django.urls import path

from forms.views import *

urlpatterns = [

    path('signupform/',SignupFields.as_view()),
    path('signupformds/',SignupFieldsDS.as_view()),

    path('contratlistform/',ContratFieldsList.as_view()),
    path('contrataddform/',ContratFieldsAddUpdate.as_view()),
    path('contratfilterform/',ContratFilterForm.as_view()),

    path('clientlistform/', ClientFieldsList.as_view()),
    path('clientaddform/', ClientFieldsAddUpdate.as_view()),
    path('clientfilterform/', ClientFilterForm.as_view()),

    path('dqelistform/',DQEFieldsList.as_view()),
    path('dqeaddform/',DQEFieldsAddUpdate.as_view()),
    path('dqefilterform/',DQEFilterForm.as_view()),


]