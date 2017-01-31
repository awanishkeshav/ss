PIP installs
=============
pip install django-bootstrap3
pip install celery django-celery


Commands to create clean versions of api and sim
================================================
1) Take latest code from git
2) Go to mysql prompt
3) drop databases ssdb and simdb
4) Create databases by command -  source /Users/vipinjoshi/ss-git/ss-be/be/sqls/ddl.sql
5) Exit mysql prompt
6) Create migrations for beapi
rm -rf beapi/migrations
 python manage.py makemigrations beapi
7) Create migrations for besim (actually not too sure if we shall have different dbs)
rm -rf beapi/migrations
 python manage.py makemigrations beapi
8) Create migrations for beapi
python manage.py makemigrations besim
9) Migrate
python manage.py migrate
python manage.py migrate --database=simdb
10) Use seed data
Go to mysql prompt and run
source /Users/vipinjoshi/ss-git/ss-be/be/sqls/seed.sql
