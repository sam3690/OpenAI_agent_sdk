import os
from agents import Agent, Runner, TResponseInputItem, RunContextWrapper, GuardrailFunctionOutput, input_guardrail, InputGuardrailTripwireTriggered, trace
from dotenv import load_dotenv
from WebSearchTool import custom_web_search
from pydantic import BaseModel
from openai.types.responses import ResponseTextDeltaEvent

class ResearchAgent:
    """ A simple research agent that uses web search and browsing tools. """
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        class PoliticsOutput(BaseModel):
            is_politics: bool
            reasoning: str
        
        guardrail_agent = Agent( 
            name="Guardrail check",
            instructions = "Check if the user is asking questions related to politics.",
            output_type=PoliticsOutput,
        )


        @input_guardrail
        async def politics_guardrail( 
            ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
        ) -> GuardrailFunctionOutput:
            result = await Runner.run(guardrail_agent, input, context=ctx.context)

            return GuardrailFunctionOutput(
                output_info=result.final_output, 
                tripwire_triggered=result.final_output.is_politics,
            )

        self.agent = Agent(
            name = "ReserchAgent",
            instructions = """
                    You are a helpful research assistant.
                - If the user asks a question, use custom_web_search to find the answer and explain simply.
                - If the user provides a URL, use web_browser to read it.
                - Only summarize the article if it is related to education or learning.
                - If it is not about education, politely say it's not relevant to education.
                - Always provide concise and clear answers.

                """,
            input_guardrails=[politics_guardrail],
            tools = [custom_web_search]
        )

    with trace("ResearchAgentRun"):
        # agents.map((agent) => {aasdfasdf})
        async def run(self):
                runner = Runner()
                print("""
                        This is Research Agent for Summarization, Comparison, and Learning.
                        Enter 'exit' to exit the agent.
                    """)
                try:
                    while True:
                        user_input = input("Ask me anything : ")

                        if user_input.lower() in ["quit", "exit"]:
                            break

                        result = runner.run_streamed(self.agent, user_input)

                        async for event in result.stream_events():
                            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                                print(event.data.delta, end="", flush=True)
                    print("\n")
                    print("\n")
                    print("\n")

                except InputGuardrailTripwireTriggered:
                    print("Math homework guardrail tripped")


                    