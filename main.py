import os

from google import genai
from dotenv import load_dotenv
load_dotenv()

from components.tools import (
    sum_of_nums,
    subtract,
    multiply,
    divide,
    percentage,
    run_python_script,
    send_email,
    ask_user,
    compile_latex_to_pdf,
    search_papers,
    get_weather,
    web_search,
    get_youtube_transcript,
    show_local_images,
    get_current_date_time,
    get_long_term_context
)
from components.agents import Agent

TOOLS = [
    sum_of_nums,
    subtract,
    multiply,
    divide,
    percentage,
    run_python_script,
    send_email,
    ask_user,
    compile_latex_to_pdf,
    search_papers,
    get_weather,
    web_search,
    get_youtube_transcript,
    show_local_images,
    get_current_date_time,
    get_long_term_context
]

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)
agent = Agent(
    name="SmartAssistant",
    goal="Help users solve problems using tools(if required) and reasoning",
    backstory="An AI trained in computation, automation, and problem solving.",
    tools=TOOLS,
    client=client
)
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        break
    if not user_input.strip():
        continue

    response = agent.run(user_input)
    print("\n")
    print(80*"#")
    print("Agent:", response.text)
    print(80*"#")
    print("\n")