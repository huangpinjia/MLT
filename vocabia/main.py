import tkinter as tk
from tkinter import messagebox
from quiz_logic import load_words, generate_quiz
from database import init_db, save_score, get_score_history

USERNAME = "Guest"

class VocabiaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabia - Learn Vocabulary")
        self.words = load_words()
        self.current_question = 0
        self.score = 0
        self.questions = generate_quiz(self.words)

        self.setup_widgets()

    def setup_widgets(self):
        self.question_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.question_label.pack(pady=10)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(self.root, text="", width=40, command=lambda idx=i: self.check_answer(idx))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.update_question()

    def update_question(self):
        q = self.questions[self.current_question]
        self.question_label.config(text=f"What is the meaning of: {q['word']}")
        for i, choice in enumerate(q['choices']):
            self.buttons[i].config(text=choice)

    def check_answer(self, idx):
        q = self.questions[self.current_question]
        selected = self.buttons[idx].cget('text')
        if selected == q['definition']:
            self.score += 1

        self.current_question += 1
        if self.current_question < len(self.questions):
            self.update_question()
        else:
            save_score(USERNAME, self.score, len(self.questions))
            messagebox.showinfo("Quiz Complete", f"You scored {self.score} / {len(self.questions)}")
            self.root.quit()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = VocabiaApp(root)
    root.mainloop()
