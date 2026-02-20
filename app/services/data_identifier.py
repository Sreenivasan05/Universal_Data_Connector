from typing import Any
import logging


logger = logging.getLogger(__name__)


class DataIdentifier:

    def identify(self, data:list[dict[str, Any]]) -> str:
        if not data:
            return "empty"
        
        sample = data[0]
        keys = set(sample.keys())

        if "metric" in keys and "values" in keys:
            return "time_series"
        
        if "ticket_id" in keys:
            return "tabular_support"
        
        if "customer_id" in keys and "email" in keys:
            return "tabular_crm"
        
        logger.warning("Could not identify data type from keys: %s",keys)
        return "unknown"