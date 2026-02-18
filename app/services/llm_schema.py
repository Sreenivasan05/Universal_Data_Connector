SYSTEM_PROMPT = """
You are a business data assistant.
When user asks for CRM, support, or analytics data,
you MUST call the get_data function.
Keep responses concise and optimized for voice.
"""

tools = [
    {
        "function_declarations": [
            {
                "name": "get_data",
                "description": "Retrieve business data from a specific source",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "enum": ["crm", "support", "analytics"]
                        },
                        "limit": {
                            "type": "integer"
                        }
                    },
                    "required": ["source"]
                }
            }
        ]
    }
]