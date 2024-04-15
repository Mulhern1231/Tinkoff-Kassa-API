import base64
import hashlib

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


class TransactionSecurity:
    def __init__(self, private_key_path, terminal_password):
        self.private_key_path = private_key_path
        self.terminal_password = terminal_password

    def generate_signature_and_digest(self, data: dict):
        keys_to_remove = ["DigestValue", "SignatureValue", "X509SerialNumber"]
        filtered_data = {
            key: value for key, value in data.items() if key not in keys_to_remove
        }

        concatenated_string = "".join(
            [value for key, value in sorted(filtered_data.items(), key=lambda x: x[0])]
        )

        hash_object = hashlib.sha256(concatenated_string.encode())
        digest_value = base64.b64encode(hash_object.digest()).decode()

        with open(self.private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(), password=None
            )

        signature = private_key.sign(
            hash_object.digest(), padding.PKCS1v15(), hashes.SHA256()
        )
        signature_value = base64.b64encode(signature).decode()

        return digest_value, signature_value

    def generate_token(self, data: dict):
        data_with_password = {**data, "Password": self.terminal_password}
        sorted_data = sorted(data_with_password.items(), key=lambda x: x[0])
        concatenated_values = "".join([value for key, value in sorted_data])

        hash_object = hashlib.sha256(concatenated_values.encode())
        token = hash_object.hexdigest()

        return token
