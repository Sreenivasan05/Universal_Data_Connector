from app.connectors.base import BaseConnector
from app.utils import load_json

class AnalyticsConnector(BaseConnector):

    def fetch(self):
        return load_json("analytics.json")

            
    