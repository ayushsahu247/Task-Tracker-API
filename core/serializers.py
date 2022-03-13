from rest_framework import serializers
from core.models import User, Team, Task

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name"]