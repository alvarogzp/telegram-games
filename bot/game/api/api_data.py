import codecs
import json

from tools.cipher import salted_digest


DATA_ENCODING = "utf-8"
TRANSPORT_ENCODING = "base64"
DUMMY_ENCODING = "ascii"

DATA_DIGEST_SEPARATOR = "-"


def encode(data):
    dumped_data = json.dumps(data)
    encoded_dumped_data = dumped_data.encode(DATA_ENCODING)
    encoded = _transport_encode(encoded_dumped_data)
    digest = salted_digest(encoded)
    return encoded.decode(DUMMY_ENCODING) + DATA_DIGEST_SEPARATOR + digest


def decode(data):
    try:
        encoded, digest = data.split(DATA_DIGEST_SEPARATOR, 1)
        encoded = encoded.encode(DUMMY_ENCODING)
        calculated_digest = salted_digest(encoded)
        if calculated_digest == digest:
            encoded_dumped_data = _transport_decode(encoded)
            dumped_data = encoded_dumped_data.decode(DATA_ENCODING)
            return json.loads(dumped_data)
    except Exception:
        pass
    return {}


def _transport_encode(data):
    return codecs.encode(data, TRANSPORT_ENCODING).replace(b"\n", b"")


def _transport_decode(data):
    return codecs.decode(data, TRANSPORT_ENCODING)
