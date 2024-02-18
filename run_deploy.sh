#!/bin/bash

python manage.py migrate
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@useflow.tech', '123456')" 2> /dev/null
python manage.py mock_user
python manage.py runserver 0.0.0.0:8000
