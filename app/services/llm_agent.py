from app.config import settings
import google.generativeai as genai
from app.services.data_service import DataService
from app.services.llm_schema import tools, SYSTEM_PROMPT

genai.configure(api_key=settings.API_KEY)



class LLMSERVICE:
    def __init__(self, data_service: DataService) -> None:
        self.data_service = data_service
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT,
            tools=tools
        )

    def _execute_tool(self, function_name:str, args:dict):
        if function_name == "get_data":
            source = args.get("source")
            limit = int(args.get("limit", 10))
            result = self.data_service.get_data(source=source, limit=limit)
            return result.model_dump()
        
    def run_agent(self, user_query):
        chat = self.model.start_chat()

        response = chat.send_message(user_query)

        function_call_part = None
        for part in response.candidates[0].content.parts:
            if part.function_call.name:
                function_call_part = part.function_call
                break

        
        if function_call_part is None:
            return response.text
        
        fn_name = function_call_part.name
        fn_args = dict(function_call_part.args)

        return (fn_name, fn_args)
