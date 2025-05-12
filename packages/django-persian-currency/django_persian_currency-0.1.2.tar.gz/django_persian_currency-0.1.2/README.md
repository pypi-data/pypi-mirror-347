# Django Persian Currency

A simple Django template tag for formatting Iranian currency values (تومان) into human-readable formats like:

- `1,000,000` → `1 میلیون تومان`
- `500,000` → `500 هزار تومان`
- `123,456` → `123,456 تومان`

---

## ✨ Features

- Converts raw integers into **میلیارد**, **میلیون**, or **هزار تومان** where appropriate
- Falls back to comma-separated `تومان` when not divisible
- Safe default for invalid input
- Optional support for Persian digits (you can easily enable it)

---

## 🚀 Installation

```bash
pip install django_persian_currency
```

#### Add 'django_persian_currency' to your INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    ...
    'django_persian_currency',
]
```

## 🛠 Usage

In any Django template, first load the template tags:

```
{% load toman_filters %}
```

Then use the format_toman filter:

```
{{ 1000000|format_toman }}  {# Output: 1 میلیون تومان #}
{{ 725500|format_toman }}   {# Output: 725,500 تومان #}
{{ 500000|format_toman }}   {# Output: 500 هزار تومان #}
```

## 🧪 Testing
You can test it inside a Django shell:

```
python manage.py shell
```

```python
from django.template.defaultfilters import register
from django_persian_currency.templatetags.toman_filters import format_toman

format_toman(1500000)  # Output: '1 میلیون تومان'
```

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.