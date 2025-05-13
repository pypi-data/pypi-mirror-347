import requests
from datetime import timedelta


class ConnectionSettings(object):
    DEFAULT_HOST: str = "https://elm.evoleap.com"
    DEFAULT_REQUEST_TIMEOUT: timedelta = timedelta(seconds=60)
    DEFAULT_SSL_VERIFY: bool = True

    __handler: requests
    __host: str = DEFAULT_HOST
    __request_timeout: timedelta = DEFAULT_REQUEST_TIMEOUT
    __ssl_verify: bool = DEFAULT_SSL_VERIFY

    @classmethod
    def Host(cls) -> str:
        return cls.__host

    @classmethod
    def SetHost(cls, value):
        cls.__host = value

    @classmethod
    def RequestTimeout(cls) -> timedelta:
        return cls.__request_timeout

    @classmethod
    def SetRequestTimeout(cls, timeout: timedelta):
        cls.__request_timeout = timeout

    @classmethod
    def SSLVerify(cls) -> bool:
        return cls.__ssl_verify
    
    @classmethod
    def SetSSLVerify(cls, value: bool):
        cls.__ssl_verify = value