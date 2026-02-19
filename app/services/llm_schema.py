SYSTEM_PROMPT = """
You are a business data assistant. When the user asks for data, you MUST
call get_data immediately — never ask the user to clarify the source.

Infer the source from the user's intent:
- crm        → customers, leads, sales, pipeline, accounts, contacts
- support    → tickets, complaints, issues, helpdesk, bugs, requests
- analytics  → metrics, reports, dashboards, KPIs, trends, statistics, performance

Keep responses concise and optimized for voice.
"""

TOOLS = [
    {
        "function_declarations": [
            {
                "name": "get_data",
                "description": (
                    "Retrieve business data. Infer the source from context:\n"
                    "- 'crm': customer records, leads, sales, pipeline\n"
                    "- 'support': tickets, complaints, helpdesk issues\n"
                    "- 'analytics': metrics, KPIs, trends, dashboards, statistics"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "enum": ["crm", "support", "analytics"],
                            "description": (
                                "Data source to query. "
                                "Use 'analytics' for metrics/trends/reports, "
                                "'crm' for customer/sales data, "
                                "'support' for tickets/issues."
                            ),
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Max records to return (default 10, max 100)",
                        },
                    },
                    "required": ["source"],
                },
            }
        ]
    }
]