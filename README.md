## Документация для кода TinkoffPayouts

### Описание

Класс `TinkoffPayouts` предоставляет методы для работы с API Тинькофф для осуществления платежей.

### Инициализация

Для создания экземпляра класса `TinkoffPayouts` необходимо передать следующие параметры:

- `terminal_key`: Ключ терминала, предоставленный Тинькофф.
- `x509_serial_number`: Серийный номер сертификата X509.
- `private_key_path` (необязательный): Путь к файлу с приватным ключом. По умолчанию - "private.key".

```python
api = TinkoffPayouts(terminal_key="YOUR_TERMINAL_KEY", x509_serial_number="YOUR_X509_SERIAL_NUMBER")
```

### Методы

#### add_customer

Добавление нового клиента.

**Параметры**:
- `customer_key`: Уникальный ключ клиента.
- `email` (необязательный): Электронная почта клиента.
- `phone` (необязательный): Телефон клиента.

**Пример использования**:
```python
response = api.add_customer(customer_key="CUSTOMER123", email="test@example.com", phone="+71234567890")
```

#### add_card

Добавление новой карты.

**Параметры**:
- `customer_key`: Уникальный ключ клиента.
- `check_type` (необязательный): Тип проверки. По умолчанию - "NO".

**Пример использования**:
```python
response = api.add_card(customer_key="CUSTOMER123")
```

#### get_card_list

Получение списка карт клиента.

**Параметры**:
- `customer_key`: Уникальный ключ клиента.

**Пример использования**:
```python
cards = api.get_card_list(customer_key="CUSTOMER123")
```

#### payment

Осуществление платежа.

**Параметры**:
- `payment_id`: Уникальный идентификатор платежа.

**Пример использования**:
```python
result = api.payment(payment_id="PAYMENT123")
```

#### get_state

Получение статуса платежа.

**Параметры**:
- `payment_id`: Уникальный идентификатор платежа.

**Пример использования**:
```python
status = api.get_state(payment_id="PAYMENT123")
```

### Примечания

Убедитесь, что у вас есть правильный приватный ключ и соответствующий ему сертификат X509 для работы с API Тинькофф.
