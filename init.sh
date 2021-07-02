python manage.py migrate

python manage.py loaddata users/fixtures/users.yaml

python manage.py dumpdata users.User --format=yaml > users/fixtures/users.yaml
python manage.py dumpdata pages.Page --format=yaml > pages/fixtures/pages.yaml
python manage.py dumpdata menus.Menu --format=yaml > menus/fixtures/menus.yaml