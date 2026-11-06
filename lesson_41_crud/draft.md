
- **C**reate — створити новий об’єкт.
- **R**ead — переглянути об’єкти або один об’єкт.
- **U**pdate — змінити існуючий об’єкт.
- **D**elete — видалити об’єкт.

```html
<form method="post">
  {% csrf_token %}
  <input type="text" name="title">
  <textarea name="content"></textarea>
  <button type="submit">Зберегти</button>
</form>
```