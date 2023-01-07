from bs4 import BeautifulSoup
import requests
from app.models import ExchangeRates
from app.utils import get_day_number
from datetime import datetime
import os


def scrape_exchange_rates():
    exchange_rates = []
    day_number = get_day_number()
    now = datetime.now()

    try:
        if is_scraped_already(day_number):
            return

        url = os.environ.get('EXCHANGE_RATES_SOURCE_URL')
        html = requests.get(url).text

        soup = BeautifulSoup(html, "html.parser")
        forex_table = soup.find('table', class_='forextable')

        for table_row in forex_table.tbody.find_all('tr'):
            currency_row = table_row.find('td', class_='currency')
            rate_row = table_row.find('td', class_='spot number')

            exchange_rates.append(
                {'currency': currency_row.text.strip(), 'rate': float(rate_row.span.text.strip())})

        with ExchangeRates.batch_write() as batch:
            items = [ExchangeRates(currency=item['currency'], rate=item['rate'], date=now, dayNumber=day_number)
                     for item in exchange_rates]
            for item in items:
                batch.save(item)

    except Exception as e:
        print('scheduler session failed', e)
    print('scheduler ran succesfully')


def is_scraped_already(day_number):
    try:
        ExchangeRates.get('USD', day_number)
        return True
    except:
        print('exchange rates do not exist, scraping...')

    return False
