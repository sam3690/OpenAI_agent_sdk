import os 
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
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


class AnswerAgent(BaseModel):
     answers: list[str]



class CompareResult(BaseModel):
    correct_count: int
    wrong_count: int



main_agent = Agent(
    name="StudentHelper",
    instructions="""You are a friendly teaching assistant.
    Extract the student's name and favourite subject from their message.
    Then create a fun 3-question quiz about their favourite subject.
    Return the structured data with name and subject.""",
    model=model,
    output_type=UserInfo
)


Answeragent = Agent(
    name="QuizAnswerBot",
    instructions="""You are an expert in all school subjects.
        Given the quiz questions with multiple choice answers, return the correct option letter and the correct answer text for each question, in the same order
        """,
    model=model,
    output_type=AnswerAgent
)

compare_agent = Agent(
    name="CompareAnswers",
    instructions=(
        "You will be given the correct answers and the user's answers for a quiz. "
        "Count how many answers are correct and how many are wrong. "
        "Return only the numbers as 'correct_count' and 'wrong_count'."
    ),
    model=model,
    output_type=CompareResult
)


result = Runner.run_sync(
    main_agent,
   input("Enter your name and favourite subject: "),
)

answer_result = Runner.run_sync(
    Answeragent,
    f"Questions: {result.final_output.quiz}."
)

print("\nExtracted Information:")
print(f"Name: {result.final_output.name}")
print(f"Favourite Subject: {result.final_output.favourite_subject}")
print("\nGenerated Quiz:")
print(result.final_output.quiz)
print(f"Answer of quiz:{answer_result.final_output.answers}")


user_answers = []
for i in range(len(answer_result.final_output.answers)):
    ans = input(f"Your answer for Q{i+1} (a/b/c/d): ").strip().lower()
    user_answers.append(ans)


compare_input = f"Correct answers: {answer_result.final_output.answers}\nUser answers: {user_answers}"
compare_result = Runner.run_sync(compare_agent, compare_input)

print(f"\n Correct: {compare_result.final_output.correct_count}")
print(f" Wrong: {compare_result.final_output.wrong_count}")