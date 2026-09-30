# Заняття 26. Проєкт веб-скраперу

## Мета заняття

Після заняття ви зможете:

* пояснити що таке веб-скрапінг;
* отримувати HTML сторінок;
* використовувати бібліотеку BeautifulSoup;
* знаходити елементи за тегами, атрибутами та CSS-класами;
* збирати дані із веб-сторінок;
* оформлювати результати у вигляді класів;
* використовувати декоратор `@property`;
* створювати прості веб-скрапери.

# Що таке веб-скрапінг

Веб-скрапінг (Web Scraping) — це автоматичне отримання даних із веб-сторінок.

Приклади:

* моніторинг цін;
* збір новин;
* аналіз вакансій;
* перевірка контенту сайтів;
* автоматизоване тестування.

# Як працює веб-скрапер

Типовий алгоритм:

```text
Отримати HTML
        ↓
Розібрати документ
        ↓
Знайти потрібні елементи
        ↓
Витягнути дані
        ↓
Зберегти результат
```

# HTML як дерево

Будь-яка веб-сторінка складається з HTML-тегів.

Приклад:

```html
<html>
    <body>

        <h1>Python Course</h1>

        <p>BeautifulSoup Example</p>

    </body>
</html>
```

Структура нагадує дерево.

# Інструменти для веб-скрапінгу

Найчастіше використовують:

* requests
* BeautifulSoup
* lxml
* Selenium

Сьогодні будемо працювати з BeautifulSoup.

# Встановлення бібліотек

```bash
pip install requests
pip install beautifulsoup4
```

# Отримання HTML сторінки

Для завантаження сторінки використовуємо requests.

```python
import requests

response = requests.get(
    "https://example.com"
)

print(response.status_code)
```

# Отримання HTML-коду

```python
import requests

response = requests.get(
    "https://example.com"
)

print(response.text)
```

Властивість:

```python
response.text
```

містить HTML сторінки.

# Створення BeautifulSoup

```python
from bs4 import BeautifulSoup

html = """
<h1>Hello</h1>
"""

soup = BeautifulSoup(
    html,
    "html.parser"
)
```

# Пошук першого елемента

Метод:

```python
find()
```

повертає перший знайдений елемент.

```python
title = soup.find("h1")

print(title)
```

Результат:

```html
<h1>Hello</h1>
```

# Отримання тексту

```python
title = soup.find("h1")

print(title.text)
```

Результат:

```text
Hello
```

# Приклад HTML

```html
<div>
    <h2>Python</h2>
    <h2>Java</h2>
    <h2>C#</h2>
</div>
```

# Пошук усіх елементів

Метод:

```python
find_all()
```

```python
titles = soup.find_all("h2")

print(titles)
```

# Перебір результатів

```python
titles = soup.find_all("h2")

for title in titles:
    print(title.text)
```

Результат:

```text
Python
Java
C#
```

# Пошук за CSS-класом

HTML:

```html
<div class="price">
    100
</div>
```

Пошук:

```python
price = soup.find(
    class_="price"
)

print(price.text)
```

# Пошук за атрибутом

HTML:

```html
<a href="/news">
    News
</a>
```

Пошук:

```python
link = soup.find("a")

print(link["href"])
```

Результат:

```text
/news
```

# CSS селектори

BeautifulSoup підтримує CSS-селектори.

Метод:

```python
select()
```

# Пошук через select

```python
titles = soup.select(
    ".product-title"
)
```

або

```python
links = soup.select(
    "a"
)
```

# Практичний HTML

```html
<div class="product">

    <h2 class="title">
        Laptop
    </h2>

    <span class="price">
        1000
    </span>

</div>
```

# Отримання назви товару

```python
title = soup.find(
    class_="title"
)

print(title.text)
```

# Отримання ціни

```python
price = soup.find(
    class_="price"
)

print(price.text)
```

# Повний приклад

```python
from bs4 import BeautifulSoup

html = """
<div class="product">
    <h2 class="title">Laptop</h2>
    <span class="price">1000</span>
</div>
"""

soup = BeautifulSoup(
    html,
    "html.parser"
)

title = soup.find(
    class_="title"
).text

price = soup.find(
    class_="price"
).text

print(title)
print(price)
```

# Створення моделі даних

Отримані дані зручно зберігати в класах.

```python
class Product:

    def __init__(
        self,
        title,
        price
    ):
        self.title = title
        self.price = price
```

# Створення об'єкта

```python
product = Product(
    title="Laptop",
    price=1000
)

print(product.title)
```

# Навіщо потрібен @property

Іноді дані потрібно обчислювати автоматично.

Без property:

```python
product.get_price()
```

З property:

```python
product.price
```

Виглядає як звичайний атрибут.

# Перший приклад property

```python
class Product:

    def __init__(self, price):
        self._price = price

    @property
    def price(self):
        return self._price
```

# Використання property

```python
product = Product(100)

print(product.price)
```

Результат:

```text
100
```

# Обчислювана властивість

```python
class Product:

    def __init__(self, price):
        self.price = price

    @property
    def price_with_tax(self):
        return self.price * 1.2
```

# Використання

```python
product = Product(100)

print(product.price_with_tax)
```

Результат:

```text
120.0
```

# Проєкт: скрапер товарів

Створимо HTML.

```html
<div class="product">
    <h2>Laptop</h2>
    <span>1000</span>
</div>

<div class="product">
    <h2>Mouse</h2>
    <span>50</span>
</div>
```

# Клас Product

```python
class Product:

    def __init__(
        self,
        name,
        price
    ):
        self.name = name
        self.price = int(price)

    @property
    def price_with_tax(self):
        return round(
            self.price * 1.2,
            2
        )
```

# Збір даних

```python
products = []

items = soup.find_all(
    class_="product"
)

for item in items:

    name = item.find("h2").text

    price = item.find("span").text

    product = Product(
        name,
        price
    )

    products.append(product)
```

# Виведення результату

```python
for product in products:

    print(product.name)

    print(product.price)

    print(product.price_with_tax)
```

# Типові проблеми скраперів

* Зміна структури сайту
* Відсутність елементів
* Блокування ботів
* Динамічний контент JavaScript
* Повільна робота мережі

Саме тому потрібна обробка помилок.

# Безпечний пошук

Погано:

```python
title = soup.find(
    class_="title"
).text
```

Якщо елемент відсутній — буде помилка.

# Кращий варіант

```python
title = soup.find(
    class_="title"
)

if title:
    print(title.text)
```

# Де використовується веб-скрапінг

* Тестування сайтів
* Моніторинг цін
* SEO-аналітика
* Збір вакансій
* Бізнес-аналітика
* Пошукові системи

# Підсумок

На цьому занятті ми:

* познайомилися з веб-скрапінгом;
* використовували requests;
* працювали з BeautifulSoup;
* знаходили елементи через find і find_all;
* використовували CSS-селектори;
* створювали моделі даних;
* вивчили декоратор @property;
* реалізували простий веб-скрапер товарів.

Веб-скрапінг є одним із найпопулярніших способів автоматичного збору інформації з веб-сайтів і часто використовується як у тестуванні, так і в аналітиці даних.
