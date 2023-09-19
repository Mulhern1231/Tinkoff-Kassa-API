import base64
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import requests

class TinkoffPayouts:
    BASE_URL = "https://securepay.tinkoff.ru"
    
    def __init__(self, terminal_key, x509_serial_number, private_key_path="private.key"):
        self.terminal_key = terminal_key
        self.x509_serial_number = x509_serial_number
        self.private_key_path = private_key_path
        
    def generate_signature_and_digest(self, data):
        # Удалить ключи, которые не нужно включать в хэш
        keys_to_remove = ['DigestValue', 'SignatureValue', 'X509SerialNumber']
        filtered_data = {key: value for key, value in data.items() if key not in keys_to_remove}
        
        # Сортировка по ключам и конкатенация значений
        concatenated_string = ''.join([value for key, value in sorted(filtered_data.items(), key=lambda x: x[0])])
        
        # Вычисление SHA256 и кодирование в Base64
        hash_object = hashlib.sha256(concatenated_string.encode())
        digest_value = base64.b64encode(hash_object.digest()).decode()
        
        # Подпись с помощью RSA ключа и кодирование в Base64
        with open(self.private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
            
        signature = private_key.sign(
            hash_object.digest(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        signature_value = base64.b64encode(signature).decode()

        return digest_value, signature_value
    

    # Добавление клиента и работа с ним
    def add_customer(self, customer_key, email=None, phone=None):
        """
            Регистрирует клиента в связке с терминалом
        """
        data = {
            "TerminalKey": self.terminal_key,
            "CustomerKey": customer_key,
            "X509SerialNumber": self.x509_serial_number
        }
        
        if email:
            data["Email"] = email
            
        if phone:
            data["Phone"] = phone

        digest_value, signature_value = self.generate_signature_and_digest(data)

        data['DigestValue'] = digest_value
        data['SignatureValue'] = signature_value

        response = requests.post(f"{self.BASE_URL}/e2c/v2/AddCustomer", json=data)
        return response.json()

    def get_customer(self, customer_key):
        """
            Получение данных клиента
        """
        data = {
            "TerminalKey": self.terminal_key,
            "CustomerKey": customer_key,
            "X509SerialNumber": self.x509_serial_number
        }

        digest_value, signature_value = self.generate_signature_and_digest(data)

        data['DigestValue'] = digest_value
        data['SignatureValue'] = signature_value

        response = requests.post(f"{self.BASE_URL}/e2c/v2/GetCustomer", json=data)
        return response.json()
    
    def remove_customer(self, customer_key):
        """
            Удаление данных клиента
        """
        data = {
            "TerminalKey": self.terminal_key,
            "CustomerKey": customer_key,
            "X509SerialNumber": self.x509_serial_number
        }

        digest_value, signature_value = self.generate_signature_and_digest(data)

        data['DigestValue'] = digest_value
        data['SignatureValue'] = signature_value

        response = requests.post(f"{self.BASE_URL}/e2c/v2/RemoveCustomer", json=data)
        return response.json()

    def get_card_list(self, customer_key):
        """
        Получает список карт для указанного клиента.
        
        Parameters:
        - customer_key (str): Идентификатор клиента в системе Мерчанта.

        """

        data = {
            "TerminalKey": self.terminal_key,
            "CustomerKey": customer_key,
            "X509SerialNumber": self.x509_serial_number
        }

        digest_value, signature_value = self.generate_signature_and_digest(data)

        data['DigestValue'] = digest_value
        data['SignatureValue'] = signature_value

        response = requests.post("https://securepay.tinkoff.ru/e2c/v2/GetCardList", json=data)
        return response.json()

    def add_card(self, customer_key, check_type=None):
        """
            Инициализирует привязку карты к клиенту.
            
            Parameters:
            - customer_key (str): Идентификатор клиента в системе Мерчанта.
            - check_type (str, optional): Тип проверки карты. Если не передается, автоматически проставляется значение "NO".
        """
        data = {
            "TerminalKey": self.terminal_key,
            "CustomerKey": customer_key,
            "X509SerialNumber": self.x509_serial_number
        }

        # Если передан параметр check_type, добавляем его в данные запроса
        if check_type:
            data["CheckType"] = check_type

        digest_value, signature_value = self.generate_signature_and_digest(data)

        data['DigestValue'] = digest_value
        data['SignatureValue'] = signature_value

        response = requests.post("https://securepay.tinkoff.ru/e2c/v2/AddCard", json=data)
        return response.json()

    def check_3ds_version(self, payment_id, card_data, token):
        """
            Проверяет поддерживаемую версию 3DS протокола по карточным данным.
            
            Parameters:
            - payment_id (int): Уникальный идентификатор транзакции в системе Тинькофф Кассы.
            - card_data (str): Зашифрованные данные карты.
            - token (str): Подпись запроса.
        """
        data = {
            "TerminalKey": self.terminal_key,
            "PaymentId": payment_id,
            "CardData": card_data,
            "Token": token
        }

        response = requests.post("https://securepay.tinkoff.ru/e2c/v2/Check3dsVersion", json=data)
        return response.json()

    def remove_card(self, card_id, customer_key):
        """
            Удаляет карту, ранее привязанную к клиенту.
            
            Parameters:
            - card_id (int): Идентификатор карты в системе Тинькофф Кассы.
            - customer_key (str): Идентификатор клиента в системе Мерчанта.
        """
        data = {
            "TerminalKey": self.terminal_key,
            "CardId": card_id,
            "CustomerKey": customer_key,
            "X509SerialNumber": self.x509_serial_number
        }

        digest_value, signature_value = self.generate_signature_and_digest(data)

        data['DigestValue'] = digest_value
        data['SignatureValue'] = signature_value

        response = requests.post("https://securepay.tinkoff.ru/e2c/v2/RemoveCard", json=data)
        return response.json()

    # Работа с выплатами
    def init_payout(self, order_id, card_id, amount, data=None):
        """
            Инициирует выплату.
            
            Parameters:
            - order_id (str): Уникальный номер заказа в системе Мерчанта.
            - card_id (str): Идентификатор карты пополнения, привязанной с помощью метода AddCard.
            - amount (int): Сумма в копейках.
            - data (dict, optional): Дополнительные параметры передаваемые в объект DATA.
        """
        request_data = {
            "TerminalKey": self.terminal_key,
            "OrderId": order_id,
            "CardId": card_id,
            "Amount": amount,
            "X509SerialNumber": self.x509_serial_number
        }

        # Если переданы дополнительные параметры, добавляем их в запрос
        if data:
            request_data["DATA"] = data

        digest_value, signature_value = self.generate_signature_and_digest(request_data)

        request_data['DigestValue'] = digest_value
        request_data['SignatureValue'] = signature_value

        response = requests.post("https://securepay.tinkoff.ru/e2c/v2/Init", json=request_data)
        return response.json()

    def confirm_payout(self, payment_id):
        """
            Производит пополнение карты.
            
            Parameters:
            - payment_id (str): Уникальный идентификатор транзакции в системе Тинькофф Кассы. 
        """
        request_data = {
            "TerminalKey": self.terminal_key,
            "PaymentId": payment_id,
            "X509SerialNumber": self.x509_serial_number
        }

        digest_value, signature_value = self.generate_signature_and_digest(request_data)

        request_data['DigestValue'] = digest_value
        request_data['SignatureValue'] = signature_value

        response = requests.post("https://securepay.tinkoff.ru/e2c/v2/Payment", json=request_data)
        return response.json()

    def get_payout_status(self, payment_id):
        """
            Возвращает текущий статус выплаты.
            
            Parameters:
            - payment_id (int): Идентификатор операции в системе Тинькофф Кассы.
        """
        request_data = {
            "TerminalKey": self.terminal_key,
            "PaymentId": payment_id,
            "X509SerialNumber": self.x509_serial_number
        }

        digest_value, signature_value = self.generate_signature_and_digest(request_data)

        request_data['DigestValue'] = digest_value
        request_data['SignatureValue'] = signature_value

        response = requests.post("https://securepay.tinkoff.ru/e2c/v2/GetState", json=request_data)
        return response.json()

