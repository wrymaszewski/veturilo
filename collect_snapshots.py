import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veturilo.settings')

import django
django.setup()

# from time import sleep
from scraper.scripts.tasks import take_snapshot
# from datetime import datetime

if __name__ == '__main__':
    # taking snapshots every 10min
    # for i in range(142):
        take_snapshot()
        # sleep(600)
