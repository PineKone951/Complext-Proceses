import tkinter as tk
from tkinter import messagebox
import random
import re


SCORING_MODE = "end" # "instant" or "end"

RESULTS_MODE = "score_only" # "breakdown" or "score_only"


game_data = []
guesses = []
is_hidden = True
current_question = 0
score = 0
selected_answer = None

# Matches whole numbers written normally (e.g. 12, 2008, -5) but not things like 007 or 1,000
NUMBER_PATTERN = re.compile(r"^-?(0|[1-9]\d*)$")


def apply_answer_masking():
    # Show or hide the secret answers and keep the toggle button text in step
    char_to_show = "*" if is_hidden else ""

    entry_a1.config(show=char_to_show)
    entry_a2.config(show=char_to_show)
    entry_a3.config(show=char_to_show)

    if is_hidden:
        toggle_btn.config(text="Show Answers")
    else:
        toggle_btn.config(text="Hide Answers")


def toggle_answers():
    global is_hidden
    is_hidden = not is_hidden
    apply_answer_masking()


def reset_setup():
    # Clear the last game so the next host starts fresh and Player 2 can't see old answers
    global is_hidden
    game_data.clear()

    for entry in (entry_q1, entry_a1, entry_q2, entry_a2, entry_q3, entry_a3):
        entry.delete(0, tk.END)

    is_hidden = True
    apply_answer_masking()


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


def make_number_decoys(correct_text, how_many=2):
    # Make false answers with values close to the real one so elimination doesn't work
    n = int(correct_text)

    if 1900 <= n <= 2100:
        spread = 8  # looks like a year, so keep the false answers close
    else:
        spread = max(3, round(abs(n) * 0.2))

    candidates = [n + offset for offset in range(-spread, spread + 1) if offset != 0]
    if n >= 0:
        candidates = [c for c in candidates if c >= 0]  # no negative ages, counts, etc.

    return [str(c) for c in random.sample(candidates, how_many)]


def make_choices(question_index):
    # Build the list of buttons Player 2 sees: the real answer plus false ones
    correct = game_data[question_index]["answer"]

    if NUMBER_PATTERN.match(correct):
        decoys = make_number_decoys(correct)
    else:
        # Text answers can't be generated, so use the host's other answers as false options
        decoys = []
        for i, item in enumerate(game_data):
            other = item["answer"]
            taken = [correct.lower()] + [d.lower() for d in decoys]
            if i != question_index and other.lower() not in taken:
                decoys.append(other)

    choices = [correct] + decoys
    random.shuffle(choices)
    return choices


def start_guessing_game():
    global current_question, score
    current_question = 0
    score = 0
    guesses.clear()
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

    choices = make_choices(current_question)
    for button, choice in zip(answer_buttons, choices):
        button.config(text=choice, state="normal", bg=default_button_bg)
        button.pack(fill="x", padx=35, pady=6)


def choose_answer(clicked_button):
    global selected_answer, score
    if selected_answer is not None:
        return

    answer = clicked_button["text"]
    selected_answer = answer
    correct_answer = game_data[current_question]["answer"]
    guesses.append(answer)

    for button in answer_buttons:
        button.config(state="disabled")
    clicked_button.config(bg="light blue")

    if answer == correct_answer:
        score += 1

    if SCORING_MODE == "instant":
        # Option A: tell Player 2 straight away
        if answer == correct_answer:
            feedback_label.config(text="Correct!", fg="green")
        else:
            feedback_label.config(
                text=f"Not quite. The answer was: {correct_answer}",
                fg="red"
            )
    else:
        # Option B: keep the result secret until the end
        feedback_label.config(text="Answer locked in!", fg="black")

    next_btn.config(state="normal")


def get_friend_message(points, total):
    ratio = points / total
    if ratio == 1:
        return "Best Friends!"
    elif ratio >= 0.6:
        return "Good Friends!"
    elif ratio > 0:
        return "Acquaintances!"
    else:
        return "Strangers!"


def show_results():
    guessing_frame.pack_forget()

    total = len(game_data)
    score_label.config(text=f"You scored {score} out of {total}!")
    message_label.config(text=get_friend_message(score, total))

    # Clear any breakdown left over from the last game
    for widget in breakdown_frame.winfo_children():
        widget.destroy()

    if RESULTS_MODE == "breakdown":
        # Option B: show what the host entered next to what Player 2 picked
        for i, item in enumerate(game_data):
            got_it = guesses[i] == item["answer"]
            row = tk.Frame(breakdown_frame)
            row.pack(fill="x", padx=20, pady=4)
            tk.Label(
                row, text=f"Q{i + 1}: {item['question']}", font=("Arial", 11, "bold"),
                wraplength=340, justify="left", anchor="w"
            ).pack(fill="x")
            tk.Label(
                row, text=f"Host's answer: {item['answer']}", font=("Arial", 11),
                wraplength=340, justify="left", anchor="w"
            ).pack(fill="x")
            tk.Label(
                row,
                text=f"Player 2 picked: {guesses[i]} ({'Correct' if got_it else 'Wrong'})",
                font=("Arial", 11), fg="green" if got_it else "red",
                wraplength=340, justify="left", anchor="w"
            ).pack(fill="x")
        play_again_btn.config(text="Play Again / Swap Players")
    else:
        # Option A: just the score and message
        play_again_btn.config(text="Play Again")

    results_frame.pack(fill="both", expand=True, pady=20)


def play_again():
    results_frame.pack_forget()
    reset_setup()
    setup_frame.pack(pady=20)


def next_question():
    global current_question
    current_question += 1

    if current_question == len(game_data):
        show_results()
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

toggle_btn = tk.Button(setup_frame, text="Show Answers", command=toggle_answers)
toggle_btn.pack(pady=10)
apply_answer_masking()  # answers start hidden

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

default_button_bg = answer_buttons[0].cget("bg")  # works on any operating system


def connect_answer_commands():
    for button in answer_buttons:
        button.config(command=lambda selected=button: choose_answer(selected))


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

results_frame = tk.Frame(root)

tk.Label(results_frame, text="Game Over!", font=("Arial", 18)).pack(pady=8)
score_label = tk.Label(results_frame, text="", font=("Arial", 16))
score_label.pack(pady=6)
message_label = tk.Label(results_frame, text="", font=("Arial", 20, "bold"))
message_label.pack(pady=6)

breakdown_frame = tk.Frame(results_frame)
breakdown_frame.pack(fill="x")

play_again_btn = tk.Button(results_frame, text="Play Again", command=play_again)
play_again_btn.pack(pady=15)

root.mainloop()
