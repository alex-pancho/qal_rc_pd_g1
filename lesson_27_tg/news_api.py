
import requests

def get_news(country="UA", size =3):
    q_params = {"country": country, "size": size}
    responce = requests.get("https://freenewsapi.ai/v1/trends", params=q_params)
    return responce.json()

def get_top_news():
    r = get_news()
    top = []
    for t in r.get('trends'):
        top.append([t.get('title'), t.get('url')])
    return top


if __name__ == "__main__":
    r = get_news()
    top = []
    for t in r.get('trends'):
        top.append([t.get('title'), t.get('url')])
    print(top)