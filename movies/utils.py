import datetime
from ast import literal_eval

import requests

from django.conf import settings


def fetch_api_data(title, serializer):
    response = requests.get(f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t={title}')
    fetched_data = response.json()

    if not literal_eval(fetched_data.get('Response', False)):
        raise RuntimeError(fetched_data['Error'])

    data = {field.lower(): value for field, value in fetched_data.items() if field.lower() in serializer.fields}

    parsed_values = {
        'year': int(data['year']),
        'released': datetime.datetime.strptime(data['released'], '%d %b %Y').strftime('%Y-%m-%d'),
        'metascore': int(data['metascore']),
        'imdbrating': float(data['imdbrating']),
        'dvd': datetime.datetime.strptime(data['dvd'], '%d %b %Y').strftime('%Y-%m-%d')
    }

    data.update(parsed_values)
    return data
