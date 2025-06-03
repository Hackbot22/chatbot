from ollama import chat
from ollama import ChatResponse
from rich.console import Console
from rich.markdown import Markdown
import os

# Simple Lojban Latin-to-Cyrillic mapping (expand as needed)
latin_to_cyrillic = {
    'a': 'а', 'b': 'б', 'c': 'ц', 'd': 'д', 'e': 'е', 'f': 'ф',
    'g': 'г', 'h': 'х', 'i': 'и', 'j': 'ж', 'k': 'к', 'l': 'л',
    'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с',
    't': 'т', 'u': 'у', 'v': 'в', 'x': 'кс', 'y': 'й', 'z': 'з',
    "'": 'ь', ' ': ' ', ',': ',', '.': '.', '?': '?', '!': '!',
}

def lojban_to_cyrillic(text: str) -> str:
    return ''.join(latin_to_cyrillic.get(char.lower(), char) for char in text)

class TranslatorChat:
    def __init__(self, model_name: str = "gemma3"):
        self.model_name = model_name
        self.pull_model()

    def pull_model(self):
        print(f"Pulling model '{self.model_name}'...")
        os.system(f"ollama pull {self.model_name}")

    def chat(self, messages):
        response: ChatResponse = chat(
            model=self.model_name,
            messages=messages
        )
        return response['message']['content']

    def translate_to_lojban(self, message: str) -> str:
        response: ChatResponse = chat(
            model=self.model_name,
            messages=[
                {
                    'role': 'user',
                    'content': f"Translate this English text to Lojban (say nothing but the output): {message}",
                }
            ]
        )
        return response['message']['content']

def main():
    translator = TranslatorChat(model_name=input("model name $ "))
    console = Console()
    os.system("cls" if os.name == "nt" else "clear")
    running = True
    translate_mode = False
    chat_history = []
    while running:
        if not translate_mode:
            user_message = input("chat $ ")
            if user_message.lower() == "/exit":
                print("Exiting chatbot...")
                break
            elif user_message.lower() == "/translate":
                translate_mode = True
                print("Switched to translate mode. Type English to translate, or /chat to return to chat mode.")
                continue
            chat_history.append({'role': 'user', 'content': user_message})
            bot_reply = translator.chat(chat_history)
            chat_history.append({'role': 'assistant', 'content': bot_reply})
            console.print(Markdown(f"**Bot:** {bot_reply}"))
        else:
            user_message = input("english $ ")
            if user_message.lower() == "/chat":
                translate_mode = False
                print("Switched to chat mode.")
                continue
            if user_message.lower() == "/exit":
                print("Exiting translator...")
                break
            lojban = translator.translate_to_lojban(user_message)
            cyrillic = lojban_to_cyrillic(lojban)
            console.print(Markdown(f"**Lojban:** {lojban}\n**Cyrillic:** {cyrillic}"))

if __name__ == "__main__":
    main()