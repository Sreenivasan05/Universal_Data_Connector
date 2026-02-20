from typing import Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BusinessRulesEngine:
    """
    Applies source-aware business rules before voice optimization
    Rules: sort by recency, deduplicate, enforce limit
    """

    SORT_FIELDS = {
        "time_series" : "date",
        "tabular_crm" : "created_at",
        "tabular_support" : "created_at"
    }

    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def _get_priority_rank(self, data):
        priority = data.get("priority", "low")
        priority_rank = self.PRIORITY_ORDER.get(priority, 9)
        return priority_rank

    def apply(self, data:list[dict[str, Any]], limit:int=10, data_type:str = "unknown"):
        if not data:
            return []
        
        result = list(data) # dont want to mutate the original

        # For support tickets, sort by prioirity first, then recency
        if data_type == "tabular_support":
            result = sorted(
            result,
            key=lambda r: (
                self._get_priority_rank(r),
                -datetime.fromisoformat(r["created_at"]).timestamp(),
            ),
            )
        
        else:
            sort_field = self.SORT_FIELDS.get(data_type)
            if sort_field:
                result.sort(key=lambda r: str(r.get(sort_field, ""))
                            , reverse= True)
            
        if len(result) > limit:
            logger.debug(
                "Business rule: truncating %d records to limit=%d", len(result), limit
            )
            result = result[:limit]

        return result

