from openai import OpenAI
from context import SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, EXAMPLES
from dotenv import load_dotenv
import gradio as gr
import os

load_dotenv(override=True)

MODEL_NAME = "claude-haiku-4-5-20251001"

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1/"

openai = OpenAI(api_key=anthropic_api_key, base_url=ANTHROPIC_BASE_URL)

system = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat(message, history):
    messages = system + history + [{"role": "user", "content": message}]
    
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)

    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(message)
        messages.extend(results)
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    return response.choices[0].message.content

if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(show_label=False)
    ).launch(css=CSS, js=JS, theme=gr.themes.Base())