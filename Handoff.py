import os
from agents import Runner,OpenAIChatCompletionsModel,WebSearchTool,Agent,handoff,set_tracing_disabled, SQLiteSession
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents.run import RunConfig
load_dotenv()
class Handoff:
   def __init__(self):
      self.session = SQLiteSession("history-agent.db")
    

      self.API_KEY = os.getenv("OPENROUTER_API_KEY")
      if not self.API_KEY:
         print("API KEY IS OF")
      set_tracing_disabled(disabled=True)
      self.client = AsyncOpenAI(
           base_url="https://openrouter.ai/api/v1",
           api_key= self.API_KEY
      )
      self.model =OpenAIChatCompletionsModel(
         model = "openai/gpt-4o-mini",
         openai_client= self.client
      )
      self.config = RunConfig(
        model= self.model,
        tracing_disabled=True,
        model_provider=self.client

      )

      self.agent=Agent(
         name= 'Teacher',
         instructions= 'you are a maths teacher answer all maths question',
         model=self.model
      )

   def run(self):
    while True:
     try:
      message = input("Enter your text")
      if message.lower() == "exit":
        print("Exiting agent session...")
        break
      reasult = Runner.run_sync(
         self.agent,message,
         run_config= self.config,
        session=self.session)
      print(reasult.final_output)
     except Exception as e:
      print(e)


agent1= Handoff()
agent1.run()