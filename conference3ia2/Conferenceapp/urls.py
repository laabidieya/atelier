from django.urls import path
from . import views
from .views import *


urlpatterns = [
    # Liste des conférences
    path("liste/", ConferenceList.as_view(), name="liste_conferences"),

    # Détails d'une conférence
    path("<int:pk>/", ConferenceDetails.as_view(), name="conference_details"),

    # Ajouter une nouvelle conférence
    path("add/", ConferenceCreate.as_view(), name="conference_add"),

    # Modifier une conférence existante
    path("<int:pk>/modifier/", ConferenceUpdate.as_view(), name="conference_update"),
    path("<int:pk>/delete/", ConferenceDelete.as_view(), name="conference_delete"),
    
    # Liste des soumissions
    path("submissions/liste/", ListSubmissions.as_view(), name="liste_submissions"),
    
    # Ajouter une soumission
    path("submissions/add/", AddSubmission.as_view(), name="submission_add"),
    
    # Modifier une soumission
    path("submissions/<str:submission_id>/modifier/", UpdateSubmission.as_view(), name="submission_update"),
    
    # Détails d'une soumission
    path("submissions/<str:submission_id>/", DetailSubmission.as_view(), name="submission_details"),
]

