import logging

logger = logging.getLogger(__name__)

class VoiceOptimizer:

    def _aggregate(self, data: list[dict]) -> list[dict]:
        from collections import defaultdict

        grouped: dict[str, list] = defaultdict(list)
        dates:   dict[str, list] = defaultdict(list)

        for record in data:
            metric = record.get("metric", "unknown")
            value  = record.get("value")
            date   = record.get("date", "")
            if value is not None:
                grouped[metric].append(float(value))
            if date:
                dates[metric].append(date)

        summaries = []
        for metric, values in grouped.items():
            sorted_dates = sorted(dates[metric])

            mid   = len(values) // 2
            trend = "up" if (sum(values[mid:]) / max(len(values[mid:]), 1)) > \
                            (sum(values[:mid]) / max(mid, 1)) else "down"
            summaries.append({
                "metric":      metric,
                "average":     round(sum(values) / len(values), 1),
                "min":         min(values),
                "max":         max(values),
                "trend":       trend,
                "data_points": len(values),
                "period":      f"{sorted_dates[0]} to {sorted_dates[-1]}" if sorted_dates else "unknown",
            })
        logger.debug("Voice optimizer aggregated %d metrics", len(summaries))
        return summaries


    def optimize(self,data,data_type,aggregate):
        if not data:
            return []

        # Aggregate only when LLM explicitly requests it
        # AND data is actually aggregatable (time_series)
        if aggregate and data_type == "time_series":
            return self._aggregate(data)

        return data



