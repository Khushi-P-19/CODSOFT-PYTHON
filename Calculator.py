import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        self.root.configure(bg="#2d2d2d")

        self.current = ""
        self.previous = ""
        self.op = ""
        self.memory = 0
        self.mode = 'rad'
        self.mode_button = None

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.entry_var, font=('Arial', 22), bd=10, insertwidth=2,
                              width=18, borderwidth=4, relief='sunken', justify='right')
        self.entry.grid(row=0, column=0, columnspan=5, padx=10, pady=20)

        self.create_buttons()

        self.root.bind('<Key>', self.key_press)

    def create_buttons(self):
        buttons = [
            ('C', 1, 0, self.clear, "#d9534f"),
            ('←', 1, 1, self.backspace, "#f0ad4e"),
            ('%', 1, 2, self.percent, "#5bc0de"),
            ('/', 1, 3, lambda: self.operation('/'), "#0275d8"),
            ('sin', 1, 4, self.sin_func, "#5bc0de"),
            ('7', 2, 0, lambda: self.append('7')),
            ('8', 2, 1, lambda: self.append('8')),
            ('9', 2, 2, lambda: self.append('9')),
            ('*', 2, 3, lambda: self.operation('*'), "#0275d8"),
            ('cos', 2, 4, self.cos_func, "#5bc0de"),
            ('4', 3, 0, lambda: self.append('4')),
            ('5', 3, 1, lambda: self.append('5')),
            ('6', 3, 2, lambda: self.append('6')),
            ('-', 3, 3, lambda: self.operation('-'), "#0275d8"),
            ('tan', 3, 4, self.tan_func, "#5bc0de"),
            ('1', 4, 0, lambda: self.append('1')),
            ('2', 4, 1, lambda: self.append('2')),
            ('3', 4, 2, lambda: self.append('3')),
            ('+', 4, 3, lambda: self.operation('+'), "#0275d8"),
            ('log', 4, 4, self.log_func, "#5bc0de"),
            ('0', 5, 0, lambda: self.append('0')),
            ('.', 5, 1, lambda: self.append('.')),
            ('=', 5, 2, self.calculate, "#5cb85c", 2),
            ('sqrt', 5, 4, self.sqrt_func, "#5bc0de"),
            ('**', 6, 0, lambda: self.operation('**'), "#5bc0de"),
            ('exp', 6, 1, self.exp_func, "#5bc0de"),
            ('ln', 6, 2, self.ln_func, "#5bc0de"),
            ('pi', 6, 3, self.pi_func, "#5bc0de"),
            ('e', 6, 4, self.e_func, "#5bc0de"),
            ('1/x', 7, 0, self.one_over, "#5bc0de"),
            ('M+', 7, 1, self.memory_add, "#f0ad4e"),
            ('M-', 7, 2, self.memory_sub, "#f0ad4e"),
            ('MR', 7, 3, self.memory_recall, "#f0ad4e"),
            ('MC', 7, 4, self.memory_clear, "#f0ad4e"),
            ('MS', 8, 0, self.memory_store, "#f0ad4e"),
            ('RAD', 8, 1, self.toggle_mode, "#f0ad4e", 4),
        ]

        for btn_info in buttons:
            text, row, col, command, *rest = btn_info
            color = rest[0] if rest else "#f7f7f7"
            span = rest[1] if len(rest) > 1 else 1
            btn = tk.Button(
                self.root, text=text, padx=15, pady=15, bd=4, fg="black", bg=color,
                font=('Arial', 16), command=command
            )
            btn.grid(row=row, column=col, columnspan=span, padx=5, pady=5, sticky='we')
            if text == 'RAD':
                self.mode_button = btn

    def append(self, symbol):
        if symbol == '.' and '.' in self.current:
            return
        self.current += symbol
        self.entry_var.set(self.current)

    def operation(self, op):
        if self.current:
            if self.previous and self.op:
                self.calculate()
            self.previous = self.current if not self.previous else self.previous
            self.current = ""
            self.op = op
        self.entry_var.set(self.previous + " " + op + " ")

    def calculate(self):
        if not self.current or not self.op or not self.previous:
            return
        try:
            prev = float(self.previous)
            curr = float(self.current)
            if self.op == '+':
                result = prev + curr
            elif self.op == '-':
                result = prev - curr
            elif self.op == '*':
                result = prev * curr
            elif self.op == '/':
                if curr == 0:
                    raise ZeroDivisionError
                result = prev / curr
            elif self.op == '**':
                result = prev ** curr
            self.entry_var.set(str(result))
            self.previous = str(result)
            self.current = ""
            self.op = ""
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero is not allowed.")
            self.clear()
        except:
            messagebox.showerror("Error", "Invalid expression.")
            self.clear()

    def clear(self):
        self.current = ""
        self.previous = ""
        self.op = ""
        self.entry_var.set("")

    def backspace(self):
        self.current = self.current[:-1]
        self.entry_var.set(self.current)

    def percent(self):
        if not self.current:
            return
        try:
            curr = float(self.current)
            if self.op in ['+', '-']:
                curr = float(self.previous) * (curr / 100)
            else:
                curr = curr / 100
            self.current = str(curr)
            self.entry_var.set(self.current)
        except:
            messagebox.showerror("Error", "Invalid percent operation.")

    def toggle_mode(self):
        if self.mode == 'rad':
            self.mode = 'deg'
            self.mode_button.config(text='DEG')
        else:
            self.mode = 'rad'
            self.mode_button.config(text='RAD')

    def get_trig(self, func, value):
        try:
            val = float(value)
            if self.mode == 'deg':
                val = math.radians(val)
            return func(val)
        except:
            raise ValueError

    def sin_func(self):
        if self.current:
            try:
                result = self.get_trig(math.sin, self.current)
                self.current = str(result)
                self.entry_var.set(self.current)
            except:
                messagebox.showerror("Error", "Invalid input for sin.")

    def cos_func(self):
        if self.current:
            try:
                result = self.get_trig(math.cos, self.current)
                self.current = str(result)
                self.entry_var.set(self.current)
            except:
                messagebox.showerror("Error", "Invalid input for cos.")

    def tan_func(self):
        if self.current:
            try:
                result = self.get_trig(math.tan, self.current)
                self.current = str(result)
                self.entry_var.set(self.current)
            except:
                messagebox.showerror("Error", "Invalid input for tan.")

    def log_func(self):
        if self.current:
            try:
                val = float(self.current)
                if val <= 0:
                    raise ValueError
                result = math.log10(val)
                self.current = str(result)
                self.entry_var.set(self.current)
            except:
                messagebox.showerror("Error", "Invalid input for log.")

    def ln_func(self):
        if self.current:
            try:
                val = float(self.current)
                if val <= 0:
                    raise ValueError
                result = math.log(val)
                self.current = str(result)
                self.entry_var.set(self.current)
            except:
                messagebox.showerror("Error", "Invalid input for ln.")

    def exp_func(self):
        if self.current:
            try:
                val = float(self.current)
                result = math.exp(val)
                self.current = str(result)
                self.entry_var.set(self.current)
            except:
                messagebox.showerror("Error", "Invalid input for exp.")

    def sqrt_func(self):
        if self.current:
            try:
                val = float(self.current)
                if val < 0:
                    raise ValueError
                result = math.sqrt(val)
                self.current = str(result)
                self.entry_var.set(self.current)
            except:
                messagebox.showerror("Error", "Invalid input for sqrt.")

    def one_over(self):
        if self.current:
            try:
                val = float(self.current)
                if val == 0:
                    raise ZeroDivisionError
                result = 1 / val
                self.current = str(result)
                self.entry_var.set(self.current)
            except ZeroDivisionError:
                messagebox.showerror("Error", "Division by zero is not allowed.")
            except:
                messagebox.showerror("Error", "Invalid input for 1/x.")

    def pi_func(self):
        self.current = str(math.pi)
        self.entry_var.set(self.current)

    def e_func(self):
        self.current = str(math.e)
        self.entry_var.set(self.current)

    def memory_add(self):
        if self.current:
            try:
                self.memory += float(self.current)
            except:
                pass

    def memory_sub(self):
        if self.current:
            try:
                self.memory -= float(self.current)
            except:
                pass

    def memory_recall(self):
        self.current = str(self.memory)
        self.entry_var.set(self.current)

    def memory_clear(self):
        self.memory = 0

    def memory_store(self):
        if self.current:
            try:
                self.memory = float(self.current)
            except:
                pass

    def key_press(self, event):
        if event.char.isdigit() or event.char == '.':
            self.append(event.char)
        elif event.char in '+-*/^':
            self.operation(event.char if event.char != '^' else '**')
        elif event.char == '%':
            self.percent()
        elif event.keysym == 'Return' or event.char == '=':
            self.calculate()
        elif event.keysym == 'BackSpace':
            self.backspace()
        elif event.keysym == 'Escape':
            self.clear()

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
