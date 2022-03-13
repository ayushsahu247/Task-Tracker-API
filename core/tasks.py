from codecs import ignore_errors
import smtplib
from email.message import EmailMessage
from datetime import date


from celery.decorators import periodic_task
from celery.task.schedules import crontab
from core.models import TaskUpdates, Task

@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="status_change_updates",
    ignore_result=True
)
def status_change_updates():
    #send mail to all team leaders???
    task_updates = TaskUpdates.objects.filter(updated_on=date.today())
    content = ''
    subject = 'Update'
    for update in task_updates:
        content='\n {} - {}'.format(update.update_title, update.task.id)
        send_mail(update.task.team_leader.email, subject, content)



@periodic_task(
    run_every=(crontab(minute='0', hour='0')),
    name="status_change_updates",
    ignore_result=True
)
def deadline_miss_update():
    print("Deadline Missed")
    missed_tasks=[]
    for task in Task.objects.filter(status__in=["Assigned", "In Progress"]):
        if task.end_date<date.today():
            for member in task.members.all():
                send_mail( member.email, "Deadline Missed","deadline missed for {}".format(task.id))



def send_mail(recepient, subject, content):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'from@gmail.com'  
    msg['To'] = recepient
    msg.set_content(content)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
        smtp.login('placeholder_email', 'placeholder_password')
        smtp.send_message(msg)
