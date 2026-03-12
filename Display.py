import tkinter as tk
from tkinter import messagebox

# Button labels
BUTTONS = [
    "Option A",
    "Option B",
    "Option C",
    "Option D",
    "Option E"
]

selected = set()

def toggle(name, btn):
    if name in selected:
        selected.remove(name)
        btn.config(relief="raised", bg="SystemButtonFace")
    else:
        selected.add(name)
        btn.config(relief="sunken", bg="lightblue")
    update_list()

def update_list():
    listbox.delete(0, tk.END)
    for item in sorted(selected):
        listbox.insert(tk.END, item)

def save_record():
    name = name_entry.get().strip()
    email = email_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Please enter a record name.")
        return

    if not email:
        messagebox.showerror("Error", "Please enter an email.")
        return

    if not selected:
        messagebox.showerror("Error", "Select at least one option.")
        return

    line = ",".join([name, email] + list(selected))

    with open("records.txt", "a") as f:
        f.write(line + "\n")

    messagebox.showinfo("Saved", "Record saved!")

    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    selected.clear()
    update_list()

    for btn in buttons:
        btn.config(relief="raised", bg="SystemButtonFace")

# Window
root = tk.Tk()
root.title("Record Creator")
root.geometry("600x420")

# Record name
tk.Label(root, text="Record Name:").pack(anchor="w", padx=10, pady=5)
name_entry = tk.Entry(root, width=40)
name_entry.pack(anchor="w", padx=10)

# Email field
tk.Label(root, text="Email:").pack(anchor="w", padx=10, pady=5)
email_entry = tk.Entry(root, width=40)
email_entry.pack(anchor="w", padx=10)

# Main frame
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Left side buttons
button_frame = tk.Frame(frame)
button_frame.pack(side="left")

buttons = []
for label in BUTTONS:
    b = tk.Button(button_frame, text=label, width=15)
    b.config(command=lambda l=label, btn=b: toggle(l, btn))
    b.pack(pady=5)
    buttons.append(b)

# Right side list
list_frame = tk.Frame(frame)
list_frame.pack(side="right", fill="y")

tk.Label(list_frame, text="Selected:").pack()

listbox = tk.Listbox(list_frame, width=25)
listbox.pack()

# Save button
save_btn = tk.Button(root, text="Save", command=save_record, width=10)
save_btn.pack(side="right", padx=10, pady=10)

root.mainloop()