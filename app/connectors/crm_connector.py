from .base import BaseConnector
from app.utils import load_json

class CRMConnector(BaseConnector):

    def fetch(self):
        return load_json("customers.json")