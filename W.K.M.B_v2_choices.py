import tkinter as tk
from tkinter import messagebox
import random

game_data = []
is_hidden = False
current_question = 0
score = 0
selected_answer = None

def toggle_answers():
    global is_hidden
    is_hidden = not is_hidden
    
    char_to_show = "*" if is_hidden else ""
    
    entry_a1.config(show=char_to_show)
    entry_a2.config(show=char_to_show)
    entry_a3.config(show=char_to_show)
    
    if is_hidden:
        toggle_btn.config(text="Show Answers")
    else:
        toggle_btn.config(text="Hide Answers")

def lock_in_questions():
    global game_data
    game_data.clear()

    q1, a1 = entry_q1.get().strip(), entry_a1.get().strip()
    q2, a2 = entry_q2.get().strip(), entry_a2.get().strip()
    q3, a3 = entry_q3.get().strip(), entry_a3.get().strip()

    if not (q1 and a1 and q2 and a2 and q3 and a3):
        messagebox.showwarning("Error", "Please fill in all fields!")
        return

    game_data = [
        {"question": q1, "answer": a1},
        {"question": q2, "answer": a2},
        {"question": q3, "answer": a3}
    ]

    messagebox.showinfo("Success", "Pass the laptop to Player 2!")
    setup_frame.pack_forget()
    start_guessing_game()

def start_guessing_game():
    global current_question, score
    current_question = 0
    score = 0
    guessing_frame.pack(fill="both", expand=True, pady=20)
    show_question()

def show_question():
    global selected_answer
    selected_answer = None

    question_data = game_data[current_question]
    question_number_label.config(
        text=f"Question {current_question + 1} of {len(game_data)}"
    )
    question_label.config(text=question_data["question"])
    feedback_label.config(text="", fg="black")
    next_btn.config(state="disabled")

    for button in answer_buttons:
        button.pack_forget()

    choices = [item["answer"] for item in game_data]
    random.shuffle(choices)
    for button, choice in zip(answer_buttons, choices):
        button.config(text=choice, state="normal", bg="SystemButtonFace")
        button.pack(fill="x", padx=35, pady=6)

def choose_answer(answer):
    global selected_answer, score
    if selected_answer is not None:
        return

    selected_answer = answer
    correct_answer = game_data[current_question]["answer"]
    for button in answer_buttons:
        if button["text"] == answer:
            button.config(bg="light blue")
        button.config(state="disabled")

    if answer == correct_answer:
        score += 1
        feedback_label.config(text="Correct!", fg="green")
    else:
        feedback_label.config(
            text=f"Not quite. The answer was: {correct_answer}",
            fg="red"
        )

    next_btn.config(state="normal")

def next_question():
    global current_question
    current_question += 1

    if current_question == len(game_data):
        guessing_frame.pack_forget()
        messagebox.showinfo(
            "Game Over",
            f"You scored {score} out of {len(game_data)}!"
        )
        setup_frame.pack(pady=20)
        return

    show_question()

root = tk.Tk()
root.title("Who Knows Me Best?")
root.geometry("400x650")

setup_frame = tk.Frame(root)
setup_frame.pack(pady=20)

tk.Label(setup_frame, text="Host Setup (Option B)", font=("Arial", 18)).pack(pady=12)

tk.Label(setup_frame, text="Question 1:", font=("Arial", 14)).pack(pady=10)
entry_q1 = tk.Entry(setup_frame)
entry_q1.pack()
tk.Label(setup_frame, text="Secret Answer 1:", font=("Arial", 14)).pack(pady=12)
entry_a1 = tk.Entry(setup_frame)
entry_a1.pack()

tk.Label(setup_frame, text="Question 2:", font=("Arial", 14)).pack(pady=12)
entry_q2 = tk.Entry(setup_frame)
entry_q2.pack()
tk.Label(setup_frame, text="Secret Answer 2:", font=("Arial", 14)).pack(pady=12)
entry_a2 = tk.Entry(setup_frame)
entry_a2.pack()

tk.Label(setup_frame, text="Question 3:", font=("Arial", 14)).pack(pady=12)
entry_q3 = tk.Entry(setup_frame)
entry_q3.pack()
tk.Label(setup_frame, text="Secret Answer 3:", font=("Arial", 14)).pack(pady=12)
entry_a3 = tk.Entry(setup_frame)
entry_a3.pack()

toggle_btn = tk.Button(setup_frame, text="Hide Answers", command=toggle_answers)
toggle_btn.pack(pady=10)

lock_btn = tk.Button(setup_frame, text="Lock In & Pass Laptop", command=lock_in_questions)
lock_btn.pack(pady=10)

guessing_frame = tk.Frame(root)

question_number_label = tk.Label(
    guessing_frame, text="", font=("Arial", 14)
)
question_number_label.pack(pady=10)

tk.Label(
    guessing_frame, text="Player 2: Make your guess!",
    font=("Arial", 18)
).pack(pady=12)

question_label = tk.Label(
    guessing_frame, text="", font=("Arial", 16),
    wraplength=340, justify="center"
)
question_label.pack(pady=25)

answer_buttons = []
for _ in range(3):
    button = tk.Button(
        guessing_frame, text="", font=("Arial", 13),
        command=lambda: None
    )
    answer_buttons.append(button)

def connect_answer_commands():
    for button in answer_buttons:
        button.config(command=lambda selected=button: choose_answer(selected["text"]))

connect_answer_commands()

feedback_label = tk.Label(
    guessing_frame, text="", font=("Arial", 12),
    wraplength=340, justify="center"
)
feedback_label.pack(pady=12)

next_btn = tk.Button(
    guessing_frame, text="Next Question",
    command=next_question, state="disabled"
)
next_btn.pack(pady=15)

root.mainloop()