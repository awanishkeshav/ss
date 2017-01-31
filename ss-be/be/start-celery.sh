export C_FORCE_ROOT="true"
python ./manage.py celeryd -l info > /var/log/celery/celery.out 2>&1 &