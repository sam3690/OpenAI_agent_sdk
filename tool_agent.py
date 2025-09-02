import os 
from dotenv import load_dotenv
# from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, SQLiteSession
from agents.run import RunConfig
from openai import AsyncOpenAI
from WebSearchTool import custom_web_search 

class ToolAgent:
    def __init__(self):
        load_dotenv()
        # self.searchTool = WebSearchTool.custom_web_search()
        self.session = SQLiteSession("history_agent.db")

        self.API_KEY = os.getenv("OPENROUTER_API_KEY")
        if not self.API_KEY:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")

        set_tracing_disabled(disabled=True)

        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.API_KEY
        )
    
        self.model = OpenAIChatCompletionsModel(
            model='openai/gpt-oss-20b',
            openai_client=self.client
        )

        self.config = RunConfig(
            model=self.model,
            model_provider=self.client,
            tracing_disabled=True
        )

        self.agent = Agent(
            name="TradingAgent",
            instructions="Answer any question user asks related to Stock or Crypto only."
            "if the user asks prices or current market index you can use TradingAgent tool",
            model=self.model,
            tools=[custom_web_search] # dont add round brackets 
        )

    

    def run(self):
        """Run the agent with a given message"""
        print("""
                This is a Trading agent asks questions only related to Crypto and Stocks.
                Enter 'exit' to exit the agent.
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