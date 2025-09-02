# import os
# from dotenv import load_dotenv
# from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
# from openai import AsyncOpenAI
# from openai.types.chat import ChatCompletion

# load_dotenv()

# API_KEY = os.getenv("OPENROUTER_API_KEY")
# if not API_KEY:
#     raise ValueError("Missing OPENROUTER_API_KEY environment variable")

# client = AsyncOpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=API_KEY
# )

# model = OpenAIChatCompletionsModel(
#     model="openai/gpt-4o-mini",
#     openai_client=client
# )

# set_tracing_disabled(disabled=True)

# agent = Agent(
#     name= "HelloAgent",
#     instructions= "You are a helpful assistant.",
#     model=model
# )

# # print(os.getenv("OPENROUTER_API_KEY"))

#     # model="openai/gpt-4o-mini",


# # context
# result = Runner.run_sync(agent, [
#         {"role": "user", "content": "I am feeling cold"},
#         {"role": "user", "content": "can you get the weather forcast?"}
#     ],)

# print(result.final_output)

import os
from history_agent import HistoryAgent
from tool_agent import TradingAgent


# agent = HistoryAgent()
agent = TradingAgent()

def main():
    agent.run()

if __name__ == "__main__":
    main()
