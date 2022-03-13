from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    MEMBER = "TL"
    LEADER = "TL"
    type_choices = [
        (MEMBER, "Member"),
        (LEADER, "Leader")
    ]

    user_type = models.CharField(choices=type_choices,default=MEMBER, max_length=100)
    availability = models.BooleanField(default=True)


class Task(models.Model):
    ASSIGNED="Assigned"
    IN_PROGRESS="In Progress"
    UNDER_REVIEW="Under Review"
    DONE="Done"
    status_choices = [
        (ASSIGNED, "Assigned"),
        (IN_PROGRESS, "In Progress"),
        (UNDER_REVIEW, "Under Revieww"),
        (DONE, "Done")
    ]

    name=models.CharField(max_length=250)
    description=models.TextField()
    team_leader=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="teamLeaderOf")
    members=models.ManyToManyField(User, related_name="membersOf")
    status=models.CharField(choices=status_choices, default=ASSIGNED, max_length=20)

class Team(models.Model):
    name=models.CharField(max_length=100)
    team_leader=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="teamLeaderOfTeam")
    members=models.ManyToManyField(User, related_name="membersOfTeam")


# many to many field because one employee can take on multiple tasks and one task can be assigned to multiple employees