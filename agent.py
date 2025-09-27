import os
from dotenv import load_dotenv
from agents import Agent, Runner, RunContextWrapper, function_tool, trace, WebSearchTool, output_guardrail, GuardrailFunctionOutput, TResponseInputItem
from openai.types.responses import ResponseTextDeltaEvent
from dataclasses import dataclass, asdict
from WebSearchTool import custom_web_search
from pydantic import BaseModel

import asyncio

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# @dataclass
class UserInput(BaseModel):
    name: str
    

@function_tool
def greeting_agent(ctx: RunContextWrapper[UserInput]) -> str:
    name = ctx.get("name")
    return f"Hello, {name}! How can I assist you today?"

agent = Agent(
    name="WebSearchAgent",
    model="gpt-4o-mini",
    instructions=(
        "You are a helpful assistant. When context provides `name`, greet the user"
        " once using the `greeting_agent` tool before answering their first"
        " question. Do not ask for their name again if it is already in context."
        " Strictly respond in English."
        " Don't respond to harmful or illegal queries."
        " After greeting, answer their queries, using web search when helpful."
    ),
    tools=[WebSearchTool(), greeting_agent]
)


with trace("agent.log"):
    async def run_agent():
        runner = Runner()
        print("Starting the agent...")
        user_name = input("Please provide your name first: ")

        print("To exit the agent, type 'exit' or 'quit'.")
        if user_name.strip():
            print("\nAgent greeting:\n")
            print(f"Hello, {user_name}! How can I assist you today?")
        user_input = input("Enter your query to the agent: ")
        greeted = False

        while user_input.lower() not in ['exit', 'quit']:
            prompt = user_input
            if not greeted:
                prompt = (
                    "Please greet the user named in context once using the"
                    " `greeting_agent` tool, then answer this question: "
                    + user_input
                )

            response = runner.run_streamed(
                agent,
                prompt,
                context={"name": user_name},
            )
            async for event in response:
                    print(event.text, event.data, end='', flush=True)
                    print("\n")
            print("Agent response:")
            # async for chunk in response:
            #     if isinstance(chunk, ResponseTextDeltaEvent):
            #         print(chunk.text, end='', flush=True)
            print("\n")
            print(response.final_output)
            greeted = True

            user_input = input("Enter your next query to the agent (or 'exit' to quit): ")
        




if __name__ == "__main__":
    asyncio.run(run_agent())