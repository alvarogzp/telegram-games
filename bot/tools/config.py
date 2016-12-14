import json
import os

CONFIG_DIR = "config/"


class Codec:
    def __init__(self, decode_func=lambda x: x, encode_func=lambda x: x):
        self.decode = decode_func
        self.encode = encode_func


class Codecs:
    INT = Codec(int, str)
    STRING = Codec(str, str)
    LINE_LIST = Codec(lambda s: s.splitlines(), "\n".join)
    JSON = Codec(json.loads, json.dumps)


class Config:
    def __init__(self, name, default_value=None, strip=True, codec=Codecs.STRING, required=False):
        self.name = name
        self.path = self._get_path()
        self.default_value = default_value
        self.strip = strip
        self.codec = codec
        self.required = required
        if required:
            assert os.path.isfile(self.path), "Required config '" + self.name + "' not found on config dir"

    def read(self):
        if os.path.isfile(self.path):
            with open(self.path) as f:
                value = f.read()
            value = self.parse(value)
        elif self.required:
            raise Exception("Required config '" + self.name + "' not found on config dir")
        else:
            value = self.default_value
        return value

    def write(self, value):
        encoded_value = self.codec.encode(value)
        with open(self.path, "w") as f:
            f.write(encoded_value)

    def parse(self, value: str):
        if self.strip:
            value = value.strip()
        return self.codec.decode(value)

    def delete(self):
        if os.path.isfile(self.path):
            os.remove(self.path)

    def _get_path(self):
        return os.path.join(CONFIG_DIR, self.name)


class Key:
    AUTH_TOKEN = Config(
        name="auth_token",
        required=True
    )

    ADMIN_CHAT_ID = Config(
        name="admin_chat_id",
        required=True
    )

    LOG_CHAT_ID = Config(
        name="log_chat_id",
        required=True
    )

    SSL_API_KEY = Config(
        name="ssl_api_key",
        required=True
    )

    SSL_API_CERT = Config(
        name="ssl_api_cert",
        required=True
    )

    PROD_GAME_TAG = Config(
        name="prod_game_tag",
        required=True
    )

    @classmethod
    def get_by_name(cls, name) -> Config:
        return cls.__dict__.get(name)
