from app.config import settings
import google.generativeai as genai
from app.services.data_service import DataService
from app.services.llm_schema import TOOLS, SYSTEM_PROMPT
from google.generativeai.types import content_types
from app.utils.retry import with_retry
import logging

genai.configure(api_key=settings.GEMINI_API_KEY)

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, data_service: DataService) -> None:
        self.data_service = data_service
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT,
            tools=TOOLS
        )

    def _execute_tool(self, function_name:str, args:dict):
        if function_name == "get_data":
            source = args.get("source")
            limit = int(args.get("limit", 10))
            aggregate = bool(args.get("aggregate",False))

            result = self.data_service.get_data(source=source, limit=limit, aggregate=aggregate)
            return result.model_dump()
    
    @with_retry(max_attempt=3, base_delay=2.0)
    def _send(self, chat, message):
        return chat.send_message(message)
        
    def run_agent(self, user_query):
        logger.info("Agent query receieved: %s", user_query)
        chat = self.model.start_chat()

        response = self._send(chat, user_query)


        function_call_part = None
        for part in response.candidates[0].content.parts:
            if part.function_call.name:
                function_call_part = part.function_call
                break

        if function_call_part is None:
            return response.text
        
        fn_name = function_call_part.name
        fn_args = dict(function_call_part.args)
        logger.info("Tool call: %s(%s)", fn_name, fn_args)

        tool_result = self._execute_tool(fn_name, fn_args)
        print("tool result", tool_result)
        tool_respone_part = content_types.to_part(
            {"function_response": {"name": fn_name, "response": tool_result}}
        )

        final_response = self._send(chat, tool_respone_part)
        print("final_response", final_response)
        return final_response.text
    

 
