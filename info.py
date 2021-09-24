import requests
from datetime import date
import ISO3166


# returns entire data from specific endpoint as python dictionary
def get_endpoint(param):
    API_ENDPOINT = f'https://disease.sh{param}'

    url_valid = True

    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        url_valid = False
        print(err)

    response_dict = response.json()

    return response_dict, url_valid


# returns country specific data as python dictionary
def covid_country(country):
    country = ISO3166.ISO3166rev.get(country)
    stats, url_valid = get_endpoint(f'/v3/covid-19/countries/{country}')
    vac_stats, dummy = get_endpoint(f'/v3/covid-19/vaccine/coverage/countries/{country}?lastdays=2&fullData=false')

    keys = ['active', 'critical', 'deaths', 'recovered', 'tests', 'today', 'cases']
    data = {x:stats[x] for x in keys if x in stats}

    today = date.today()
    if url_valid:
        data['Vaccine Doses'] = vac_stats['timeline'][f"{today.month}/{today.day-1}/{today.year%100}"]

    print(data)
    return data, url_valid


def covid_total():
    stats, url_valid = get_endpoint('/v3/covid-19/all')
    vac_stats, dummy = get_endpoint('/v3/covid-19/vaccine/coverage')

    keys = ['active', 'critical', 'deaths', 'recovered', 'tests', 'today', 'cases']
    data = {x:stats[x] for x in keys if x in stats}

    today = date.today()
    if url_valid:
        data['Vaccine doses'] = vac_stats[f"{today.month}/{today.day-1}/{today.year%100}"]

    return data, url_valid
