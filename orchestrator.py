import os
import gradio as gr
import logging
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from functionDefinitions import TOOLS, TOOL_HANDLERS

# Configure logging
logging.basicConfig(level=logging.WARN)
logging.getLogger("openai").setLevel(logging.DEBUG)

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI
MODEL = "gpt-4o"
client = AzureOpenAI(
  azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
  api_version="2024-02-01"
)


class ChatBot:
    def __init__(self):
        with open('workflows/release-workflow.txt', 'r') as file:
            self.release_process_definition = file.read()

        self.messages = [
            {
                "role": "system",
                "content": f"""
                You are a Release Process assistant. You must only answer requests related to Release Process.

                Below is the exact policy that you must follow to create a release for the user.

                POLICY:
                {self.release_process_definition}
                """
            }
        ]

    def chat(self, message, history):
        # Add user message to message history
        self._add_user_message(message)

        # Call model with message history
        response = self._call_model(self.messages)

        # Handle tool calls if any
        if response.tool_calls:
            return self._handle_function_calls(response)

        # Return response to user
        return response.content

    def _call_model(self, message):
        response = client.chat.completions.create(
            model=MODEL,
            messages=message,
            tools=TOOLS,
            parallel_tool_calls=False,
            temperature=0)
        self.messages.append(response.choices[0].message)
        return self.messages[-1]

    def _add_user_message(self, message):
        last_message = self.messages[-1]

        # Retrieve tool calls from last message
        if isinstance(last_message, dict):
            tool_calls = last_message.get("tool_calls", [])
        else:
            tool_calls = getattr(last_message, "tool_calls", [])

        if not tool_calls:
            # This is the normal conversation with the user
            self.messages.append({"role": "user", "content": message})
        else:
            # Case for handling ask_clarification response from user
            self.messages.append({"role": "tool", "content": message, "tool_call_id": tool_calls[0].id})

    def _handle_function_calls(self, response):
        first_tool_call = response.tool_calls[0]
        function_name = first_tool_call.function.name
        arguments = json.loads(first_tool_call.function.arguments)

        if function_name == "start_over":
            # Reset message history
            self.messages = [self.messages[0]]
            return "Let's start over"
        elif function_name == "ask_clarification":
            prompt = arguments.get('prompt')
            # Return prompt to ask user in UI
            return prompt
        else:
            # Call the appropriate handler for the tool
            if function_name not in TOOL_HANDLERS:
                raise ValueError(f"Unknown function: {function_name}")

            tool_response = TOOL_HANDLERS[function_name](arguments)

            # Add tool response to message history
            self.messages.append({
                "role": "tool",
                "content": json.dumps(tool_response),
                "tool_call_id": first_tool_call.id
            })

            # Call model with updated message history
            response = self._call_model(self.messages)

            # Return response to user
            return response.content


# Initialize chatbot
bot = ChatBot()

# Create Gradio interface
demo = gr.ChatInterface(
    fn=lambda message, history: bot.chat(message, history),
    chatbot=gr.Chatbot(type="messages"),
    title="Phil, your Release Chatbot",
    description="I can help you create and manage releases.",
    theme="default",
    examples=[
        "New color for the R22 mirror cap",
        "Update the infotainment system in the X33",
        "Door hinge in D21 rattling"
    ]
)

if __name__ == "__main__":
    demo.launch()
