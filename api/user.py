import requests
import logging

from utils.security import TransactionSecurity
from config.settings import API_BASE_URL


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CustomerManager:
    BASE_URL = API_BASE_URL

    def __init__(self, terminal_key: str, x509_serial_number: str):
        if not terminal_key or not x509_serial_number:
            logging.error("Initialization parameters cannot be None or empty.")
            raise ValueError("TerminalKey and X509SerialNumber are required.")

        self.session = requests.Session()
        self.terminal_key = terminal_key
        self.x509_serial_number = x509_serial_number

    def _prepare_data(self, **kwargs):
        data = {key: value for key, value in kwargs.items() if value is not None}
        data.update(
            {
                "TerminalKey": self.terminal_key,
                "X509SerialNumber": self.x509_serial_number,
            }
        )
        try:
            digest_value, signature_value = (
                TransactionSecurity.generate_signature_and_digest(data)
            )
            data.update(
                {
                    "DigestValue": digest_value,
                    "SignatureValue": signature_value,
                }
            )
        except Exception as e:
            logging.error(f"Error generating signature: {e}")
            raise
        return data

    def _send_request(self, endpoint, data):
        try:
            response = self.session.post(f"{self.BASE_URL}/{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Network-related error occurred: {e}")
            raise
        except Exception as err:
            logging.error(f"An unexpected error occurred: {err}")
            raise

    def add_customer(self, customer_key, email: str = None, phone: int = None):
        data = self._prepare_data(CustomerKey=customer_key, Email=email, Phone=phone)
        return self._send_request("AddCustomer", data)

    def get_customer(self, customer_key):
        data = self._prepare_data(CustomerKey=customer_key)
        return self._send_request("GetCustomer", data)

    def remove_customer(self, customer_key):
        data = self._prepare_data(CustomerKey=customer_key)
        return self._send_request("RemoveCustomer", data)

    def get_card_list(self, customer_key):
        data = self._prepare_data(CustomerKey=customer_key)
        return self._send_request("GetCardList", data)

    def add_card(self, customer_key, check_type: str = None):
        data = self._prepare_data(CustomerKey=customer_key, CheckType=check_type)
        return self._send_request("AddCard", data)

    def check_3ds_version(self, payment_id, card_data, token):
        if not all([payment_id, card_data, token]):
            logging.error("PaymentId, CardData, and Token cannot be None.")
            raise ValueError("All parameters are required for 3DS check.")
        data = {
            "TerminalKey": self.terminal_key,
            "PaymentId": payment_id,
            "CardData": card_data,
            "Token": token,
            "X509SerialNumber": self.x509_serial_number,
        }
        return self._send_request("Check3dsVersion", data)

    def remove_card(self, card_id, customer_key):
        data = self._prepare_data(CardId=card_id, CustomerKey=customer_key)
        return self._send_request("RemoveCard", data)
