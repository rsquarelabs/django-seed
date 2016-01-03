# rsquarelabs-xyz api



This project uses PostgreSQL as primary data base.. For the very first time, run 
```
python manage.py makemigrations core
python manage.py migrate
```





## Technical Stack
- Django
- Django Restframework
- PostgreSQL (Primary Database)
- MongoDB (Secondary Database)


## Token based authentication api 

http://localhost:8000/restful/api-token-auth/

```bash
# create token 
curl -X POST -d "username=rrmerugu&password=welcome123" http://localhost:8000/restful/api-token-auth/

# refresh token
curl -X POST -H "Content-Type: application/json" -d '{"token":"<EXISTING_TOKEN>"}' http://localhost:8000/restful/api-token-refresh/
```

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class RestrictedView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request):
        data = {
            'id': request.user.id,
            'username': request.user.username,
            'token': str(request.auth)
        }
        return Response(data)
        
```
In header, pass the "Authorisation" : "JWT <token>"
 
JWT(default) is the prefix defined in the settings..  

## Milestones 
- Logger 
- Queing System - RabbitMQ & Celery [done]
- Emails
- 404, 500 , broken links email
- MongoDB as secondary
- Admin Panel, custom admin data

- RPC/socket - keep api connection alive 
- AngularJS
- D3 Graphs
- Write tests for above
- django-compressor
- sass



### How to implement Queing System

We implemented this queing system with rabbitmq and celery

1. ./rabbitmq-server 
2. python manage.py celeryd -l INFO
3. python manage.py runserver

```python
# in tasks.py
@celery.task
def add(x,y):
	return x + y

# in views.py
def test_celery(request):
	result = tasks.add.delay(10 , 30)
	return HttpResponse(result.task_id)

# in urls.py
urlpatterns = [
  ...
  url(r'^test-task$', views.test_celery),
 ]
```
Test the task `http://localhost:8000/restful/test-task`


### How to implement Logging 
```python
# import this in the file where you want to log 
import logging
logger = logging.getLogger(__name__)


# log what you want to 
logger.debug("Im debug message")
logger.info("Im info message")

```


### 404 & 500 Error Pages 

To see these, you must make some changes in `settings.py`:

```
DEBUG = False # you will see 404 and 500 error page only if this is False
ALLOWED_HOSTS = ['localhost']
```

But in `DEBUG=false` mode, static files wont be served, you can run it with `python manage.py runserver --insecure`

## Installation

brew install postgresql
pip install psycopg2


```

To have launchd start postgresql at login:
  mkdir -p ~/Library/LaunchAgents
  ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents
Then to load postgresql now:
  launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist
Or, if you don't want/need launchctl, you can just run:
  postgres -D /usr/local/var/postgres
==> Summary

```

## Reasons why I moved from MongoDB to PostgreSQL as Primary Database
1. MongoEngine support was removed recently(from 0.9) and don't know when they will be back, currently it is 0.10.5
2. MongoEngine support pymongo2.7, where as the latest is pymongo3.2
3. MongoEngine support djangorestframework till 3.0.5, where as currently it is 3.3.2
4. In PostgreSQL 9.4 more efficient  JSONB type is added, so **we can have a mix of relational and document data** (which is very likely).
5. https://www.quora.com/Which-database-should-I-use-for-a-killer-web-application-MongoDB-PostgreSQL-or-MySQL
6. http://www.aptuz.com/blog/is-postgres-nosql-database-better-than-mongodb/
7. http://thebuild.com/presentations/json2015-pgconfus.pdf


## Reasons why I used RabbitMQ than Redis 
1. http://stackoverflow.com/questions/9140716/whats-the-advantage-of-using-celery-with-rabbitmq-over-redis-mongodb-or-django
2. https://www.quora.com/What-is-the-difference-between-a-message-queue-and-a-task-queue-Why-would-a-task-queue-require-a-message-broker-like-RabbitMQ-Redis-Celery-or-IronMQ-to-function

## Reference

https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn


