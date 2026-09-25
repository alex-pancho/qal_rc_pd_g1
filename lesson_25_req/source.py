import requests
import os
import json

from dotenv import load_dotenv

load_dotenv()

username = os.getenv("CAR_USERNAME")
password = os.getenv("CAR_PASSWORD")

base_url = 'https://car-service-api-and-ui.onrender.com'

def get_web_data(url_enpoint, userdata:dict={}, headers={}):
    url = f"{base_url}/{url_enpoint}"
    response = requests.get(url, params=userdata, headers=headers)
    return response

def post_web_data(url_enpoint, userdata:dict={}, headers:dict={}):
    url = f"{base_url}/{url_enpoint}"
    response = requests.post(url, json=userdata, headers=headers)
    return response

def processing_response_body(response):
    try:
        data = response.json()  # отримання даних у форматі JSON
    except json.JSONDecodeError:
        data = {"nojson": response.text}
    return data

def get_token():
    url_enpoint = "api/auth/signin/"
    userdata = {'username': username, 'password': password}
    response = post_web_data(url_enpoint, userdata)
    body = processing_response_body(response)
    return body.get('access')


if __name__ == "__main__":
    #url = 'http://jsonplaceholder.typicode.com/posts/1/comments'
    # url_enpoint = "api/auth/signin/"
    # userdata ={'username': "panix", 'password': 'LetMyPeople2G)'}
    # response = post_web_data(url_enpoint, userdata)
    # body = processing_response_body(response)
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    print(headers)

    # logout_post = "api/auth/logout/"
    # response = post_web_data(logout_post, headers=headers)

    brands_get = "api/brands/"
    response = get_web_data(brands_get, headers=headers)
    body = processing_response_body(response)
    print(body)

    models_get = "api/models/"
    userdata = {"brand": 1}
    response = get_web_data(models_get, userdata, headers=headers)
    body = processing_response_body(response)
    print(body)
