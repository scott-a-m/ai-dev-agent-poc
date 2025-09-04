import os
import sys
from ai_dev_agent_helpers import (
    build_prompt_and_get_messages,
    get_data_from_file,
    perform_ai_model_request
)

verbose = "--verbose" in sys.argv

MODEL = os.getenv("MODEL_NAME", "mistral")
MODEL_API_URL = os.getenv("MODEL_API_URL", "http://localhost:11434/api/chat")

(code, language, file_path) = get_data_from_file()
messages = build_prompt_and_get_messages(code, language)

user_response = perform_ai_model_request(MODEL, MODEL_API_URL, messages, file_path, language, verbose, True)

# 🔁 Multiturn loop
while True:
    user_input = user_response if user_response else input("\n💬 Ask a follow-up, type 'new' for another file, or 'exit': ").strip().lower()
    user_response = ""

    if user_input == "exit":
        print("👋 Session ended.")
        break

    elif user_input == "new":
        print("📂 Starting a new file review...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
        break

    messages.append({"role": "user", "content": user_input})

    user_response = perform_ai_model_request(MODEL, MODEL_API_URL, messages, file_path, language, verbose)

