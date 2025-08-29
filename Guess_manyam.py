import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessingGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Number Guessing Game")
        self.score = 0
        self.enter_binding = None  # To manage Enter key binding
        self.setup_main_menu()

    def setup_main_menu(self):
        self.clear_screen()

        tk.Label(self.root, text="Select Difficulty", font=('Helvetica', 16)).pack(pady=10)

        tk.Button(self.root, text="Easy (1-50, 10 attempts)", command=lambda: self.start_game(50, 10)).pack(pady=5)
        tk.Button(self.root, text="Medium (1-100, 7 attempts)", command=lambda: self.start_game(100, 7)).pack(pady=5)
        tk.Button(self.root, text="Hard (1-200, 5 attempts)", command=lambda: self.start_game(200, 5)).pack(pady=5)

    def start_game(self, max_number, max_attempts):
        self.max_number = max_number
        self.max_attempts = max_attempts
        self.attempts_left = max_attempts
        self.target_number = random.randint(1, max_number)
        self.last_diff = None

        self.clear_screen()

        tk.Label(self.root, text=f"Guess a number between 1 and {max_number}", font=('Helvetica', 14)).pack(pady=10)

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=5)
        self.entry.focus()

        # Rebind Enter safely
        if self.enter_binding:
            self.root.unbind('<Return>', self.enter_binding)
        self.enter_binding = self.root.bind('<Return>', lambda event: self.check_guess())

        self.submit_btn = tk.Button(self.root, text="Submit Guess", command=self.check_guess)
        self.submit_btn.pack(pady=5)

        self.feedback_label = tk.Label(self.root, text="", font=('Helvetica', 12))
        self.feedback_label.pack(pady=5)

        self.status_label = tk.Label(self.root, text=f"Attempts left: {self.attempts_left}", font=('Helvetica', 12))
        self.status_label.pack(pady=5)

    def check_guess(self):
        try:
            guess = self.entry.get()
            if not guess.isdigit():
                self.feedback_label.config(text="Please enter a valid number.")
                return

            guess = int(guess)
            if guess < 1 or guess > self.max_number:
                self.feedback_label.config(text=f"Guess must be between 1 and {self.max_number}")
                return

            self.attempts_left -= 1
            diff = abs(guess - self.target_number)

            if guess == self.target_number:
                round_score = self.max_number // (self.max_attempts - self.attempts_left or 1)
                self.score += round_score
                messagebox.showinfo("🎉 Correct!", f"You guessed it right!\nScore this round: {round_score}\nTotal Score: {self.score}")
                self.play_again()
            elif self.attempts_left == 0:
                messagebox.showinfo("💀 Game Over", f"You ran out of attempts!\nThe number was {self.target_number}")
                self.play_again()
            else:
                hint = ""
                if self.last_diff is not None:
                    if diff < self.last_diff:
                        hint = "Getting warmer 🔥"
                    elif diff > self.last_diff:
                        hint = "Getting colder 🧊"
                    else:
                        hint = "Same distance 🤔"
                else:
                    hint = "First guess - no hint yet!"

                direction = "Try higher 🔼" if guess < self.target_number else "Try lower 🔽"

                self.feedback_label.config(text=f"{hint} | {direction}")
                self.status_label.config(text=f"Attempts left: {self.attempts_left}")
                self.last_diff = diff
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

    def play_again(self):
        self.clear_screen()
        tk.Label(self.root, text="Do you want to play again?", font=('Helvetica', 14)).pack(pady=10)
        tk.Button(self.root, text="Yes", command=self.setup_main_menu).pack(pady=5)
        tk.Button(self.root, text="No", command=self.root.destroy).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")  # Optional: Set a default size
    game = NumberGuessingGameGUI(root)
    root.mainloop()
