import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','veturilo.settings')

import django
django.setup()

# from time import sleep
from scraper.scripts.tasks import reduce_data, delete_old
from datetime import datetime

if __name__ == '__main__':
    present_date = datetime.now()
    if present_date.day == 1:
        reduce_data()
        delete_old()
