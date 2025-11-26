import tkinter as tk
import random

class MathQuiz:
    def __init__(self, root):
        # Initialize the main window and quiz variables
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.geometry("400x400")  # Set window size
        self.root.configure(bg="#f0f8ff")  # Light blue background
        self.score = 0
        self.question_count = 0
        self.correct_answer = None
        self.attempt = 1
        self.digits = 1        
        self.displayMenu()

    # ---------------- DISPLAY MENU ----------------
    def displayMenu(self):
        # Clear the window and display difficulty selection menu with improved design
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame for centering
        main_frame = tk.Frame(self.root, bg="#f0f8ff")
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="DIFFICULTY LEVEL", font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#2e8b57").pack(pady=20)
        
        # Buttons with colors and hover effects
        easy_btn = tk.Button(main_frame, text="Easy (1 digit)", width=20, font=("Arial", 14), bg="#90ee90", fg="black", command=lambda: self.start_quiz(1))
        easy_btn.pack(pady=10)
        easy_btn.bind("<Enter>", lambda e: easy_btn.config(bg="#32cd32"))
        easy_btn.bind("<Leave>", lambda e: easy_btn.config(bg="#90ee90"))
        
        moderate_btn = tk.Button(main_frame, text="Moderate (2 digits)", width=20, font=("Arial", 14), bg="#ffa500", fg="black", command=lambda: self.start_quiz(2))
        moderate_btn.pack(pady=10)
        moderate_btn.bind("<Enter>", lambda e: moderate_btn.config(bg="#ff8c00"))
        moderate_btn.bind("<Leave>", lambda e: moderate_btn.config(bg="#ffa500"))
        
        advanced_btn = tk.Button(main_frame, text="Advanced (4 digits)", width=20, font=("Arial", 14), bg="#ff6347", fg="black", command=lambda: self.start_quiz(4))
        advanced_btn.pack(pady=10)
        advanced_btn.bind("<Enter>", lambda e: advanced_btn.config(bg="#dc143c"))
        advanced_btn.bind("<Leave>", lambda e: advanced_btn.config(bg="#ff6347"))
        
        # Added Exit button to the menu
        exit_btn = tk.Button(main_frame, text="Exit", font=("Arial", 14), bg="#dc143c", fg="white", command=self.root.quit)
        exit_btn.pack(pady=10)
        exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg="#b22222"))
        exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg="#dc143c"))

    # ---------------- START QUIZ ----------------
    def start_quiz(self, digits):
        self.digits = digits
        self.score = 0
        self.question_count = 0
        self.next_question()

    # ---------------- RANDOM NUMBER GENERATION ----------------
    def randomInt(self):
        low = 10 ** (self.digits - 1)
        high = 10 ** self.digits - 1
        return random.randint(low, high)

    # ---------------- DECIDE OPERATION (+ or -) ----------------
    def decideOperation(self):
        return random.choice(["+", "-"])

    # ---------------- DISPLAY PROBLEM ----------------
    def displayProblem(self):
        num1 = self.randomInt()
        num2 = self.randomInt()
        op = self.decideOperation()

        if op == "+":
            self.correct_answer = num1 + num2
        else:
            self.correct_answer = num1 - num2

        return f"{num1} {op} {num2} ="

    # ---------------- CHECK IF ANSWER IS CORRECT ----------------
    def isCorrect(self, user_answer):
        return user_answer == self.correct_answer

    # ---------------- HANDLE NEXT QUESTION ----------------
    def next_question(self):
        if self.question_count >= 10:
            self.displayResults()
            return

        self.question_count += 1
        self.attempt = 1

        self.problem = self.displayProblem()

        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame for question UI
        main_frame = tk.Frame(self.root, bg="#f0f8ff")
        main_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(main_frame, text=f"Question {self.question_count}/10", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#2e8b57").pack(pady=10)
        tk.Label(main_frame, text=self.problem, font=("Arial", 24, "bold"), bg="#f0f8ff", fg="#000080").pack(pady=20)

        self.answer_entry = tk.Entry(main_frame, font=("Arial", 18), width=10, justify="center")
        self.answer_entry.pack(pady=10)

        submit_btn = tk.Button(main_frame, text="Submit", font=("Arial", 14), bg="#4682b4", fg="white", command=self.check_answer)
        submit_btn.pack(pady=10)
        submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="#1e90ff"))
        submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="#4682b4"))

        self.feedback = tk.Label(main_frame, text="", font=("Arial", 14), bg="#f0f8ff", fg="red")
        self.feedback.pack(pady=10)

        # Added Quit button to allow quitting the quiz anytime
        quit_btn = tk.Button(main_frame, text="Quit Quiz", font=("Arial", 12), bg="#dc143c", fg="white", command=self.displayMenu)
        quit_btn.pack(pady=5)
        quit_btn.bind("<Enter>", lambda e: quit_btn.config(bg="#b22222"))
        quit_btn.bind("<Leave>", lambda e: quit_btn.config(bg="#dc143c"))

        # Added score display in the top-right corner
        self.score_label = tk.Label(main_frame, text=f"Score: {self.score}", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#000080")
        self.score_label.place(relx=1.0, rely=0.0, anchor="ne")

    # ---------------- CHECK USER ANSWER ----------------
    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            self.feedback.config(text="Please enter a number.")
            return

        if self.isCorrect(user_answer):
            if self.attempt == 1:
                self.score += 10
                self.feedback.config(text="Correct! +10 points", fg="green")
            else:
                self.score += 5
                self.feedback.config(text="Correct! +5 points", fg="green")

            # Update score label
            self.score_label.config(text=f"Score: {self.score}")
            self.root.after(1000, self.next_question)

        else:
            if self.attempt == 1:
                self.attempt = 2
                self.feedback.config(text="Wrong. Try again!", fg="orange")
            else:
                self.feedback.config(text=f"Wrong again. The correct answer was {self.correct_answer}.", fg="red")
                self.root.after(1500, self.next_question)

    # ---------------- DISPLAY FINAL RESULTS ----------------
    def displayResults(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame for results UI
        main_frame = tk.Frame(self.root, bg="#f0f8ff")
        main_frame.pack(expand=True, fill=tk.BOTH)

        grade = self.calculateGrade()

        tk.Label(main_frame, text="Quiz Completed!", font=("Arial", 22, "bold"), bg="#f0f8ff", fg="#2e8b57").pack(pady=20)
        tk.Label(main_frame, text=f"Final Score: {self.score}/100", font=("Arial", 18), bg="#f0f8ff", fg="#000080").pack(pady=10)
        tk.Label(main_frame, text=f"Rank: {grade}", font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#ff4500").pack(pady=10)

        play_again_btn = tk.Button(main_frame, text="Play Again", font=("Arial", 14), bg="#32cd32", fg="white", command=self.displayMenu)
        play_again_btn.pack(pady=10)
        play_again_btn.bind("<Enter>", lambda e: play_again_btn.config(bg="#228b22"))
        play_again_btn.bind("<Leave>", lambda e: play_again_btn.config(bg="#32cd32"))

        exit_btn = tk.Button(main_frame, text="Exit", font=("Arial", 14), bg="#dc143c", fg="white", command=self.root.quit)
        exit_btn.pack(pady=5)
        exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg="#b22222"))
        exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg="#dc143c"))

    # ---------------- GRADE CALCULATOR ----------------
    def calculateGrade(self):
        if self.score >= 90:
            return "A+"
        elif self.score >= 80:
            return "A"
        elif self.score >= 70:
            return "B"
        elif self.score >= 60:
            return "C"
        elif self.score >= 50:
            return "D"
        else:
            return "F"


# ---------------- RUN APP ----------------
root = tk.Tk()
MathQuiz(root)
root.mainloop()
