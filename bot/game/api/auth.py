import codecs
import json

from tools.cipher import salted_digest


DATA_ENCODING = "utf-8"
TRANSPORT_ENCODING = "base64"
DUMMY_ENCODING = "ascii"

DATA_DIGEST_SEPARATOR = "-"


def encode(data):
    dumped_data = json.dumps(data, separators=(',', ':'))
    encoded_dumped_data = dumped_data.encode(DATA_ENCODING)
    encoded_data = _transport_encode(encoded_dumped_data)
    digest = salted_digest(encoded_data)
    encoded_digest = _transport_encode(digest).decode(DUMMY_ENCODING)
    return encoded_data.decode(DUMMY_ENCODING) + DATA_DIGEST_SEPARATOR + encoded_digest


def decode(data):
    try:
        encoded_data, encoded_digest = data.split(DATA_DIGEST_SEPARATOR, 1)
        digest = _transport_decode(encoded_digest.encode(DUMMY_ENCODING))
        encoded_data = encoded_data.encode(DUMMY_ENCODING)
        calculated_digest = salted_digest(encoded_data)
        if calculated_digest == digest:
            encoded_dumped_data = _transport_decode(encoded_data)
            dumped_data = encoded_dumped_data.decode(DATA_ENCODING)
            return json.loads(dumped_data)
    except Exception:
        pass
    return {}


def _transport_encode(data):
    return codecs.encode(data, TRANSPORT_ENCODING).replace(b"\n", b"")


def _transport_decode(data):
    return codecs.decode(data, TRANSPORT_ENCODING)
