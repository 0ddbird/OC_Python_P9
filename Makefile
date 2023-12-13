.PHONY: run tw

run:
		python manage.py runserver

tw:
		python manage.py tailwind start

sp:
		python manage.py shell_plus