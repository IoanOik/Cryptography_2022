from space_comm import transmitter
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad


class Encryptor:
    def __init__(self, name: str) -> None:
        self.key_pair_generation(name)

    def key_pair_generation(self, name: str) -> None:
        key_pair = RSA.generate(2048)
        self.private_key = RSA.import_key(key_pair.export_key())
        self.public_key = RSA.import_key(key_pair.public_key().export_key())
        file = open(name + ".txt", "wb")
        file.write(key_pair.public_key().export_key())
        file.close()

    def encrypt_and_sign(self, plainText: list, id: int) -> bytes:
        # session key asymmetric encryption
        receiver_file = str(id) + ".txt"
        receiver_public_key = RSA.import_key(open(receiver_file, "rb").read())
        session_key = get_random_bytes(AES.block_size)
        cipher_rsa = PKCS1_OAEP.new(key=receiver_public_key)
        encrypted_session_key = cipher_rsa.encrypt(message=session_key)
        # data symmetric encryption
        iv_vector = get_random_bytes(AES.block_size)
        padded_text = pad(data_to_pad=bytes(plainText), block_size=AES.block_size)
        self.cipher = AES.new(key=session_key, mode=AES.MODE_CBC, iv=iv_vector)
        encrypted_data = iv_vector + self.cipher.encrypt(padded_text)
        # message authentication
        hash_msg = SHA256.new(encrypted_session_key + encrypted_data)
        signature = pkcs1_15.new(self.private_key).sign(hash_msg)

        return encrypted_session_key + encrypted_data + signature

    def verify_signature(self, cipherText: bytes, sender_public_key: bytes) -> bool:
        hash_msg = SHA256.new(cipherText[:288])
        rsa_key = RSA.import_key(sender_public_key)
        try:
            pkcs1_15.new(rsa_key).verify(hash_msg, cipherText[288:])
        except (ValueError, TypeError):
            return False
        return True

    def _decrypt_(self, cipherText: bytes) -> bytes | None:
        encrypted_sym_key = cipherText[:256]
        cipher_rsa = PKCS1_OAEP.new(key=self.private_key)
        try:
            symmetric_key = cipher_rsa.decrypt(encrypted_sym_key)
        except (ValueError):
            # Message is not for this spacecraft, so it cannot get properly decrypted by it
            return None
        iv_vector = cipherText[256:272]
        cipher = AES.new(key=symmetric_key, mode=AES.MODE_CBC, iv=iv_vector)
        plainText = cipher.decrypt(cipherText[272:288])
        return unpad(padded_data=plainText, block_size=AES.block_size)


## handle outgoing message
def prepare_msg(msg_type, id, dir, dis):
    msg = [msg_type, id, dir, dis]
    encryptor = Encryptor("base_station")
    buffer = encryptor.encrypt_and_sign(plainText=msg, id=id)
    return buffer
    # return bytes([msg_type, id, dir, dis])


if __name__ == "__main__":

    t = transmitter("base station")

    id = int(input("Give id: "))
    dir = int(input("Give direction [1-4] 1-U, 2-R, 3-D, 4-L: "))
    dis = int(input("Give dinstance [1-4]: "))

    msg_type = 1  # command
    pos_x = 10
    pos_y = 10
    b = prepare_msg(msg_type, id, dir, dis)
    t.transmit(b)
