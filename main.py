import os
import platform
import subprocess
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
        # Todo: Need to improve the functionality below tp enhance the user experience
        print("📂 If on windows, relaunching ai dev agent in a new Command Prompt window, if not exiting...")
        if platform.system() == "Windows":
            subprocess.Popen([
                "cmd.exe", "/c", "start", "cmd.exe", "/k", f"python {os.path.abspath(__file__)}"
            ])
        break
    
    messages.append({"role": "user", "content": user_input})

    user_response = perform_ai_model_request(MODEL, MODEL_API_URL, messages, file_path, language, verbose)
