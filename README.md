# `currency_exchange`

## General Notes:

- The project is operating system dependent and was built in ubuntu Linux.
- This project requires aws credentials ideally of root user's(reason: no permission problems) in order to provision aws resources automatically.
- Euro has been considered as the base/from currency for task simplicity's sake and exchanges rates of euro to other currencies are directly scraped from https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html everyday.
- Project is built using django and makes use of zappa to deploy wsgi layer to lambda.

## TECHNICAL DESCRIPTION:

- The project uses beautifulsoup4 library to scrape euro to other currency's exchange rates from the URL mentioned above and this is an in-memory scheduler it does not persist if the application crashes.
- The scheduled job is configured to run on mon - fri every week at 01:05am. Runs once when program boots up and then gets scheduled.
- Zappa helps provision API GATEWAY automatically, creates an s3 bucket where it puts the zip file of the project and python libraries and then passes it to the lambda function. Zappa automatically transforms request from API gateway to wsgi interface of the project.
- Zappa makes use of the projects virtual environment (virtualenv library) and zips up all the manyLinux version of the packages that are in the environment.

### PREREQUISITES:

1. Updated ubuntu operating system version > 18.04
2. Python version > 3.7 but < 3.10(latest)
3. AWS credentials configured via aws-cli. (run: aws configure. requires; access key, secret key, region)

## Endpoints

### GET EURO EXCHANGE RATES:

There is only one endpoint exposed to get euro currency exchange rates information.

**Request:**

Base currency is always euro. You can pass query parameters listed below to fetch a specific currency or compare its rate against the previous day's rate. If you don't pass any of the query parameters listed below then it will respond with all of the exchange rates for the date the request was made.

**Url:** `GET <AWS-API-GATEWAY-URL>/production/app/get_euro_exchange_rates?toCurrency=USD&includePreviousDayComparison=true`

Query Params:

- toCurrency (optional: string) expected values(USD, AUD, SAR...) pass this to get exchange rates of this currency against euro.
- includePreviousDayComparison (optional: boolean) pass this to include previous day's rate difference as compared to today.

**Respone example 1:**

```json
{
  "exchange_rate_data": [
    {
      "currency": "<some-currency>",
      "rate": "<some-number>",
      "date": "2023-01-08 22:43:28.915517+00:00"
    }
    // ...
  ]
}
```

**Respone example 2:**

```json
{
  "currency": "<some-currency>",
  "rate": "<some-number>",
  "date": "2023-01-08 22:43:28.915517+00:00",
  "rateDifference": "<rate-difference>" //compared to previous day of date parameter.
}
```
