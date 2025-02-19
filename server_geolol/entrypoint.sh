export > /app/.env
python manage.py migrate
python manage.py first_setup
python manage.py runserver 0.0.0.0:8000