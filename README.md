# Документация для API Тинькофф кассы

## Описание
Эта библиотека предоставляет программный интерфейс для интеграции с сервисами Тинькофф Кассы. С её помощью можно автоматизировать процессы создания, управления и отслеживания транзакций.

## Как пользоваться:
1. **Установка и настройка**:
   - Установите библиотеку, используя команду 
   - `pip install -r requirements.txt`.

2. **Инициализация менеджеров**:
   ```python
    from TinkoffKassa.api import create_customer_manager, create_deal_manager

    customer_manager = create_customer_manager('your_terminal_key', 'your_x509')
    deal_manager = create_deal_manager('your_terminal_key')
    ```
3. **Вызов метода**:
    ```python
    deal_response = deal_manager.init_deal(order_id, amount)
    ```
   
## Список методов

### Класс `create_deal_manager`

1. `init_deal(self, order_id, amount)` - Инициирует сделку с указанным идентификатором заказа и суммой.

2. `confirm_deal(self, payment_id)` - Подтверждает сделку с указанным идентификатором платежа.

3. `cancel_deal(self, payment_id)` - Отменяет сделку с указанным идентификатором платежа.

4. `payment(self, payment_id, card_id, amount)` - Осуществляет платеж по идентификатору платежа, идентификатору карты и сумме.

### Класс `create_customer_manager`

1. `add_customer(self, customer_key, email: str = None, phone: int = None)` - Добавляет нового клиента с указанным ключом клиента, электронной почтой и телефоном.

2. `get_customer(self, customer_key)` - Возвращает информацию о клиенте по его ключу.

3. `remove_customer(self, customer_key)` - Удаляет клиента по его ключу.

4. `get_card_list(self, customer_key)` - Возвращает список карт, привязанных к клиенту по его ключу.

5. `add_card(self, customer_key, check_type: str = None)` - Добавляет карту к клиенту с возможностью указать тип проверки.

6. `check_3ds_version(self, payment_id, card_data, token)` - Проверяет версию 3DS для указанного платежа, данных карты и токена.

7. `remove_card(self, card_id, customer_key)` - Удаляет карту по её идентификатору и ключу клиента.