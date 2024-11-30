import os
import pyperclip
from tkinter import Tk, filedialog, Button, Text, Label, Frame, Scrollbar, RIGHT, Y, BOTTOM, BOTH, END

def generate_commit_message(file_name):
    if file_name.endswith(".component.ts"):
        name_partial = file_name.split(".component.ts")[0]
        return f"Add {file_name} to be an Angular component for the {name_partial} element in the Angular application"
    elif file_name.endswith(".component.html"):
        name_partial = file_name.split(".component.html")[0]
        return f"Add {file_name} to be a template for the {name_partial} element in the Angular application"
    elif file_name.endswith("-style.component.scss"):
        name_partial = file_name.split("-style.component.scss")[0]
        return f"Add {file_name} to style the {name_partial} element in the Angular application"
    else:
        return None

def copy_to_clipboard(text):
    pyperclip.copy(text)

def display_commit_messages(selected_files):
    display_window = Tk()
    display_window.title("Generated Commit Messages")
    display_window.option_add("*Font", "Arial 14")
    display_window.geometry("900x900")
    frame = Frame(display_window)
    frame.pack(fill=BOTH, expand=True)
    scrollbar = Scrollbar(frame, orient="vertical")
    scrollbar.pack(side=RIGHT, fill=Y)
    for file_path in selected_files:
        file_name = os.path.basename(file_path)
        commit_message = generate_commit_message(file_name)
        if commit_message:
            label = Label(display_window, text=f"File: {file_name}",
                          font=("Arial", 16, "bold"))
            label.pack(anchor="w", padx=20, pady=(15, 5))
            text_box = Text(display_window, height=3, width=90, wrap="word",
                            padx=10, pady=10)
            text_box.insert(END, commit_message)
            text_box.config(state="disabled")
            text_box.pack(padx=20, pady=5)
            copy_button = Button(
                display_window,
                text="Copy",
                command=lambda message=commit_message: copy_to_clipboard(message),
            )
            copy_button.pack(padx=20, pady=(0, 15))
    bottom_frame = Frame(display_window)
    bottom_frame.pack(side=BOTTOM, pady=20)
    select_new_button = Button(bottom_frame, text="Select New Files",
                               command=lambda: [display_window.destroy(), select_files()])
    select_new_button.pack(side="left", padx=10)
    cancel_button = Button(bottom_frame, text="Cancel",
                           command=display_window.destroy)
    cancel_button.pack(side="right", padx=10)
    display_window.mainloop()

def select_files():
    root = Tk()
    root.withdraw()
    selected_files = filedialog.askopenfilenames(
        title="Select Files",
        filetypes=[
            ("Angular Component Files", "*.component.ts;*.component.html;*.component.scss"),
            ("All Files", "*.*"),
        ],
    )
    if not selected_files:
        print("No files selected.")
        return
    display_commit_messages(selected_files)

if __name__ == "__main__":
    select_files()