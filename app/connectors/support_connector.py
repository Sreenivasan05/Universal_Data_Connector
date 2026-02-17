from app.connectors.base import BaseConnector
from app.utils import load_json

class SupportConnector(BaseConnector):

    def fetch(self):
        return load_json("support_tickets.json")