from pymongo import MongoClient


class HygieiaRepo:
    def __init__(self, host, port, db):
        uri = 'mongodb://{host}:{port}'.format(
            host=host,
            port=port,
        )
        self._client = client = MongoClient(uri)
        self._db = client[db]
