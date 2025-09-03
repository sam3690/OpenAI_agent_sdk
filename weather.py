import os 
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Agent, Runner, handoff, OpenAIChatCompletionsModel, set_tracing_disabled,WebSearchTool
from openai import AsyncOpenAI
import asyncio

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY environment variable")

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)
set_tracing_disabled(disabled=True)

model = OpenAIChatCompletionsModel(
    model="openai/gpt-4o-mini",
    openai_client=client
)


WeatherAgent = Agent(
    name = "weather agent",
    instructions = "You are a weather assistant who provides current and upcoming weather information.",
    tools=[WebSearchTool()],
 
)
travel_agent = Agent(
    name="Travel Agent",
    instructions="You are a travel assistant who helps with flights, hotels, and trip planning.",
    tools=[WebSearchTool()],
    handoffs=[WeatherAgent],   # yahan Weather Agent ko handoff ki permission di


)


async def getresult():
    try:
        prompt = "Plan a trip to San Francisco and also tell me what the weather will be like tomorrow."
        reasult =await Runner.run(travel_agent,"Plan a trip to Lahore and tell me the weather.")
        print(reasult)
    except Exception as e:
        print("error:", e)

asyncio.run(getresult())