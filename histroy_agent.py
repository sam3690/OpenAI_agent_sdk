import os 
from dotenv import load_dotenv
# from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, SQLiteSession
from agents.run import RunConfig
from openai import AsyncOpenAI

class HistoryAgent:
    def __init__(self):
        load_dotenv()

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
            model='deepseek/deepseek-r1-0528',
            openai_client=self.client
        )

        self.config = RunConfig(
            model=self.model,
            model_provider=self.client,
            tracing_disabled=True
        )

        self.agent = Agent(
            name="math agent",
            instructions="Answer any question user asks related to arithimatics only.",
            model=self.model
        )

    

    def run(self):
        """Run the agent with a given message"""
        while True:
            message = input("Enter a message for the agent: ")
            if message.lower() == "exit":
                print("Exiting agent session...")
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