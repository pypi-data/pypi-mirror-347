![](https://i.imgur.com/izqgNh7.png)

# CrystalPayAPI - Python SDK для CrystalPay

[![PyPI version](https://img.shields.io/pypi/v/CrystalPayAPI.svg)](https://pypi.python.org/pypi/CrystalPayAPI/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Русская документация 
[English Version](#english-documentation)

### Оглавление
1. [Установка](#установка)
3. [Быстрый старт](#быстрый-старт)
3. [Инициализация](#инициализация)
4. [Методы работы](#методы-работы)
   - [Информация о кассе](#информация-о-кассе)
   - [Платежи](#платежи)
   - [Вывод средств](#вывод-средств)
   - [Курсы валют](#курсы-валют)
5. [Обработка ошибок](#обработка-ошибок)

### Установка
```bash
pip install CrystalPayAPI
```

### Быстрый старт

```python
from crystalpayapi import CrystalPayAPI, InvoiceType, PayoffSubtractFrom

# Инициализация
cp = CrystalPayAPI("Ваш_логин", "Secret_1", "Secret_2")

# Создание инвойса
invoice = cp.create_invoice(
    amount=100.0,
    invoice_type=InvoiceType.PURCHASE,
    lifetime=15,
    description="Оплата товара"
)

# Проверка статуса
invoice_info = cp.get_invoice(invoice["id"])
```

### Инициализация
```python
from crystalpayapi import CrystalPayAPI, InvoiceType, PayoffSubtractFrom

# Основной конструктор
cp = CrystalPayAPI(
    auth_login="Ваш_логин",      # Логин кассы
    auth_secret="Secret_1",      # Секретный ключ 1
    salt="Secret_2",             # Секретный ключ 2
    base_url="https://api.crystalpay.io/v2/"  # Опционально
)
```

### Методы работы

#### Информация о кассе
```python
# Получение информации о кассе
account_info = cp.get_me()
"""
{
    "id": "12345",
    "name": "Моя касса",
    "status_level": 2,
    "created_at": "2023-01-01 00:00:00"
}
"""

# Получение баланса
balance = cp.get_balance(hide_empty=True)
"""
{
    "RUB": {"amount": 1000, "currency": "RUB"},
    "BTC": {"amount": 0.05, "currency": "BTC"}
}
"""
```

#### Платежи
```python
# Создание платежа
invoice = cp.create_invoice(
    amount=500,
    invoice_type=InvoiceType.PURCHASE,
    lifetime=30,  # в минутах
    description="Оплата заказа #123",
    redirect_url="https://your-site.com/thanks"
)
"""
{
    "id": "inv_123",
    "url": "https://pay.crystalpay.io/?i=inv_123",
    "amount": 500,
    "type": "purchase"
}
"""

# Проверка статуса
status = cp.get_invoice("inv_123")
"""
{
    "id": "inv_123",
    "state": "paid",
    "amount": 500,
    "created_at": "2023-01-01 12:00:00"
}
"""
```

#### Вывод средств
```python
# Создание вывода
payoff = cp.create_payoff(
    amount=0.01,
    method="BTC",
    wallet="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    subtract_from=PayoffSubtractFrom.BALANCE
)
```

#### Курсы валют
```python
# Получение курсов
rates = cp.get_exchange_rates(["BTC", "ETH"])
"""
{
    "BTC": {"price": 2500000},
    "ETH": {"price": 150000}
}
"""
```

### Обработка ошибок
```python
from crystalpayapi import CrystalPayAPIError

try:
    cp.create_invoice(amount=100, ...)
except CrystalPayAPIError as e:
    print(f"Ошибка API: {e}")
```

---

## English Documentation

### Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Initialization](#initialization)
4. [Methods](#methods)
   - [Account Info](#account-info)
   - [Payments](#payments)
   - [Withdrawals](#withdrawals)
   - [Exchange Rates](#exchange-rates)
5. [Error Handling](#error-handling)

### Installation
```bash
pip install CrystalPayAPI
```

### Quick Start

```python
from crystalpayapi import CrystalPayAPI, InvoiceType, PayoffSubtractFrom

# Initialize client
cp = CrystalPayAPI("your_login", "secret1", "secret2")

# Create invoice
invoice = cp.create_invoice(
    amount=100.0,
    invoice_type=InvoiceType.PURCHASE,
    lifetime=15,
    description="Product payment"
)

# Check status
invoice_info = cp.get_invoice(invoice["id"])
```

### Initialization
```python
from crystalpayapi import CrystalPayAPI, InvoiceType, PayoffSubtractFrom

cp = CrystalPayAPI(
    auth_login="your_login",
    auth_secret="secret_1", 
    salt="secret_2",
    base_url="https://api.crystalpay.io/v2/"  # Optional
)
```

### Methods

#### Account Info
```python
# Get merchant info
account_info = cp.get_me()

# Get balances
balance = cp.get_balance(hide_empty=True)
```

#### Payments
```python
# Create invoice
invoice = cp.create_invoice(
    amount=100,
    invoice_type=InvoiceType.PURCHASE,
    lifetime=15,
    description="Order #123"
)

# Check status
status = cp.get_invoice(invoice["id"])
```

#### Withdrawals
```python
# Create withdrawal
payoff = cp.create_payoff(
    amount=0.1,
    method="BTC",
    wallet="3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5",
    subtract_from=PayoffSubtractFrom.BALANCE
)
```

#### Exchange Rates
```python
# Get rates
rates = cp.get_exchange_rates(["BTC", "USDT"])
```

### Error Handling
```python
try:
    cp.create_payoff(...)
except CrystalPayAPIError as e:
    print(f"API Error: {e}")
```

---

## License
MIT License. See [LICENSE](LICENSE) for details.