from django.apps import AppConfig
from app.models import ExchangeRates
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from exchange_rates_job import scrape_exchange_rates
from pytz import utc


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        if not ExchangeRates.exists():
            print('spawning exchange rates table in db...')
            ExchangeRates.create_table(
                read_capacity_units=30, write_capacity_units=30, wait=True)

        print('setting up scheduler to scrape exchange rates and store them to the databse')

        scrape_exchange_rates()  # run once every boot time then get scheduled
        scheduler = BackgroundScheduler(timezone=utc)
        scheduler.add_job(scrape_exchange_rates, 'cron',
                          day_of_week='mon-fri', hour=1, minute=5)  # scheduled to run Mon-Fri at 1:05am
        scheduler.start()

        # uncomment below to run once or locally
        # scrape_exchange_rates()
