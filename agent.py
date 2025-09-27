import os
from dotenv import load_dotenv
from agents import Agent, Runner, RunContextWrapper, function_tool, trace
from openai.types.responses import ResponseTextDeltaEvent
from dataclasses import dataclass, asdict
from WebSearchTool import custom_web_search

import asyncio

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

@dataclass
class UserInfo():
    name: str = ""

@function_tool
def greet_user(ctx: RunContextWrapper[UserInfo]) -> str:
    """Greet the user by name."""
    user_info = ctx.context.get("User_Info", {})
    name = user_info.get('name', 'there') if isinstance(user_info, dict) else 'there'
    return f"Hello, {name}! How can I assist you today?"

agent = Agent(
    name="WebSearchAgent",
    instructions="""
        You are a helpful assistant that uses web search to answer user queries.
        When the user asks a question, use the web search tool to find relevant information.
        Provide concise and accurate answers based on the search results.
    """,
    tools=[custom_web_search, greet_user],
)
with trace("ResearchAgentRun"):
    async def run_agent():
        """Run the agent with a given message"""
        user_info = UserInfo()
        user_info.name = input("Please enter your name: ")
        # print(f"Hello, {user_info.name}! How can I assist you today?")

        # greet immediately
        # greeting = Runner.run_sync(
        #     agent,
        #     "greet the user", 
        #     context={"User_Info": user_info}
        # )
        # print("\nAgent Response:\n")
        # print(greeting.final_output)

        
        while True:
            message = input("Enter a message for the agent (or 'exit' to quit): ")
            if message.lower() == "exit":
                print("Exiting agent session...")
                break

            try:
                print("\nAgent Response:")
                
                # Run the agent with streaming
                result = await Runner.run(
                    agent,
                    message, 
                    context={"User_Info": asdict(user_info)}
                )
                
                print(result.messages[-1].content)
                
            except Exception as e:
                print(f"Error running agent: {e}")


if __name__ == "__main__":
    asyncio.run(run_agent())