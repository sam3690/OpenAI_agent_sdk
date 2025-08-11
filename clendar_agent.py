import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from pydantic import BaseModel


load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY environment variable")


# Also set OPENAI_API_KEY so SDK doesn't complain
# os.environ["OPENAI_API_KEY"] = API_KEY

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)
set_tracing_disabled(disabled=True)

#Define output schema
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

model = OpenAIChatCompletionsModel(
    model="openai/gpt-4o-mini",
    openai_client=client
) 

agent = Agent(
    name="Calendar Extractor",
    instructions="Extract the calendar event details from the user's text",
    output_type=CalendarEvent,
    model=model
)

text = input("Enter the text to extract calendar event details: ")
result = Runner.run_sync(agent, text)
print("\n Structured Output Object:")
print(result.final_output)

print("\nAccess individual fields:")
print(f"Name: {result.final_output.name}")
print(f"Date: {result.final_output.date}")
print(f"Participants: {', '.join(result.final_output.participants)}")