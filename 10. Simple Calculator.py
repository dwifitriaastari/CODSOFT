import tkinter as tk
import math
import ast

memory = 0  

def calculate():
    """Performs the calculation based on the display."""
    try:
        expression = display.get()
        # Replace mathematical symbols for evaluation
        expression = expression.replace("√", "math.sqrt").replace("^", "**")
        result = eval(expression)
        display.delete(0, tk.END)
        display.insert(0, str(result))
    except Exception as e:
        display.delete(0, tk.END)
        display.insert(0, "Error")

def button_click(number):
    """Inserts the clicked number or operator into the display."""
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current + str(number))

def clear_display():
    """Clears the display."""
    display.delete(0, tk.END)

def clear_entry():
    """Clears the current entry (CE)."""
    display.delete(display.index(tk.INSERT), tk.END)  

def backspace():
    """Removes the last character from the display."""
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current[:-1])

def change_sign():
    """Changes the sign of the number in the display."""
    current = display.get()
    if current and current[0] == '-':
        display.delete(0, tk.END)
        display.insert(0, current[1:])
    else:
        display.delete(0, tk.END)
        display.insert(0, '-' + current)

def memory_clear():
    """Clears the memory (MC)."""
    global memory
    memory = 0

def memory_recall():
    """Recalls the value from memory (MR)."""
    global memory
    display.delete(0, tk.END)
    display.insert(0, str(memory))

def memory_add():
    """Adds the current value to memory (M+)."""
    global memory
    try:
        memory += float(display.get())
    except:
        display.insert(0, "Error")

def memory_subtract():
    """Subtracts the current value from memory (M-)."""
    global memory
    try:
        memory -= float(display.get())
    except:
        display.insert(0, "Error")

def memory_store():
    """Stores the current value into memory (MS)."""
    global memory
    try:
        memory = float(display.get())
    except:
        display.insert(0, "Error")

def power_of_y():
    """Adds the power operator to the display (M^)."""
    display.insert(tk.END, "^")

def percentage():
    """Calculates the percentage of the current value."""
    try:
        result = float(display.get()) / 100
        display.delete(0, tk.END)
        display.insert(0, str(result))
    except:
        display.delete(0, tk.END)
        display.insert(0, "Error")

def reciprocal():
    """Calculates the reciprocal (1/x)."""
    try:
        result = 1 / float(display.get())
        display.delete(0, tk.END)
        display.insert(0, str(result))
    except:
        display.delete(0, tk.END)
        display.insert(0, "Error")

def square():
    """Calculates the square (x^2)."""
    try:
        result = float(display.get()) ** 2
        display.delete(0, tk.END)
        display.insert(0, str(result))
    except:
        display.delete(0, tk.END)
        display.insert(0, "Error")

def square_root():
    """Calculates the square root (√x)."""
    try:
        result = math.sqrt(float(display.get()))
        display.delete(0, tk.END)
        display.insert(0, str(result))
    except:
        display.delete(0, tk.END)
        display.insert(0, "Error")

def safe_calculate():
    try:
        expression = display.get()
        expression = expression.replace("√", "math.sqrt").replace("^", "**")
        result = ast.literal_eval(expression)
        formatted_result = "{:.10f}".format(result)
        display.delete(0, tk.END)
        display.insert(0, formatted_result)
    except (ValueError, SyntaxError, TypeError, AttributeError) as e:
        display.delete(0, tk.END)
        display.insert(0, "Error")

# Create the main window
root = tk.Tk()
root.title("Pink Calculator")
root.configure(bg="#FCE4EC")

# Create the display
display = tk.Entry(root, width=25, borderwidth=5, font=("Arial", 20), bg="#F8BBD0", fg="#37474F", justify="right")  # Pink display, dark text
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Define button layout (similar to the image)
buttons = [
    ("MC", "MR", "M+", "M-", "MS", "M^"),
    ("%", "CE", "C", "<-"),
    ("1/x", "x^2", "√x", "/"),
    ("7", "8", "9", "*"),
    ("4", "5", "6", "-"),
    ("1", "2", "3", "+"),
    ("+/-", "0", ".", "=")
]

# Create buttons
button_config = {
    "=": {"command": calculate, "padx": 30, "bg": "#F48FB1"},
    "C": {"command": clear_display, "bg": "#F06292"},
    "CE": {"command": clear_entry, "bg": "#F06292"},
    "<-": {"command": backspace, "text":"⌫", "bg": "#F06292"},
    "+/-": {"command": change_sign, "bg": "#F06292"},
    "MC": {"command": memory_clear, "bg": "#F8BBD0"},
    "MR": {"command": memory_recall, "bg": "#F8BBD0"},
    "M+": {"command": memory_add, "bg": "#F8BBD0"},
    "M-": {"command": memory_subtract, "bg": "#F8BBD0"},
    "MS": {"command": memory_store, "bg": "#F8BBD0"},
    "M^": {"command": power_of_y, "bg": "#F8BBD0"},
    "%": {"command": percentage, "bg": "#F8BBD0"},
    "1/x": {"command": reciprocal, "bg": "#F8BBD0"},
    "x^2": {"command": square, "bg": "#F8BBD0"},
    "√x": {"command": square_root, "text":"√", "bg": "#F8BBD0"},
}

row_val = 1
for row in buttons:
    col_val = 0
    for button_text in row:
        config = button_config.get(button_text, {"command": lambda num=button_text: button_click(num), "bg": "#F8BBD0"})
        text = config.get("text", button_text)
        tk.Button(root, text=text, padx=config.get("padx", 20), pady=20, font=("Arial", 16), bg=config["bg"], fg="#37474F" if config["bg"] == "#F8BBD0" else "white", command=config["command"], relief=tk.RAISED, borderwidth=2).grid(row=row_val, column=col_val, sticky="nsew")
        col_val += 1
    row_val += 1

# Configure row and column weights to make buttons expand
for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Start the GUI
root.mainloop()