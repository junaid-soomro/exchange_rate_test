from rest_framework.decorators import api_view
from app.models import ExchangeRates
from django.http import HttpResponse
from .utils import get_day_number, is_true
import json


@api_view(['GET'])
def get_euro_exchange_rates(request):
    try:

        day_number = get_day_number()
        query_params = request.query_params

        exchange_rate_data = []
        if not query_params:
            for item in ExchangeRates.scan(ExchangeRates.dayNumber == day_number):
                exchange_rate_data.append(
                    {"currency": item.currency, "rate": item.rate, "date": str(item.date)})

            return HttpResponse(json.dumps({'exchange_rate_data': exchange_rate_data}), content_type="application/json")

        to_currency = query_params.get('toCurrency')
        includePreviousDayComparison = query_params.get(
            'includePreviousDayComparison')

        if not to_currency:
            raise Exception(
                "invalid query parameter received. Allowed: (toCurrency:string, includePreviousDayComparison:boolean)")

        exchange_rate_today = ExchangeRates.get(to_currency, day_number)
        exchange_rate_delta = None

        exchange_rate_delta = {
            "currency": to_currency,
            "rate": exchange_rate_today.rate, "date": str(exchange_rate_today.date),
            "previous rate": None, "previous date": None
        }

        if is_true(includePreviousDayComparison):
            try:
                exchange_rate_yesterday = ExchangeRates.get(
                    to_currency, day_number - 1)
                exchange_rate_delta["previous rate"] = exchange_rate_yesterday.rate
                exchange_rate_delta["previous date"] = str(
                    exchange_rate_yesterday.date)

            except:
                # log to server
                print('previous day record does not exist for this currency')

        return HttpResponse(json.dumps({**exchange_rate_delta}), content_type="application/json")

    except Exception as e:
        message = str(e) if str(e) != 'None' else 'something went wrong'
        if isinstance(e, ExchangeRates.DoesNotExist):
            message = "not exist! no rate exchange record found against this currency"
        return HttpResponse(json.dumps({'error': message}), status=400, content_type="application/json")
