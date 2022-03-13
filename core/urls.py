from django.urls import path 
from core.views import CreateTeam

urlpatterns = [
    path('', CreateTeam.as_view())
]