import random
import tkinter as tk
from tkinter import messagebox

from Data import questions
from Backend import get_questions, check_answer, calculate_score, quiz_finished
from Frontend import welcome_screen, display_questions, get_user_answer, show_correct, show_incorrect, show_final_score

def get_questions_for_difficulty(question_data, difficulty):
    return [question for question in question_data if question.get("difficulty") == difficulty]


class SynapseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Synapse Quiz")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f7fb")
        self.root.resizable(False, False)

        self.current_frame = None
        self.name_entry = None
        self.age_entry = None
        self.user_name = ""
        self.user_age = 0
        self.selected_difficulty = None
        self.quiz_questions = []
        self.current_question_index = 0
        self.score = 0

        self.show_home_screen()

    def clear_screen(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def show_home_screen(self):
        self.clear_screen()
        self.current_frame = tk.Frame(self.root, bg="#f4f7fb")
        self.current_frame.pack(fill="both", expand=True)

        title = tk.Label(
            self.current_frame,
            text="Welcome to Synapse Quiz",
            font=("Segoe UI", 24, "bold"),
            bg="#f4f7fb",
            fg="#1f3a5f",
        )
        title.pack(pady=40)

        subtitle = tk.Label(
            self.current_frame,
            text="Test your knowledge with fun quiz questions",
            font=("Segoe UI", 12),
            bg="#f4f7fb",
            fg="#4b5563",
        )
        subtitle.pack(pady=10)

        start_button = tk.Button(
            self.current_frame,
            text="Start Quiz",
            font=("Segoe UI", 12, "bold"),
            width=18,
            bg="#2563eb",
            fg="white",
            command=self.show_user_screen,
        )
        start_button.pack(pady=20)

    def show_user_screen(self):
        self.clear_screen()
        self.current_frame = tk.Frame(self.root, bg="#f4f7fb")
        self.current_frame.pack(fill="both", expand=True)

        tk.Label(
            self.current_frame,
            text="Enter your details",
            font=("Segoe UI", 18, "bold"),
            bg="#f4f7fb",
            fg="#1f3a5f",
        ).pack(pady=20)

        tk.Label(self.current_frame, text="Name:", bg="#f4f7fb").pack(pady=(10, 2))
        self.name_entry = tk.Entry(self.current_frame, width=30)
        self.name_entry.pack()

        tk.Label(self.current_frame, text="Age:", bg="#f4f7fb").pack(pady=(10, 2))
        self.age_entry = tk.Entry(self.current_frame, width=30)
        self.age_entry.pack()

        submit_button = tk.Button(
            self.current_frame,
            text="Continue",
            font=("Segoe UI", 11, "bold"),
            width=15,
            bg="#10b981",
            fg="white",
            command=self.validate_user,
        )
        submit_button.pack(pady=20)

    def validate_user(self):
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()

        if not name:
            messagebox.showwarning("Missing name", "Please enter your name.")
            return

        if not age.isdigit() or int(age) < 12:
            messagebox.showwarning("Invalid age", "Age must be 12 or older.")
            return

        self.user_name = name
        self.user_age = int(age)
        self.show_difficulty_screen()

    def show_difficulty_screen(self):
        self.clear_screen()
        self.current_frame = tk.Frame(self.root, bg="#f4f7fb")
        self.current_frame.pack(fill="both", expand=True)

        tk.Label(
            self.current_frame,
            text="Choose Difficulty",
            font=("Segoe UI", 18, "bold"),
            bg="#f4f7fb",
            fg="#1f3a5f",
        ).pack(pady=30)

        tk.Button(
            self.current_frame,
            text="Easy",
            width=20,
            command=lambda: self.start_quiz("easy"),
        ).pack(pady=8)
        tk.Button(
            self.current_frame,
            text="Medium",
            width=20,
            command=lambda: self.start_quiz("medium"),
        ).pack(pady=8)
        tk.Button(
            self.current_frame,
            text="Hard",
            width=20,
            command=lambda: self.start_quiz("hard"),
        ).pack(pady=8)

    def start_quiz(self, difficulty):
        self.selected_difficulty = difficulty
        self.quiz_questions = get_questions_for_difficulty(questions, difficulty)
        random.shuffle(self.quiz_questions)
        self.current_question_index = 0
        self.score = 0

        if not self.quiz_questions:
            messagebox.showinfo("No questions", "No questions are available for this difficulty yet.")
            return

        self.show_question_screen()

    def show_question_screen(self):
        self.clear_screen()
        self.current_frame = tk.Frame(self.root, bg="#f4f7fb")
        self.current_frame.pack(fill="both", expand=True)

        if self.current_question_index >= len(self.quiz_questions):
            self.show_result_screen()
            return

        question = self.quiz_questions[self.current_question_index]
        question_text = question["question"]
        options = question["options"]

        tk.Label(
            self.current_frame,
            text=f"Hello {self.user_name}!",
            font=("Segoe UI", 12),
            bg="#f4f7fb",
            fg="#374151",
        ).pack(pady=(10, 5))

        tk.Label(
            self.current_frame,
            text=f"Question {self.current_question_index + 1} of {len(self.quiz_questions)}",
            font=("Segoe UI", 10),
            bg="#f4f7fb",
            fg="#6b7280",
        ).pack()

        tk.Label(
            self.current_frame,
            text=question_text,
            font=("Segoe UI", 16, "bold"),
            wraplength=700,
            justify="center",
            bg="#f4f7fb",
            fg="#111827",
        ).pack(pady=25)

        for index, option in enumerate(options):
            tk.Button(
                self.current_frame,
                text=option,
                width=35,
                pady=8,
                command=lambda selected=index: self.check_answer(selected),
            ).pack(pady=6)

    def check_answer(self, selected_index):
        question = self.quiz_questions[self.current_question_index]
        if selected_index == question["correct_index"]:
            self.score += 1

        self.current_question_index += 1
        self.show_question_screen()

    def show_result_screen(self):
        self.clear_screen()
        self.current_frame = tk.Frame(self.root, bg="#f4f7fb")
        self.current_frame.pack(fill="both", expand=True)

        tk.Label(
            self.current_frame,
            text="Quiz Complete",
            font=("Segoe UI", 22, "bold"),
            bg="#f4f7fb",
            fg="#1f3a5f",
        ).pack(pady=20)

        tk.Label(
            self.current_frame,
            text=f"{self.user_name}, you scored {self.score} out of {len(self.quiz_questions)}",
            font=("Segoe UI", 14),
            bg="#f4f7fb",
            fg="#374151",
        ).pack(pady=12)

        tk.Button(
            self.current_frame,
            text="Play Again",
            width=18,
            command=self.show_difficulty_screen,
        ).pack(pady=10)

        tk.Button(
            self.current_frame,
            text="Back to Home",
            width=18,
            command=self.show_home_screen,
        ).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = SynapseApp(root)
    root.mainloop()