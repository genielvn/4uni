# 4uni

generate a new key
```
django-admin shell
from django.core.management.utils import get_random_secret_key  
get_random_secret_key() # dont include single quotes at the start and end
```

create .env file inside fouruni folder and type the following
```
SECRET_KEY=<paste it here>
```

dont forget to install the requirements
```
pip install -r requirements.txt
```

## working with the (fucking) database
to drop all tables and reset it to initial state, delete all files in the migration folder and do the following IN ORDER.
```
py manage.py sqlflush
py manage.py flush
py manage.py makemigrations
py manage.py sqlmigrate main xxxx # xxxx = the migration number
py manage.py migrate
```
if things doesnt work still, delete the fucking db. (this took me like 20 minutes to figure it out)

if you see a conflict between user and admin shit, or something like that, comment 'django.contrib.admin' on setting.py and the admin url on fouruni/urls.py. idk why, but i am getting fucking errors.

## Testing the database
```
py manage.py shell
from main.models import Board, Thread, User, Role, University, Reply

sample_board = Board.objects.create(board_id="pup", name="Polytecnic Universitiy of The Philippines")
sample_role = Role.objects.create(name="User")
sample_uni = University.objects.create(
    university_id = "up",
    name = "Polytecnic Universitiy of The Philippines",
    verified = True
)
sample_user = User.objects.create(
    username="Anonymous",
    password="test",
    role=sample_role,
    university=sample_uni
)
sample_thread = Thread.objects.create(
    title="Title 1",
    board=sample_board,
    username=sample_user,
    body="This is a body from Title 1"
)
sample_reply = Reply.objects.create(
    username=sample_user,
    thread=sample_thread,
    body="This is a reply.",
)
```