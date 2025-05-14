import os
from langgraph_sdk import get_sync_client
from dotenv import load_dotenv

load_dotenv()



class AuthenticationAgent:
    def __init__(self, instructions: str, pentest_uuid: str):
        self.auth_agent = get_sync_client(url=os.getenv("AUTH_AGENT_URL"))
        self.instructions = instructions
        self.pentest_uuid = pentest_uuid
    
    def authenticate(self):
        session_details = None
        response = self.auth_agent.runs.stream(
            thread_id=self.pentest_uuid,
            assistant_id="agent",
            input={
                "instructions": self.instructions
            },
            stream_mode="values"
        )
        for chunk in response:
            if chunk.data.get("session_details") != None:
                session_details = chunk.data.get("session_details")
                break
        return session_details

