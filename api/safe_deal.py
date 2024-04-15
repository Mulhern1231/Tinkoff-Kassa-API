import logging

import requests

from config.settings import API_BASE_URL
from utils.security import TransactionSecurity

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SafeDealAPI:
    def __init__(self, terminal_key: str, private_key_path: str, password: str):
        self.terminal_key = terminal_key
        self.BASE_URL = API_BASE_URL

        self.security = TransactionSecurity(
            private_key_path=private_key_path, terminal_password=password
        )

    def _prepare_request(self, method, data):
        try:
            token = self.security.generate_token(data)
            data["Token"] = token
            return method, data
        except Exception as e:
            logging.error(f"Error in preparing request for {method}: {e}")
            raise

    def _send_request(self, endpoint, data):
        logging.debug(f"Sending request to {endpoint} with data: {data}")
        try:
            response = requests.post(f"{self.BASE_URL}/{endpoint}", json=data)
            response.raise_for_status()
            logging.info(f"Request to {endpoint} successful.")
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

    def init_deal(self, order_id, amount):
        data = {"TerminalKey": self.terminal_key, "OrderId": order_id, "Amount": amount}
        endpont, payload = self._prepare_request("Init", data)
        return self._send_request(endpont, payload)

    def confirm_deal(self, payment_id):
        data = {"TerminalKey": self.terminal_key, "PaymentId": payment_id}
        endpont, payload = self._prepare_request("Confirm", data)
        return self._send_request(endpont, payload)

    def cancel_deal(self, payment_id):
        data = {"TerminalKey": self.terminal_key, "PaymentId": payment_id}
        endpont, payload = self._prepare_request("Cancel", data)
        return self._send_request(endpont, payload)

    def payment(self, payment_id, card_id, amount):
        data = {
            "TerminalKey": self.terminal_key,
            "PaymentId": payment_id,
            "CardId": card_id,
            "Amount": amount,
        }
        endpont, payload = self._prepare_request("Payment", data)
        return self._send_request(endpont, payload)
