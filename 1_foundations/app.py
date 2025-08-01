from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr


load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )
    print("We are at push function with text: ", text)


def record_user_details(email="Email not provided", mobile_number="Number not provided", name="Name not provided", notes="not provided"):
    if not email and not mobile_number:
        return {"error": "Either email or mobile_number is required"}
    push(f"Recording {name} with email {email}, mobile number {mobile_number} and notes {notes}")
    print(f"We are at record_user_details function with email: {email}, mobile number: {mobile_number}, name: {name} and notes: {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording: {question} as unknown question")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "mobile_number": {
                "type": "string",
                "description": "The mobile number of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": [],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Saksham Jain"
        ## reader = PdfReader("me/FAQs.txt")
        ## self.faq = ""
        ##for page in reader.pages:
        ##    text = page.extract_text()
        ##    if text:
        ##        self.faq += text
        with open("1_foundations/me/FAQs.txt", "r", encoding="utf-8") as f:
            self.faqs = f.read()
        reader = PdfReader("1_foundations/me/Resume.pdf")
        self.resume = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text
        with open("1_foundations/me/Projects.txt", "r", encoding="utf-8") as f:
            self.projects = f.read()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"We are at handle_tool_call. Tool called: {tool_name} with arguments: {arguments}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You answer questions on {self.name}'s website, specifically about his career, background, skills, and experience.\
    You represent {self.name} faithfully and professionally, as if speaking to a potential client or employer. \
    You have access to a list of FAQs previously answered by {self.name}, as well as a summary of their resume and Projects. Use these to guide your responses. \
    If a user asks something unrelated to {self.name}'s career or background, respond humorously that you don’t know. \
    For any question you cannot answer—even if it's trivial — use the record_unknown_question tool. \
    Try to formally and subtly ask user about their details like name, phone number or email and use the record_user_details tool to save it. \
    Be engaging and helpful, but always professional."

        system_prompt += f"\n\n## FAQs:\n{self.faqs}\n\n## Resume:\n{self.resume}\n\n## Projects:\n{self.projects}"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools, tool_choice="auto")
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

# if __name__ == "__main__":
#    me = Me()
#    gr.ChatInterface(me.chat, type="messages").launch()

if __name__ == "__main__":
    me = Me()
    #gr.ChatInterface(me.chat, type="messages").launch(share=True)
    gr.ChatInterface(me.chat, type="messages").launch(
    share=True,           # Creates public link
    server_name="0.0.0.0",  # Allow external connections
    server_port=7860,     # Specify port
    debug=True            # Enable debug mode
    )
    