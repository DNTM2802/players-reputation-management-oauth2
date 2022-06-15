source venv/bin/activate
#python3 manage.py runserver 127.0.0.1:8002

daphne tables_matchmaker.asgi:application --port 8002 --bind 127.0.0.1 -v2
docker run -p 6379:6379 -d redis:5
python manage.py runworker channels --settings=tables_matchmaker.settings -v2
