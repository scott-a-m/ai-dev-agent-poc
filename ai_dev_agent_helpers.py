import json
import os
import re
import sys
import requests

def detect_language(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    ext_to_lang = {
        ".py": "python", ".js": "javascript", ".ts": "typescript", ".java": "java",
        ".cpp": "c++", ".c": "c", ".cs": "c#", ".go": "go", ".rb": "ruby",
        ".php": "php", ".html": "html", ".css": "css", ".sh": "bash",
        ".rs": "rust", ".swift": "swift", ".kt": "kotlin", ".sql": "sql",
        ".json": "json", ".xml": "xml"
    }
    return ext_to_lang.get(ext, "plain text")

def build_prompt_and_get_messages(code: str, language: str) -> list:
    prompt = f"""
    Please review the following {language} code for:
    - Bugs or syntax issues
    - Performance problems
    - Best practices
    - Maintainability

    Return:
    - The fixed or optimized version of the code in a single block enclosed within triple backticks.
    - A brief explanation of what was changed and why.

    Here is the code:

    ```{language}
    {code}```
    """
    messages = [
        {
            "role": "system",
            "content": "You are a senior software engineer. Review code for bugs, performance, best practices, and maintainability. Respond with clear diagnostics and concise suggestions."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    return messages

def extract_code_block(text: str) -> str:
    match = re.search(r"```([a-zA-Z0-9#+-]*)\n(.*?)```", text, re.DOTALL)
    return match.group(2).strip() if match else None

def handle_ai_response(message: str, file_path: str) -> str:
    fixed_code = extract_code_block(message)

    if fixed_code:
        user_input = input("\n⚠️ Do you want to overwrite the original file with this updated code? If yes, then respond with 'y', if no, how can I further refine the code for you? \n\n").strip()

        if user_input.lower() == "y":
            backup_path = file_path + ".bak"
            os.rename(file_path, backup_path)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_code)

            print(f"\n✅ File has been updated and saved.")
            print(f"🛡️ Backup saved as: {backup_path}")
            return ""
        else:
            return user_input
    else:
        print("\n⚠️ No code has been detected in the code checker response.")
        return ""

def get_data_from_file(prompt: str ="📄 Enter file path: ") -> tuple:
    print("Hi there👋! Hope your day is going well. What file would you like me to take a look at?")
    while True:
        path = input(prompt).strip()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            language = detect_language(path)
            return (code, language, path)
        print(f"❌ File not found: {path}")
        print("🔁 Try again.")


def perform_ai_model_request(model: str, api_url: str, messages: list, file_path: str, language: str, verbose: bool, firstRequest: bool = False):
    try:
        payload = {
            "model": model,
            "messages": messages,
            "stream": True
        }

        if firstRequest:
            print(f"\n🔎 I am now reviewing your {language} code, please hang on a moment...\n")
        else:
            print("\n🧠 Thinking...\n")

        response = requests.post(api_url, json=payload, stream=True)

        full_message = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    content = chunk.get("message", {}).get("content", "")
                    print(content, end="", flush=True)
                    full_message += content
                except json.JSONDecodeError:
                    print("\n⚠️ Failed to decode streamed chunk:", line.decode("utf-8"))

        print()
        
        messages.append({"role": "assistant", "content": full_message})

        if verbose:
            print("\n📡 Streaming payload:")
            print(json.dumps(payload, indent=2))
            print("\n📨 Full streamed response:")
            print(full_message)

        user_response = handle_ai_response(full_message, file_path)
        return user_response

    except requests.exceptions.RequestException as e:
        print("❌ Local API request failed:", e)
        sys.exit(1)

def log_http_transaction(endpoint: str, headers: dict, payload: dict, response: dict):
    print("\n📡 HTTP Request:")
    print(f"POST {endpoint}")
    print("Headers:")
    for k, v in headers.items():
        print(f"  {k}: {v}")
    print("\nPayload:")
    print(json.dumps(payload, indent=2))

    print("\n📨 HTTP Response:")
    print(json.dumps(response, indent=2))

