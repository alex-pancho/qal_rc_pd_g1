import time


def execute(func, arg):
    if arg == "Oleksandr":
        arg = "Alex"
    func(arg)


def say_hello(arg=""):
    print(f"Hello, {arg}!")

execute(say_hello, "Oleksandr")
execute(say_hello, "Oleksiy")

def logger(func):

    def wrapper():
        print("Function started")
        func()
        print("Function finished")

    return wrapper

@logger
def create_user():
    print("Creating user")


create_user()

def logger2(func):

    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper

@logger2
def create_user2(name, second):
    print(f"User {name} {second} created")


create_user2("Alex", second="Panix")


def log_request(func):

    def wrapper(*args, **kwargs):
        print(f"API call: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@log_request
def get_user(user_id):
    print(f"Loading user {user_id}")

get_user(100)


def measure_time(func):

    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        finish = time.time()

        print(f"{func.__name__} execution time: {finish - start:.3f}s")

        return result

    return wrapper


@measure_time
def load_data():
    time.sleep(1)


load_data()

def require_role(role):
    def decorator(func):
        def wrapper(user_role):
            if user_role != role:
                raise PermissionError("Access denied")

            return func(user_role)

        return wrapper

    return decorator

user_role = "admin"

@require_role("admin")
def delete_user(user_role):
    print("User deleted")

delete_user(user_role)

def retry(attempts):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    pass
            raise Exception("All attempts failed")
        return wrapper
    return decorator

@retry(3)
def send_request():
    # raise Exception
    print("GET url.com")

send_request()

def logger3(level):
    def decorator(func):
        def wrapper(*args, **kwargs):           
            result = func(*args, **kwargs)
            print(f"[{level}] {func.__name__}: {result}")
            return result
        return wrapper
    return decorator

@logger3("INFO")
def create_user3():
    return "CREATED"

@logger3("ERROR")
def delete_user3():
    return "WRONG TABLE"

create_user3()
delete_user3()

def memoize(func):
    cache = {}
    def wrapper(number):
        if number not in cache:
            cache[number] = func(number)

        return cache[number]

    return wrapper


@memoize
def square(number):
    print("Calculating...")
    return number * number

print(square(5))
print(square(5))
print(square(5))

# @app.route("/users")
# def get_users():
#     pass

# @login_required
# def profile(request):
#     pass

# @pytest.fixture
# def browser():
#     pass
