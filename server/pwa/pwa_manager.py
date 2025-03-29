import os
import hashlib
import time
import base64
import ecdsa
from jose import jws


class PwaManager:

    @staticmethod
    def _to_base64(key):
        key = base64.urlsafe_b64encode(key).strip(b"=")
        return key

    @staticmethod
    def _make_jwt(header, claims, key):
        vk = key.get_verifying_key()
        jwt = jws.sign(
            claims,
            key,
            algorithm=header.get("alg", "ES256")).strip("=")
        # The "0x04" octet indicates that the key is in the
        # uncompressed form. This form is required by the
        # server and DOM API. Other crypto libraries
        # may prepend this prefix automatically.
        raw_public_key = b"\x04" + vk.to_string()
        public_key = PwaManager._to_base64(raw_public_key)
        return jwt, public_key

    @staticmethod
    def gen_keys():
        rewrite_pub =False
        # Checks if the file with the key exists.
        key_file = "keys/vapid_private_key.pem"
        key_dir = os.path.dirname(key_file)

        # Creates the directory if it does not exist.
        if not os.path.exists(key_dir):
            os.makedirs(key_dir)

        if os.path.exists(key_file):
            # Loads the key from the file.
            with open(key_file, "rb") as f:
                file_contents = f.read()
            my_key = ecdsa.SigningKey.from_pem(file_contents)
        else:
            rewrite_pub = True
            # Generates a new key if the file is not found.
            my_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
            # Saves the key to a file.
            with open(key_file, "wb") as f:
                f.write(my_key.to_pem())

        # Standard header for all VAPID objects.
        header = {"typ": "JWT", "alg": "ES256"}

        # Custom claims.
        claims = {
            "aud": "https://updates.push.services.mozilla.com",
            "exp": int(time.time()) + 86400,
            "sub": "mailto:" + PwaManager.get_claim_email(),
        }

        # Creates a JWT and retrieves the public key.
        (jwt, public_key) = PwaManager._make_jwt(header, claims, my_key)

        if isinstance(public_key, bytes):
            public_key = public_key.decode()

        if public_key.startswith("b'"):
            public_key = public_key[2:-1]

        pk = PwaManager._to_base64(my_key.to_string())

        if isinstance(pk, bytes):
            pk = pk.decode()

        if pk.startswith("b'"):
            pk = pk[2:-1]

        public_key_file = "keys/vapid_private_key.pub"
        if rewrite_pub or not os.path.exists(public_key_file):
            with open(public_key_file, "wb") as f:
                f.write(PwaManager.get_public_key().encode("utf-8"))

        return public_key, pk

    @staticmethod
    def get_public_key():
        public, private = PwaManager.gen_keys()
        return public

    @staticmethod
    def get_private_key():
        public, private = PwaManager.gen_keys()
        return private


    @staticmethod
    def get_endpoint_hash(endpoint):
        endpoint = str(endpoint)
        m = hashlib.sha256()
        m.update(endpoint.encode('utf-8'))
        return m.hexdigest()


    @staticmethod
    def get_claim_email():
        return os.environ.get('CLAIMS_EMAIL')