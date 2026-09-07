import tkinter as tk
from tkinter import messagebox

game_data = []

def lock_in_questions():
    global game_data
    game_data.clear()

    q1, a1 = entry_q1.get().strip(), entry_a1.get().strip()
    q2, a2 = entry_q2.get().strip(), entry_a2.get().strip()
    q3, a3 = entry_a3.get().strip(), entry_a3.get().strip()

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
root.geometry("400x500")

setup_frame = tk.Frame(root)
setup_frame.pack(pady=20)

tk.Label(setup_frame, text="Host Setup", font=("Arial", 16)).pack(pady=10)

tk.Label(setup_frame, text="Question 1:").pack()
entry_q1 = tk.Entry(setup_frame)
entry_q1.pack()
tk.Label(setup_frame, text="Secret Answer 1:").pack()
entry_a1 = tk.Entry(setup_frame, show="*")
entry_a1.pack()

tk.Label(setup_frame, text="Question 2:").pack()
entry_q2 = tk.Entry(setup_frame)
entry_q2.pack()
tk.Label(setup_frame, text="Secret Answer 2:").pack()
entry_a2 = tk.Entry(setup_frame, show="*")
entry_a2.pack()

tk.Label(setup_frame, text="Question 3:").pack()
entry_q3 = tk.Entry(setup_frame)
entry_q3.pack()
tk.Label(setup_frame, text="Secret Answer 3:").pack()
entry_a3 = tk.Entry(setup_frame, show="*")
entry_a3.pack()

lock_btn = tk.Button(setup_frame, text="Lock In & Pass Laptop", command=lock_in_questions)
lock_btn.pack(pady=20)

root.mainloop()