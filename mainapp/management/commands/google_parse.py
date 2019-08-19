from django.core.management.base import BaseCommand
import requests, json
class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get('https://www.dota2.com/jsfeed/heropediadata?feeds=abilitydata&l=english')
        print(r.json())

#этот скрипт выполняется командой python manage.py google_parse, например чтобы прям с сайта грузануть в ДБ данные
#пример того, как через скрипт можно загрузить данные в ДБ и много всего прочего