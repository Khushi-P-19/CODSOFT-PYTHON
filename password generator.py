import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import math
import pyperclip

def calculate_entropy(pwd):
    char_set_size = 0
    if any(c.isupper() for c in pwd): char_set_size += 26
    if any(c.islower() for c in pwd): char_set_size += 26
    if any(c.isdigit() for c in pwd): char_set_size += 10
    if any(c in string.punctuation for c in pwd): char_set_size += len(string.punctuation)
    if char_set_size == 0: return 0
    return len(pwd) * math.log2(char_set_size)

def check_strength(pwd):
    length = len(pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_symbol = any(c in string.punctuation for c in pwd)
    score = sum([has_upper, has_lower, has_digit, has_symbol])
    entropy = calculate_entropy(pwd)
    
    if length >= 16 and score == 4 and entropy >= 80:
        return "Very Strong", "darkgreen", 100
    elif length >= 12 and score == 4 and entropy >= 60:
        return "Strong", "green", 80
    elif length >= 8 and score >= 3 and entropy >= 40:
        return "Moderate", "orange", 60
    elif length >= 6 and score >= 2:
        return "Weak", "red", 40
    else:
        return "Very Weak", "darkred", 20

def generate_password():
    try:
        length = length_var.get()
        if length < 4:
            raise ValueError("Password length must be at least 4.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Password length must be at least 4.")
        return
    chars = ''
    if use_upper.get(): chars += string.ascii_uppercase
    if use_lower.get(): chars += string.ascii_lowercase
    if use_digits.get(): chars += string.digits
    if use_symbols.get(): chars += string.punctuation
    if exclude_ambiguous.get():
        ambiguous = 'l1I0O'
        chars = ''.join(c for c in chars if c not in ambiguous)
    if not chars:
        messagebox.showerror("Invalid Selection", "Please select at least one character set.")
        return
    password = ''.join(random.choice(chars) for _ in range(length))
    generated_password.set(password)
    password_history.append(password)
    update_history_listbox()
    show_strength(password, strength_label, strength_progress)
    if auto_copy.get():
        copy_to_clipboard()

def show_strength(pwd, label, progress):
    strength, color, progress_value = check_strength(pwd)
    label.config(text=f"Strength: {strength} (Entropy: {calculate_entropy(pwd):.2f} bits)", foreground=color)
    progress['value'] = progress_value

def copy_to_clipboard():
    pwd = generated_password.get()
    if not pwd:
        messagebox.showwarning("No Password", "Nothing to copy.")
        return
    pyperclip.copy(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard!")

def check_custom():
    pwd = custom_input.get()
    if not pwd:
        messagebox.showwarning("Input Required", "Please enter a password.")
        return
    show_strength(pwd, custom_strength_label, custom_strength_progress)

def toggle_show_generated():
    generated_entry.config(show='' if show_generated.get() else '*')

def toggle_show_custom():
    custom_entry.config(show='' if show_custom.get() else '*')

def update_length_label(value):
    length_label.config(text=f"Password Length: {int(float(value))}")

def update_history_listbox():
    history_listbox.delete(0, tk.END)
    for pwd in password_history[-5:]:
        history_listbox.insert(tk.END, pwd)

def copy_selected_history():
    selection = history_listbox.curselection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select a password from history.")
        return
    pwd = history_listbox.get(selection[0])
    pyperclip.copy(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# Main window
root = tk.Tk()
root.title("Advanced Password Generator & Strength Checker")
root.geometry("600x800")
root.resizable(True, True)
root.config(bg="#f0f0f0")

# Style
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
style.configure('TButton', font=('Helvetica', 10), padding=5)
style.configure('TCheckbutton', background='#f0f0f0')
style.configure('TScale', background='#f0f0f0')
style.configure('TProgressbar', thickness=20)

# Generator Frame
generator_frame = ttk.Frame(root, padding=10)
generator_frame.pack(fill='both', expand=True)

ttk.Label(generator_frame, text="🔐 Password Generator", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

length_var = tk.IntVar(value=12)
length_label = ttk.Label(generator_frame, text="Password Length: 12")
length_label.grid(row=1, column=0, sticky='w', pady=5)
ttk.Scale(generator_frame, from_=4, to=32, orient='horizontal', variable=length_var, command=update_length_label).grid(row=1, column=1, sticky='ew', pady=5)

use_upper = tk.BooleanVar(value=True)
ttk.Checkbutton(generator_frame, text="Include Uppercase (A-Z)", variable=use_upper).grid(row=2, column=0, columnspan=2, sticky='w', pady=2)

use_lower = tk.BooleanVar(value=True)
ttk.Checkbutton(generator_frame, text="Include Lowercase (a-z)", variable=use_lower).grid(row=3, column=0, columnspan=2, sticky='w', pady=2)

use_digits = tk.BooleanVar(value=True)
ttk.Checkbutton(generator_frame, text="Include Digits (0-9)", variable=use_digits).grid(row=4, column=0, columnspan=2, sticky='w', pady=2)

use_symbols = tk.BooleanVar(value=True)
ttk.Checkbutton(generator_frame, text="Include Symbols (!@# etc.)", variable=use_symbols).grid(row=5, column=0, columnspan=2, sticky='w', pady=2)

exclude_ambiguous = tk.BooleanVar(value=False)
ttk.Checkbutton(generator_frame, text="Exclude Ambiguous Chars (l1I0O)", variable=exclude_ambiguous).grid(row=6, column=0, columnspan=2, sticky='w', pady=2)

auto_copy = tk.BooleanVar(value=False)
ttk.Checkbutton(generator_frame, text="Auto Copy to Clipboard", variable=auto_copy).grid(row=7, column=0, columnspan=2, sticky='w', pady=2)

ttk.Button(generator_frame, text="Generate Password", command=generate_password).grid(row=8, column=0, columnspan=2, pady=10)

generated_password = tk.StringVar()
generated_entry = ttk.Entry(generator_frame, textvariable=generated_password, font=("Consolas", 14), width=40, justify='center', show='*')
generated_entry.grid(row=9, column=0, columnspan=2, pady=5)

show_generated = tk.BooleanVar(value=False)
ttk.Checkbutton(generator_frame, text="Show Password", variable=show_generated, command=toggle_show_generated).grid(row=10, column=0, sticky='w', pady=2)

ttk.Button(generator_frame, text="Copy to Clipboard", command=copy_to_clipboard).grid(row=10, column=1, sticky='e', pady=2)

strength_label = ttk.Label(generator_frame, text="Strength: ", font=("Helvetica", 12, "bold"))
strength_label.grid(row=11, column=0, columnspan=2, pady=5)

strength_progress = ttk.Progressbar(generator_frame, orient='horizontal', length=200, mode='determinate')
strength_progress.grid(row=12, column=0, columnspan=2, pady=5)

# Password History
ttk.Label(generator_frame, text="Password History (Last 5)", font=("Helvetica", 12, "bold")).grid(row=13, column=0, columnspan=2, pady=5)
history_listbox = tk.Listbox(generator_frame, height=5, width=40, font=("Consolas", 10))
history_listbox.grid(row=14, column=0, columnspan=2, pady=5)
ttk.Button(generator_frame, text="Copy Selected", command=copy_selected_history).grid(row=15, column=0, columnspan=2, pady=5)
password_history = []

# Separator
ttk.Separator(root, orient='horizontal').pack(fill='x', pady=10)

# Checker Frame
checker_frame = ttk.Frame(root, padding=10)
checker_frame.pack(fill='both', expand=True)

ttk.Label(checker_frame, text="🔎 Check Your Own Password", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

custom_input = tk.StringVar()
custom_entry = ttk.Entry(checker_frame, textvariable=custom_input, font=("Consolas", 14), width=40, justify='center', show='*')
custom_entry.grid(row=1, column=0, columnspan=2, pady=5)

show_custom = tk.BooleanVar(value=False)
ttk.Checkbutton(checker_frame, text="Show Password", variable=show_custom, command=toggle_show_custom).grid(row=2, column=0, sticky='w', pady=2)

ttk.Button(checker_frame, text="Check Strength", command=check_custom).grid(row=2, column=1, sticky='e', pady=2)

custom_strength_label = ttk.Label(checker_frame, text="Strength: ", font=("Helvetica", 12, "bold"))
custom_strength_label.grid(row=3, column=0, columnspan=2, pady=5)

custom_strength_progress = ttk.Progressbar(checker_frame, orient='horizontal', length=200, mode='determinate')
custom_strength_progress.grid(row=4, column=0, columnspan=2, pady=5)

# Column configure for responsiveness
generator_frame.columnconfigure(1, weight=1)
checker_frame.columnconfigure(1, weight=1)

root.mainloop()
