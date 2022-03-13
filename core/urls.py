from django.urls import path 
from core.views import CreateTeam, GetAuthenticated, GetAvailabilityOfTeamMembers, CreateTask, GetStatusChangeReport

urlpatterns = [
    path('team', CreateTeam.as_view()),
    path('get-auth', GetAuthenticated.as_view()),
    path('availability', GetAvailabilityOfTeamMembers.as_view()),
    path('task', CreateTask.as_view()),
    path('report', GetStatusChangeReport.as_view())
]