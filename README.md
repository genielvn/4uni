# 4uni

generate a new key
```
django-admin shell
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
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
to drop all tables and reset it to initial state, delete all files in the migration folder and do the following
```
py manage.py sqlflush
```
```
py manage.py flush
```
```
py manage.py makemigrations
```
```
py manage.py migrate
```
```
py manage.py sqlmigrate
```


if you see a conflict between user and admin shit, or something like that, comment 'django.contrib.admin' on setting.py and the admin url on fouruni/urls.py. idk why, but i am getting fucking errors.
