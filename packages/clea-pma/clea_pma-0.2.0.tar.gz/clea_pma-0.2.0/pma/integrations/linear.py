from pma.utils.singleton import Singleton


class LinearClient(metaclass=Singleton):
    def __init__(self, api_key: str):
        self.api_key = api_key
