from cryptocustom_tool import WebsearchTools
import os 
from dotenv import load_dotenv
# from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, SQLiteSession
from agents.run import RunConfig
from openai import AsyncOpenAI
load_dotenv()
class WeatherAgent():
    def __init__(self):
        self.API_KEY= os.getenv('OPENROUTER_API_KEY')
        self.session = SQLiteSession("history_agent.db")
        if not self.API_KEY:
            raise ValueError("api key is missing")
    
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key= self.API_KEY
    )
        
        self.model =OpenAIChatCompletionsModel(
         model = "openai/gpt-oss-20b:free",
         openai_client= self.client
        )

        
        self.config = RunConfig(
            model=self.model,
            model_provider=self.client,
            tracing_disabled=True
        )

        self.agent = Agent(
            name="Weather",
            instructions="Answer only weather question "
          ,
            model=self.model,
            tools=[WebsearchTools] 
        )


    def run(self):
        """Run the agent with a given message"""
        print("""
              this is assistant
            """)
        while True:
            message = input("Enter a message for the agent: ")
            if message.lower() == "exit":
                print("\nExiting agent session...\n")
                break

            try:
                results = Runner.run_sync(
                    self.agent,
                    message, 
                    run_config=self.config,
                    session=self.session
                )
                print("\nCalling Agent\n")
                print(results.final_output)
                # return results.final_output
            except Exception as e:
                print(f"Error running agent: {e}")
                return None



agent=  WeatherAgent()
agent.run()