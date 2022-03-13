from datetime import datetime
import imp
from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from core.serializers import TeamSerializer
from core.models import Team, User
import jwt, datetime

class CreateTeam(APIView):
    def post(self, request):
        print(request.data)
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            # check if the user is a Leader using jwt
            user = User.objects.first()
            # user = request.user for generalized
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Unauthenticated')
            
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            if payload('type')=='TL':
                team = Team.objects.create(name=request.data["name"], team_leader=user)
                member_ids = request.data["members"].split(",")
                for id in member_ids:
                    team.members.add(User.objects.get(id=int(id)))
                return Response({"success": True,"msg":"Team created successfully"}, status=status.HTTP_200_OK)
            else:
                raise AuthenticationFailed("Unauthenticated")
        return Response({"Invalid Request"})

class GetAvailabilityOfTeamMembers(APIView):
    def get(self, request):
        # check if the user is a Leader using jwt somehow
        team_id = request.data.get("team_id")
        user = User.objects.first()
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        if payload('type')=='TL':
            if team_id:
                team = Team.objects.get(id=int(team_id))
                members = team.members.all()
                availability_dict = {}
                for member in members:
                    availability_dict[member.id]=member.availability
                return Response(availability_dict)
        return Response({"success": False,"msg":"Authentication failed"})

class CreateTask(APIView):
    def post(self, request):
        pass

class UpdateTask(APIView):
    def post(self, request):
        pass

class GetStatusChangeReport(APIView):
    def get(self, request):
        pass

class GetAuthenticated(APIView):
    def get(self, request):
        user = User.objects.first()
        payload = {
            'id': user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow(),
            'type': user.user_type
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt',value=token, httponly=True)
        response.data = {
            'jwt':token
        }
        return response