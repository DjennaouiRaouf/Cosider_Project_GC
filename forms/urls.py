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

    path('pprodlistform/',PrixProdFieldsList.as_view()),
    path('dqelistform/',DQEFieldsList.as_view()),
    path('dqeaddform/',DQEFieldsAddUpdate.as_view()),
    path('dqefilterform/',DQEFilterForm.as_view()),

    path('factureaddform/',FactureFieldsAddUpdate.as_view()),

    path('bllistform/',BLFieldsList.as_view()),
    path('bladdform/',BLFieldsAddUpdate.as_view()),
    path('blfilterform/',BLFilterForm.as_view()),

    path('facturelistform/',FactureFieldsList.as_view()),

    path('camionlistform/',CamionFieldsList.as_view()),
    path('camionaddform/',CamionAddUpdate.as_view()),
    path('camionfilterform/',CamionFilterForm.as_view()),



]