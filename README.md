# Документация для TinkoffPayouts API

## Описание

Класс `TinkoffPayouts` предоставляет методы для работы с массовыми выплатами через API Тинькофф Кассы. Он позволяет регистрировать клиентов, управлять данными клиентов и картами, инициировать и проверять выплаты.

## Перечисление методов:

1. [add_customer()](#add_customer) - Регистрация клиента.
2. [get_customer()](#get_customer) - Получение данных клиента.
3. [remove_customer()](#remove_customer) - Удаление клиента.
4. [get_card_list()](#get_card_list) - Получение списка привязанных карт клиента.
5. [add_card()](#add_card) - Привязка новой карты к клиенту.
6. [remove_card()](#remove_card) - Удаление привязанной карты.
7. [init_payout()](#init_payout) - Инициация выплаты.
8. [confirm_payout()](#confirm_payout) - Подтверждение выплаты.
9. [get_payout_status()](#get_payout_status) - Получение статуса выплаты.

## Список методов со всеми внутренними параметрами:

### <a name="add_customer"></a>add_customer()

- `customer_key` (str): Идентификатор клиента в системе Мерчанта.
- `email` (str, optional): Электронная почта клиента.
- `phone` (str, optional): Номер телефона клиента.

### <a name="get_customer"></a>get_customer()

- `customer_key` (str): Идентификатор клиента в системе Мерчанта.

### <a name="remove_customer"></a>remove_customer()

- `customer_key` (str): Идентификатор клиента в системе Мерчанта.

### <a name="get_card_list"></a>get_card_list()

- `customer_key` (str): Идентификатор клиента в системе Мерчанта.

### <a name="add_card"></a>add_card()

- `customer_key` (str): Идентификатор клиента в системе Мерчанта.
- `check_type` (str, optional): Тип проверки карты.

### <a name="remove_card"></a>remove_card()

- `card_id` (int): Идентификатор карты в системе Тинькофф Кассы.
- `customer_key` (str): Идентификатор клиента в системе Мерчанта.

### <a name="init_payout"></a>init_payout()

- `order_id` (str): Уникальный номер заказа в системе Мерчанта.
- `card_id` (str): Идентификатор карты пополнения.
- `amount` (int): Сумма в копейках.
- `data` (dict, optional): Дополнительные параметры.

### <a name="confirm_payout"></a>confirm_payout()

- `payment_id` (str): Идентификатор транзакции в системе Тинькофф Кассы.

### <a name="get_payout_status"></a>get_payout_status()

- `payment_id` (int): Идентификатор операции в системе Тинькофф Кассы.

## Как пользоваться:

Для начала, вам нужно создать экземпляр класса `TinkoffPayouts`, передав необходимые параметры:

```python
terminal_key = "YOUR_TERMINAL_KEY"
x509_serial_number = "YOUR_X509_SERIAL_NUMBER"
private_key_path = "path_to_private.key"

payouts = TinkoffPayouts(terminal_key, x509_serial_number, private_key_path)
```

Теперь, вы можете использовать различные методы класса для работы с API:

```python
# Регистрация нового клиента
response = payouts.add_customer("customer_123", email="customer@example.com", phone="+71234567890")

# Получение данных о клиенте
customer_data = payouts.get_customer("customer_123")

# Инициирование выплаты
payout_response = payouts.init_payout("order_456", "card_789", 10000)

# ... и так далее
```

Обратите внимание на то, что вы должны управлять исключениями и проверять ответы от API на наличие ошибок.
