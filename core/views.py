import imp
from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from core.serializers import TeamSerializer

class CreateTeam(APIView):
    def post(self, request):
        serializer = TeamSerializer(data=request.data)