import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from playsound import playsound
import threading

current_expression = ""
history = []

root = tk.Tk()
root.title("Калькулятор")
root.geometry("380x600")
root.resizable(False, False)
root.configure(bg="#000000")

BUTTON_FONT = ("Helvetica", 18, "bold")
DISPLAY_FONT = ("Helvetica", 24)

BG = "#000000"
FG = "#FFFFFF"
ENTRY_BG = "#000000"
ENTRY_FG = "#FFFFFF"
BTN_NUM_BG = "#333333"
BTN_OP_BG = "#FF9F0A"
BTN_TEXT = "#FFFFFF"
BTN_CLEAR_BG = "#A6A6A6"
HISTORY_BG = "#111111"
HISTORY_FG = "#00FF9D"

try:
    clock_image = Image.open("image.png")
    clock_image = clock_image.resize((32, 32), Image.Resampling.LANCZOS)
    clock_photo = ImageTk.PhotoImage(clock_image)
except Exception as e:
    print(f"Не удалось загрузить image.png: {e}")
    clock_photo = None

def play_sound():
    try:
        threading.Thread(target=lambda: playsound("mixkit-modern-technology-select-3124.wav"), daemon=True).start()
    except Exception as e:
        print(f"Звук не проигран: {e}")

def with_sound(func):
    return lambda: [play_sound(), func()]

display_frame = tk.Frame(root, bg=BG)
display_frame.pack(pady=30)

entry = tk.Label(
    display_frame,
    text="0",
    font=DISPLAY_FONT,
    bg=ENTRY_BG,
    fg=ENTRY_FG,
    anchor="e",
    width=12
)
entry.pack()

def update_display():
    entry.config(text=current_expression if current_expression else "0")

def add_to_expression(char):
    global current_expression
    if current_expression == "0" and char not in "+-*/.":
        current_expression = ""
    current_expression += str(char)
    update_display()

def clear():
    global current_expression
    current_expression = ""
    update_display()

def delete_last():
    global current_expression
    current_expression = current_expression[:-1]
    update_display()

def calculate():
    global current_expression
    try:
        result = eval(current_expression)
        
        if isinstance(result, float):
            result = round(result, 5)
        
        result_str = str(result)
        if result_str.endswith('.0'):
            result_str = result_str[:-2]
        
        history_entry = f"{current_expression} = {result}"
        history.append(history_entry)
        
        current_expression = result_str
        update_display()
    except Exception:
        current_expression = "Ошибка"
        update_display()

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("История вычислений")
    history_window.geometry("400x500")
    history_window.configure(bg=BG)

    title_label = tk.Label(
        history_window,
        text="История",
        font=("Helvetica", 16),
        bg=BG,
        fg=FG
    )
    title_label.pack(pady=10)

    history_text = tk.Text(
        history_window,
        font=("Courier", 12),
        bg=HISTORY_BG,
        fg=HISTORY_FG,
        width=50,
        height=20,
        wrap="word"
    )
    history_text.pack(padx=20, pady=10, fill="both", expand=True)

    for line in history:
        history_text.insert(tk.END, f"{line}\n")
    history_text.see(tk.END)

    def save_history():
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Сохранить историю"
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    for line in history:
                        f.write(f"{line}\n")
                messagebox.showinfo("Успех", f"История сохранена:\n{path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    save_btn = tk.Button(
        history_window,
        text="Сохранить как...",
        font=("Helvetica", 12),
        bg="#A6A6A6",
        fg="black",
        command=save_history
    )
    save_btn.pack(pady=5)

    close_btn = tk.Button(
        history_window,
        text="Закрыть",
        font=("Helvetica", 12),
        bg="#FF9F0A",
        fg="white",
        command=history_window.destroy
    )
    close_btn.pack(pady=10)

history_btn = tk.Button(
    root,
    image=clock_photo,
    bg=BG,
    bd=0,
    relief="flat",
    command=with_sound(show_history)
)
if clock_photo:
    history_btn.image = clock_photo
history_btn.pack(pady=5)

buttons_frame = tk.Frame(root, bg=BG)
buttons_frame.pack(pady=10)

button_config = [
    ['C', '⌫', '%', '÷'],
    ['7', '8', '9', '×'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['0', '.', '=']
]

for row_idx, row in enumerate(button_config):
    for col_idx, label in enumerate(row):
        if label == "C":
            command = with_sound(clear)
            bg_color = BTN_CLEAR_BG
            fg_color = "#000000"
        elif label == "⌫":
            command = with_sound(delete_last)
            bg_color = BTN_CLEAR_BG
            fg_color = "#000000"
        elif label == "%":
            command = lambda: [play_sound(), add_to_expression("/100")]
            bg_color = BTN_CLEAR_BG
            fg_color = "#000000"
        elif label == "÷":
            command = lambda: [play_sound(), add_to_expression("/")]
            bg_color = BTN_OP_BG
            fg_color = BTN_TEXT
        elif label == "×":
            command = lambda: [play_sound(), add_to_expression("*")]
            bg_color = BTN_OP_BG
            fg_color = BTN_TEXT
        elif label == "-":
            command = lambda: [play_sound(), add_to_expression("-")]
            bg_color = BTN_OP_BG
            fg_color = BTN_TEXT
        elif label == "+":
            command = lambda: [play_sound(), add_to_expression("+")]
            bg_color = BTN_OP_BG
            fg_color = BTN_TEXT
        elif label == "=":
            command = with_sound(calculate)
            bg_color = BTN_OP_BG
            fg_color = BTN_TEXT
        elif label == ".":
            command = lambda: [play_sound(), add_to_expression(".")]
            bg_color = BTN_NUM_BG
            fg_color = BTN_TEXT
        else:
            command = lambda b=label: [play_sound(), add_to_expression(b)]
            bg_color = BTN_NUM_BG
            fg_color = BTN_TEXT

        button = tk.Button(
            buttons_frame,
            text=label,
            font=BUTTON_FONT,
            bg=bg_color,
            fg=fg_color,
            bd=0,
            width=11 if label == "0" else 5,
            height=2,
            command=command
        )

        if label == "0":
            button.grid(row=row_idx, column=col_idx, columnspan=2, padx=4, pady=4, sticky="ew")
        else:
            offset = 1 if label in [".", "="] and row_idx == 4 else 0
            button.grid(row=row_idx, column=col_idx + offset, padx=4, pady=4, sticky="ew")


for i in range(4):
    buttons_frame.grid_columnconfigure(i, weight=1)

root.mainloop()