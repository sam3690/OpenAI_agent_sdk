import os 
from dotenv import load_dotenv
# from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, SQLiteSession
from agents.run import RunConfig
from openai import AsyncOpenAI, OpenAI

class TradingAgent:
    """An Trading Agent that searches web for stock or crypto market and maintains conversation history using SQLite."""
    def __init__(self):
        load_dotenv()

        self.session = SQLiteSession("history_agent.db")

        self.API_KEY = os.getenv("OPENROUTER_API_KEY")
        if not self.API_KEY:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")

        set_tracing_disabled(disabled=True)

        # Initialize the OpenAI client
        self.client = AsyncOpenAI(
            api_key=self.API_KEY,
            base_url="https://openrouter.ai/api/v1"
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
            name="TradingAgent",
            instructions="Answer any question user asks related to trading stocks or crypto only."
            "Use the web search tool to get the latest information about stock or crypto market.",
            model=self.model
            # tools=[WebSearchTool()]
        )

    def run(self):
        """Run the agent with a given message"""
        print("""
                This agent can only answer questions related to trading stocks or crypto.
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
                # results = self.client.agents.responses.create(
                #     session_id=self.session.id,
                #     messages=[{"role": "user", "content": message}],
                # )
                print("\nCalling Agent\n")
                # print(results.final_output)
                print(results.output_text)
                # return results.final_output
            except Exception as e:
                print(f"Error running agent: {e}")
                return None       