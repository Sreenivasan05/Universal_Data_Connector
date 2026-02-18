from app.connectors.crm_connector import CRMConnector
from app.connectors.support_connector import SupportConnector
from app.connectors.analytics_connector import AnalyticsConnector
from app.services.data_identifier import identify_data_type
from app.models.common import DataResponse, Metadata
from datetime import datetime, timezone

from app.services.business_rules import apply_voice_limits
from app.services.voice_optimizer import summarize_if_large


class DataService:
    def __init__(self):
        self.connector_map = {
            "crm": CRMConnector(),
            "support": SupportConnector(),
            "analytics": AnalyticsConnector(),
        }

    def get_data(self, source:str, limit:int = 10):
        connector = self.connector_map.get(source)
        if not connector:
             return {"data": [], "metadata": {"total_results": 0, "returned_results": 0, "data_freshness": "unknown"}}
        
        raw_data = connector.fetch()
        total = len(raw_data)

        filtered = apply_voice_limits(raw_data)
        optimized = summarize_if_large(filtered)

        data_type = identify_data_type(raw_data)

        metadata = Metadata(
            total_results=total,
            returned_results=len(optimized),
            data_freshness=f"Data as of {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC",
            data_type=data_type,
            source=source,
            context = f"Showing {len(optimized)} of {total} results"
        )

        return DataResponse(data=optimized, metadata=metadata)
