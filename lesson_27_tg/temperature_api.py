import openmeteo_requests

import requests_cache
from retry_requests import retry


def get_temp():
    cache_session = requests_cache.CachedSession(
        ".cache",
        expire_after=3600
    )

    retry_session = retry(
        cache_session,
        retries=5,
        backoff_factor=0.2
    )

    openmeteo = openmeteo_requests.Client(
        session=retry_session
    )

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 50.4547,
        "longitude": 30.5238,
        "current": "temperature_2m",
        "timezone": "Europe/Kyiv",
    }

    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    current = response.Current()

    temperature = current.Variables(0).Value()

    return temperature


if __name__ == "__main__":
    temp = get_temp()
    print(f"Температура у Києві: {int(temp)}° C")