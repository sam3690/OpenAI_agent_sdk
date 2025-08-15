import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import OpenAI



load_dotenv()


API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
   raise ValueError("Missing OPENROUTER_API_KEY environment variable")


client = OpenAI(
   base_url='https://openrouter.ai/api/v1',
   api_key= API_KEY
)

set_tracing_disabled(disabled=True)

model = OpenAIChatCompletionsModel(
  model="openai/gpt-4o-mini",
    openai_client=client
)

context= """you are helpful assistant professinal in programing and you give a simple idea"""

agent = Agent(
    name= "HelloAgent",
    instructions= "You are a helpful assistant.",
    model=model
)

def ask_with_context(user_message):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": user_message}
        ]
    )

   


    return response.choices[0].message.content

print(ask_with_context("give me an idea wht technology use for making website"))


