import tkinter as tk
from tkinter import messagebox
import datetime
import time
import threading
import winsound  

tasks = []

def add_task():
    task = task_entry.get()
    date_str = date_entry.get()
    time_str = time_entry.get()

    if task and date_str and time_str:
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()
            datetime_obj = datetime.datetime.combine(date_obj, time_obj)
            tasks.append((task, datetime_obj))
            task_list.insert(tk.END, f"{task} - {datetime_obj.strftime('%Y-%m-%d %H:%M')}")
            task_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
            time_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format. Use YYYY-MM-DD and HH:MM.")
    else:
        messagebox.showerror("Error", "Please enter task, date, and time.")

def delete_task():
    try:
        selected_task_index = task_list.curselection()[0]
        tasks.pop(selected_task_index)
        task_list.delete(selected_task_index)
    except IndexError:
        messagebox.showerror("Error", "Please select a task to delete.")

def clear_entry():
    task_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def check_reminders():
    while True:
        now = datetime.datetime.now()
        tasks_to_remove = []
        for index, (task, reminder_time) in enumerate(tasks):
            if now >= reminder_time:
                messagebox.showinfo("Reminder", f"Reminder: {task}")
                winsound.Beep(2500, 1000)  # Beep sound (frequency, duration)
                tasks_to_remove.append(index)
        for index in sorted(tasks_to_remove, reverse=True):
            tasks.pop(index)
            task_list.delete(index)
        time.sleep(60)  # Check every minute

root = tk.Tk()
root.title("To-Do List with Reminders")
root.geometry("665x450+550+250") #increased height
root.resizable(0, 0)
root.configure(bg="pink")

# Task Entry
task_label = tk.Label(root, text="Task:", bg="pink", font=("Comic Sans MS", 14))
task_label.pack(pady=5)
task_entry = tk.Entry(root, width=100)
task_entry.pack(pady=5)

# Date Entry
date_label = tk.Label(root, text="Date (YYYY-MM-DD):", bg="pink", font=("Comic Sans MS", 14))
date_label.pack(pady=5)
date_entry = tk.Entry(root, width=100)
date_entry.pack(pady=5)

# Time Entry
time_label = tk.Label(root, text="Time (HH:MM):", bg="pink", font=("Comic Sans MS", 14))
time_label.pack(pady=5)
time_entry = tk.Entry(root, width=100)
time_entry.pack(pady=5)

# Buttons Frame
button_frame = tk.Frame(root, bg="pink")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Task", command=add_task, font=("Comic Sans MS", 10))
add_button.pack(side=tk.LEFT, padx=15)

delete_button = tk.Button(button_frame, text="Delete Task", command=delete_task, font=("Comic Sans MS", 10))
delete_button.pack(side=tk.LEFT, padx=15)

clear_button = tk.Button(button_frame, text="Clear", command=clear_entry, font=("Comic Sans MS", 10))
clear_button.pack(side=tk.LEFT, padx=15)

# Task List
task_list_label = tk.Label(root, text="Tasks:", bg="pink", font=("Comic Sans MS", 14))
task_list_label.pack(pady=10)
task_list = tk.Listbox(root, width=100, height=10)
task_list.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start reminder thread
reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()

root.mainloop()