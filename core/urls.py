from django.urls import path 
from core.views import CreateTeam, GetAuthenticated

urlpatterns = [
    path('team', CreateTeam.as_view()),
    path('get-auth', GetAuthenticated.as_view())
]