import os 
from dotenv import load_dotenv
# from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, SQLiteSession
from agents.run import RunConfig
from openai import AsyncOpenAI

class HistoryAgent:
    """An Arithmatic Agent that maintains conversation history using SQLite."""
    def __init__(self):
        load_dotenv()

        self.session = SQLiteSession("history_agent.db")

        self.API_KEY = os.getenv("OPENROUTER_API_KEY")
        if not self.API_KEY:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")

        set_tracing_disabled(disabled=True)

        # Initialize the OpenAI client
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.API_KEY
        )

        # Initialize the model
        self.model = OpenAIChatCompletionsModel(
            model='openai/gpt-oss-20b',
            openai_client=self.client
        )

        # Configure the run settings
        self.config = RunConfig(
            model=self.model,
            model_provider=self.client,
            tracing_disabled=True
        )
        
        # Initialize the agent
        self.agent = Agent(
            name="math agent",
            instructions="Answer any question user asks related to arithimatics only.",
            model=self.model
        )

    

    def run(self):
        """Run the agent with a given message"""
        print("""
                This agent can only answer arithimatics related questions.
                Starting agent session. Type 'exit' to quit.
              """)

        while True:

            message = input("\nEnter a message for the agent: ")
            
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