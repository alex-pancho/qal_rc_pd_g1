import requests

def get_method(url:str = "https://www.example.com", params:dict={}):
    """ Getting data... """
    response = requests.get(url, params=params)
    return response


def post_method(url:str = "https://www.example.com", data_to_send:dict = {}, xform=False):
    """ Getting data... """
    if xform:
        response = requests.post(url, data=data_to_send)
    else:
        response = requests.post(url, json=data_to_send)
    return response


def put_method(url:str = "https://www.example.com", data_to_send:dict = {}):
    """ Getting data... """
    response = requests.put(url, json=data_to_send)
    return response


def print_response(response):
    print("status code:", response.status_code)
    print("url:", response.url)
    print("headers:", response.headers)
    print("requests:", response.request.body)
    print("text:", response.text)


def get_jsonplaceholder():
    url = "https://jsonplaceholder.typicode.com/comments"
    params = {'postId': 1, 'email': 'Nikita@garfield.biz'}
    response = get_method(url, params)
    return response


def post_jsonplaceholder():
    url = 'http://jsonplaceholder.typicode.com/posts'
    data_to_send = {
        'userId': 1,
        'title': 'Some title',
        'email': "Sincere@april.biz"
    }
    return post_method(url, data_to_send)


def post_pastebin():
    url = "https://pastebin.com/api/api_post.php"
    post_data = dict(
        api_dev_key = "ulMHuv-FlPEloav7EYTG3u4jRLqizgxJ",
        api_paste_code = "Ми вивчаємо запити у пітон",
        api_option = "paste",
    )
    return post_method(url, post_data, xform=True)


if __name__ == "__main__":
    # url = 'http://jsonplaceholder.typicode.com/posts/1/comments'
    # response = get_method(url)
    # print_response(response)
    response = post_pastebin()
    print_response(response)