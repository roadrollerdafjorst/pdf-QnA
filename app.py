import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import PDF_QA


class QA:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chatbot")
        self.window.geometry("500x750")

        self.file_path = ""
        self.history = []

        self.chat_log = tk.Text(self.window)
        self.user_input = ttk.Entry(self.window)
        self.send_button = ttk.Button(self.window, text="Ask", command=self.send_message)
        self.upload_button = ttk.Button(self.window, text="Upload PDF", command=self.upload_file)

        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.user_input.pack(padx=10, pady=5, fill=tk.X)
        self.send_button.pack(padx=10, pady=5)
        self.upload_button.pack(padx=10, pady=5)

    def send_message(self):
        query = self.user_input.get()
        self.append_colored_text("You: ", f"{query}", "blue")

        if self.file_path == "":
            response = "Please upload a PDF document."
            self.append_colored_text("Bot: ", f"{response}\n", "red")
        else:
            get_answer = PDF_QA.get_chain(self.file_path)
            response = get_answer({"question": query, "chat_history": self.history})["answer"]
            self.history.append((query, response))
            self.append_colored_text("Bot: ", f"{response}\n", "red")
        self.user_input.delete(0, tk.END)

    def upload_file(self):
        self.file_path = filedialog.askopenfilename()
        self.append_colored_text("Uploaded file: ", f"{(self.file_path).split('/')[-1]}\n", "black")

    def append_colored_text(self, prefix, text, color):
        self.chat_log.tag_config(color, foreground=color)
        self.chat_log.insert(tk.END, prefix, color)
        self.chat_log.insert(tk.END, text + "\n")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    qa = QA()
    qa.run()
