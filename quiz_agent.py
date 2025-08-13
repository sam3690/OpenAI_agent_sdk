import os 
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Agent, Runner, handoff, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI

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

class UserInfo(BaseModel):
    name: str
    favourite_subject: str
    quiz: str

quiz_agent = Agent(
    name="QuizAgent",
    instructions="""You are a quiz generator.
        You will receive the student's name and favorite subject.
        Create a fun 3 question quiz based on their favorite subject.
        Return the complete information including name, subject, and quiz.""",
    model=model,
    output_type=UserInfo
)

# Simple approach: just use one agent that collects info and creates quiz
main_agent = Agent(
    name="StudentHelper",
    instructions="""You are a friendly teaching assistant.
        Extract the student's name and favorite subject from their message.
        Then immediately hand off to QuizAgent with the extracted information.
        Pass the name and subject to QuizAgent so it can generate a quiz.""",
    model=model,
    # handoffs={quiz_agent.name: handoff(quiz_agent)},
    handoffs=[quiz_agent]
    # output_type=UserInfo
)
result = Runner.run_sync(
    main_agent,
    "Hello! I am Ali and my favourite subject is Mathematics.",
)

print("\nExtracted Information:")
print(f"Name: {result.final_output.name}")
print(f"Favourite Subject: {result.final_output.favourite_subject}")

print("\nGenerated Quiz:")
print(result.final_output.quiz)