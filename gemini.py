import tkinter as tk
import textwrap
import google.generativeai as genai
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return textwrap.indent(text, '> ', predicate=lambda _: True)

genai.configure(api_key="Enter your API key here")

model = genai.GenerativeModel('gemini-pro')

class ChatGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Chat with Gemini-Pro")
        self.geometry("1000x600")

        # Add a welcome label
        self.welcome_label = tk.Label(self, text="Welcome to the Gemini-Pro Chat!", font=("Arial", 14, "bold"))
        self.welcome_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Chat history text box
        self.chat_history = tk.Text(self, height=20, width=100)
        self.chat_history.grid(row=1, column=0, rowspan=2, columnspan=3, padx=10, pady=10)
        

        # User input entry box
        self.user_input = tk.Entry(self, width=90, borderwidth=5, relief=tk.RIDGE, justify=tk.LEFT)
        self.user_input.grid(row=3, column=0, columnspan=2)

        # Send button
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.grid(row=3, column=2)

        # Clear button
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_chat_history)
        self.clear_button.grid(row=3, column=3)

        # Initialize the chat
        self.chat = model.start_chat(history=[])

        # Layout and Styling
        self.chat_history.configure(font=("Arial", 12), background="black")
        self.user_input.configure(font=("Arial", 12))
        self.send_button.configure(foreground="green")
        self.clear_button.configure(foreground="red")

    def send_message(self):
        # Get the user's message
        user_message = self.user_input.get()
        # Clear the user input entry box
        self.user_input.delete(0, tk.END)

        # Send the user's message to the chat
        response = self.chat.send_message(user_message)
        response_text = response.text
        # Convert the response text to Markdown
        markdown = Markdown(response_text)

        # Display the user's message and the response in the chat history
        self.chat_history.insert(tk.END, f"User: {user_message}\n", "user_message")
        self.chat_history.insert(tk.END, f"Gemini-Pro: {markdown._repr_markdown_()}\n", "gemini_response")
        self.chat_history.tag_configure("user_message", foreground="orange", font=("Arial", 12, "bold"))
        self.chat_history.tag_configure("gemini_response", foreground="yellow", font=("Arial", 12))


    def clear_chat_history(self):
        # Clear the chat history text box
        self.chat_history.delete('1.0', tk.END)

if __name__ == "__main__":
    gui = ChatGUI()
    gui.mainloop()

