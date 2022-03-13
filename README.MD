Instructions to set-up

Install everything from the "requirments.txt" file > pip install -r requirements.txt

This should have installed all the required modules.

Install redis - https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04
Check if redis is active 
sudo systemctl start redis

The result should look something like 
Loaded: loaded (/lib/systemd/system/redis-server.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2022-03-13 17:19:30 IST; 6s ago
       Docs: http://redis.io/documentation,
             man:redis-server(1)
    Process: 33703 ExecStart=/usr/bin/redis-server /etc/redis/redis.conf (code=exited, status=0/SUCCESS)
   Main PID: 33706 (redis-server)
      Tasks: 4 (limit: 19028)
     Memory: 1.9M
     CGroup: /system.slice/redis-server.service
             └─33706 /usr/bin/redis-server 127.0.0.1:6379

Install postman (to send api requests)
Since register, login facilities havent been built, I'm using a dummy user in all apis.
Create a few users (Try to make some of them leaders, by default they will be Members)

Now run these three commands on separate terminals
python manage.py runserver
celery -A task_tracker worker -l INFO
celery -A task_tracker beat

and you are good to go.

Endpoints
1. GetAuthenticated (GET /get-auth)
This api generates the jwt which will be used for authentication in all other apis.

2. CreateTeam (POST /team)
Requires the team name, and a comma separated string of ids of members like 1,2,3,4

3. GetAvailabilityOfTeamMembers (GET /availability)
Gives the availability of team members in a json format.

4. CreateTask (POST /task)
Required inputs are task_name, priority, start_date, end_date, and member_ids in a comma separated string - 1,2,3,4

5. UpdateTask (PATCH /task)
An update_title field needs to be given to explain the update briefly. Any number of fields can be updated at a given time.

6. GetStatusChangeReport (GET /report)
Get change report via email.