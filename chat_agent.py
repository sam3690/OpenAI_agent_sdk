# import asyncio
# import os
# from dotenv import load_dotenv
# from agents import Agent, Runner
# from openai import OpenAI

# # Load your OpenAI API key from .env
# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # A very simple agent
# class SimpleAgent(Agent):
#     async def on_message(self, message: str):
#         # Send the user message to OpenAI
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",   # Small + cheap model
#             messages=[{"role": "user", "content": message}]
#         )
#         return response.choices[0].message.content

# async def main():
#     # Create and run the agent
#     runner = Runner()
#     runner.add_agent(SimpleAgent(name="my-first-agent"))
    
#     print("🤖 Simple Agent ready! Type 'quit' to exit.\n")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["quit", "exit"]:
#             break
#         response = await runner.run(user_input)
#         print("Agent:", response, "\n")

# if __name__ == "__main__":
#     asyncio.run(main())

# from openai import OpenAI
# client = OpenAI()
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Create OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# print(os.getenv("OPENAI_API_KEY"))


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}]
)

# print(response.output_text)
print(response.choices[0].message.content)

