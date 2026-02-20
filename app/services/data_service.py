from app.connectors.crm_connector import CRMConnector
from app.connectors.support_connector import SupportConnector
from app.connectors.analytics_connector import AnalyticsConnector
from app.models.common import DataResponse, Metadata
from datetime import datetime, timezone

from app.services.data_identifier import DataIdentifier
from app.services.business_rules import BusinessRulesEngine
from app.services.voice_optimizer import VoiceOptimizer

import logging

logger = logging.getLogger(__name__)




class DataService:
    def __init__(self):
        self.connector_map = {
            "crm": CRMConnector(),
            "support": SupportConnector(),
            "analytics": AnalyticsConnector(),
        }

        self.rules = BusinessRulesEngine()
        self.identifier = DataIdentifier()
        self.voice = VoiceOptimizer()

    def get_data(self, source:str, limit:int = 10, aggregate:bool = False):
        connector = self.connector_map.get(source)
        if not connector:
             return {"data": [], "metadata": {"total_results": 0, "returned_results": 0, "data_freshness": "unknown"}}
        
        raw_data = connector.fetch()
        total = len(raw_data)
        logger.debug("Connector returned %d raw records", total)

        data_type = self.identifier.identify(raw_data)
        logger.debug("Detected data_type='%s'", data_type)
        filered = self.rules.apply(raw_data, limit=limit, data_type=data_type)
        
        optimized = self.voice.optimize(filered, data_type=data_type, aggregate=aggregate)


        metadata = Metadata(
            total_results=total,
            returned_results=len(optimized),
            data_freshness=f"Data as of {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC",
            data_type=data_type,
            source=source,
            context = f"Showing {len(optimized)} of {total} results"
        )

        logger.info(
            "Returning %d/%d records from source='%s'",
            len(optimized),
            total,
            source,
        )

        return DataResponse(data=optimized, metadata=metadata)
