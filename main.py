class TinkoffPayouts:
    def __init__(self, terminal_key, x509_serial_number, private_key_path="private.key", base_url="https://securepay.tinkoff.ru"):
        self.terminal_key = terminal_key
        self.x509_serial_number = x509_serial_number
        self.private_key_path = private_key_path
        self.base_url = base_url

    def _generate_signature(self, data):
        filtered_data = {k: v for k, v in data.items() if k not in ["DigestValue", "SignatureValue", "X509SerialNumber"]}
        concatenated_values = ''.join([str(filtered_data[key]) for key in sorted(filtered_data.keys())])
        sha256_hash = SHA256.new(concatenated_values.encode())
        with open(self.private_key_path, "rb") as key_file:
            private_key = RSA.import_key(key_file.read())
        signature = pkcs1_15.new(private_key).sign(sha256_hash)
        digest_value = base64.b64encode(sha256_hash.digest()).decode()
        signature_value = base64.b64encode(signature).decode()
        data["DigestValue"] = digest_value
        data["SignatureValue"] = signature_value
        return data

    def _make_request(self, endpoint, data):
        url = self.base_url + endpoint
        signed_data = self._generate_signature(data)
        response = requests.post(url, json=signed_data)
        return response.json()

    def add_customer(self, customer_key, email=None, phone=None):
        """Добавление нового клиента"""
        data = {
            "TerminalKey": self.terminal_key,
            "CustomerKey": customer_key,
            "X509SerialNumber": self.x509_serial_number
        }
        if email:
            data["Email"] = email
        if phone:
            data["Phone"] = phone
        return self._make_request("/e2c/v2/AddCustomer", data)

    def add_card(self, customer_key, check_type="NO"):
        """Добавление новой карты"""
        data = {
            "TerminalKey": self.terminal_key,
            "CustomerKey": customer_key,
            "CheckType": check_type,
            "X509SerialNumber": self.x509_serial_number
        }
        return self._make_request("/e2c/v2/AddCard", data)

    def get_card_list(self, customer_key):
        """Получение списка карт клиента"""
        data = {
            "TerminalKey": self.terminal_key,
            "CustomerKey": customer_key,
            "X509SerialNumber": self.x509_serial_number
        }
        return self._make_request("/e2c/v2/GetCardList", data)

    def payment(self, payment_id):
        """Осуществление платежа"""
        data = {
            "TerminalKey": self.terminal_key,
            "PaymentId": payment_id,
            "X509SerialNumber": self.x509_serial_number
        }
        return self._make_request("/e2c/v2/Payment", data)

    def get_state(self, payment_id):
        """Получение статуса платежа"""
        data = {
            "TerminalKey": self.terminal_key,
            "PaymentId": payment_id,
            "X509SerialNumber": self.x509_serial_number
        }
        return self._make_request("/e2c/v2/GetState", data)
