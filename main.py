from api.safe_deal import SafeDealAPI
from api.user import CustomerManager


def create_customer_manager(terminal_key: str, x509_serial_number: str):
    return CustomerManager(terminal_key, x509_serial_number)


def create_deal_manager(terminal_key: str, private_key_path: str, password: str):
    return SafeDealAPI(terminal_key, private_key_path, password)
