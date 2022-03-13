import imp
from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from core.serializers import TeamSerializer
from core.models import Team, User, Task, TaskUpdates
import jwt, datetime
from core.tasks import send_mail

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
            if payload['type']=='TL':
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
        if payload['type']=='TL':
            data=[]
            if team_id:
                team = Team.objects.get(id=int(team_id))
                members = team.members.all()
                for member in members:
                    data.append({member.username: member.availability})
                return Response({"success":True, "data":data})
        return Response({"success": False,"msg":"Authentication failed"})



class CreateTask(APIView):
    def post(self, request):
        user = User.objects.first()
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        if payload['type']=='TL':
            task_name=request.data.get("task_name")
            team_leader = user
            priority = request.data.get("priority")
            start_date = request.data.get("start_date")
            end_date = request.data.get("end_date")
            description = request.data.get("description")
            member_ids = request.data["members"].split(",")
            if not task_name and priority and start_date and end_date and member_ids and description:
                return Response({"success":False, "msg":"Incorrect/Insufficient Parameters"})
            task = Task.objects.create(name=task_name, team_leader=team_leader, priority=priority, description=description,start_date=start_date, end_date=end_date)
            for id in member_ids:
                print(id)
                member = User.objects.get(id=int(id))
                if member.availability:
                    task.members.add(member)
                else:
                    return Response({"success":False, "msg":"Team Member is not available"})
            return Response({"success":True, "msg":"Task created successfully"})
        return Response({"success":False, "msg":"Forbidden"})

    def patch(self, request):
        user = User.objects.first()
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        type = payload["type"]
        task = Task.objects.get(id=request.data.get("task_id"))
        
        update_title = request.data.get("update_title")
        if not update_title:
            return Response({"success":False, "msg":"update_title field is required"})

        fields = [f.name for f in Task._meta.get_fields()]
        fields.remove("status")
        if user in task.members.all():
            if user.user_type!="TL":
                for field in field:
                    if field in request.data:
                        return Response({"success":False, "msg":"Forbidden"})
                if "status" in request.data:
                    task.status=request.data["status"]
                    TaskUpdates.objects.create(update_title=update_title, modifier=user)
                    return Response({"success":True, "msg":"Task Updated"})
            else:
                # full privileges
                if "status" in request.data:
                    task.status=request.data["status"]
                if "name" in request.data:
                    task.name=request.data["name"]
                if "description" in request.data:
                    task.description=request.data["description"]
                if "team_leader_id" in request.data:
                    task.team_leader=User.objects.get(id=int(request.data["team_leader_id"]))
                if "start_date" in request.data:
                    task.start_date=request.data["start_date"]
                if "end_date" in request.data:
                    task.end_date=request.data["end_date"]
                
                TaskUpdates.objects.create(update_title=update_title, modifier=user)
                return Response({"success":True, "msg":"Task Updated"})
        return Response({"success":False, "msg":"Forbidden"})

class GetStatusChangeReport(APIView):
    def get(self, request):
        user = User.objects.first()
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        type = payload["type"]
        if type=="TL":
            date = request.data["date"]
            task_updates = TaskUpdates.objects.filter(updated_on=date)
            content = ''
            subject = 'Update'
            for update in task_updates:
                if update.task.team_leader==user:
                    content='\n {} - {}'.format(update.update_title, update.task.id)
                    send_mail(user, subject, content)
            return Response({"success":True})
        return Response({"success":False, "msg":"Authentication Failed"})

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