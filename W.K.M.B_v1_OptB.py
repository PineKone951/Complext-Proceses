import tkinter as tk
from tkinter import messagebox

game_data = []
is_hidden = False

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

root.mainloop()