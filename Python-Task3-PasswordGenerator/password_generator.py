import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


# ============================================================
# PASSWORD HISTORY
# ============================================================

password_history = []


# ============================================================
# CHARACTER SETS
# ============================================================

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
NUMBERS = string.digits
SYMBOLS = string.punctuation

AMBIGUOUS = "0O1lI"


# ============================================================
# PASSWORD STRENGTH
# ============================================================

def get_strength(length, character_count):
    """Calculate password strength."""

    if length >= 16 and character_count >= 4:
        return "Strong"

    elif length >= 12 and character_count >= 3:
        return "Medium"

    else:
        return "Weak"


# ============================================================
# GENERATE PASSWORD
# ============================================================

def generate_password():

    try:
        length = int(length_var.get())

    except ValueError:

        messagebox.showerror(
            "Invalid Length",
            "Please enter a valid password length."
        )

        return

    # Minimum length
    if length < 8:

        messagebox.showerror(
            "Invalid Length",
            "Password length must be at least 8 characters."
        )

        return

    # Selected character types
    selected_sets = []

    if lowercase_var.get():
        selected_sets.append(LOWERCASE)

    if uppercase_var.get():
        selected_sets.append(UPPERCASE)

    if numbers_var.get():
        selected_sets.append(NUMBERS)

    if symbols_var.get():
        selected_sets.append(SYMBOLS)

    # At least 2 types required
    if len(selected_sets) < 2:

        messagebox.showerror(
            "Character Selection",
            "Please select at least two character types."
        )

        return

    # Exclude ambiguous characters
    if ambiguous_var.get():

        selected_sets = [
            "".join(
                character
                for character in character_set
                if character not in AMBIGUOUS
            )
            for character_set in selected_sets
        ]

    # Check that sets are still usable
    selected_sets = [
        character_set
        for character_set in selected_sets
        if character_set
    ]

    if len(selected_sets) < 2:

        messagebox.showerror(
            "Character Selection",
            "The selected character types contain no usable characters."
        )

        return

    # Make sure at least one character from every
    # selected type is included.
    password_characters = [
        secrets.choice(character_set)
        for character_set in selected_sets
    ]

    # Combined character set
    combined_set = "".join(selected_sets)

    # Fill remaining positions
    remaining = length - len(password_characters)

    for _ in range(remaining):

        password_characters.append(
            secrets.choice(combined_set)
        )

    # Secure shuffle using secrets
    shuffled_password = []

    while password_characters:

        index = secrets.randbelow(
            len(password_characters)
        )

        shuffled_password.append(
            password_characters.pop(index)
        )

    password = "".join(shuffled_password)

    # Display password
    password_var.set(password)

    # Automatically copy to clipboard
    try:

        pyperclip.copy(password)

        clipboard_label.config(
            text="✓ Password copied to clipboard"
        )

    except Exception:

        clipboard_label.config(
            text="Could not copy automatically"
        )

    # Strength
    strength = get_strength(
        length,
        len(selected_sets)
    )

    strength_label.config(
        text=f"Strength: {strength}"
    )

    if strength == "Strong":
        strength_label.config(
            foreground="green"
        )

    elif strength == "Medium":
        strength_label.config(
            foreground="orange"
        )

    else:
        strength_label.config(
            foreground="red"
        )

    # Session history
    password_history.insert(
        0,
        password
    )

    # Keep only the latest 5
    del password_history[5:]

    update_history()


# ============================================================
# COPY PASSWORD
# ============================================================

def copy_password():

    password = password_var.get()

    if not password:

        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )

        return

    try:

        pyperclip.copy(password)

        clipboard_label.config(
            text="✓ Password copied to clipboard"
        )

    except Exception as error:

        messagebox.showerror(
            "Clipboard Error",
            f"Could not copy password:\n{error}"
        )


# ============================================================
# UPDATE HISTORY
# ============================================================

def update_history():

    history_listbox.delete(
        0,
        tk.END
    )

    for index, password in enumerate(
        password_history,
        start=1
    ):

        history_listbox.insert(
            tk.END,
            f"{index}. {password}"
        )


# ============================================================
# CLEAR HISTORY
# ============================================================

def clear_history():

    password_history.clear()

    update_history()


# ============================================================
# GUI
# ============================================================

root = tk.Tk()

root.title(
    "Secure Password Generator"
)

root.geometry(
    "620x720"
)

root.resizable(
    False,
    False
)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    root,
    text="SECURE PASSWORD GENERATOR",
    font=("Arial", 22, "bold")
)

title_label.pack(
    pady=20
)


subtitle_label = tk.Label(
    root,
    text="Generate strong passwords using Python secrets",
    font=("Arial", 10)
)

subtitle_label.pack(
    pady=2
)


# ============================================================
# MAIN FRAME
# ============================================================

main_frame = tk.Frame(
    root,
    padx=30,
    pady=10
)

main_frame.pack()


# ============================================================
# PASSWORD LENGTH
# ============================================================

tk.Label(
    main_frame,
    text="Password Length:",
    font=("Arial", 12)
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=10
)

length_var = tk.IntVar(
    value=16
)

length_spinbox = tk.Spinbox(
    main_frame,
    from_=8,
    to=128,
    textvariable=length_var,
    width=10,
    font=("Arial", 12)
)

length_spinbox.grid(
    row=0,
    column=1,
    sticky="w",
    pady=10
)


# ============================================================
# CHARACTER TYPES
# ============================================================

tk.Label(
    main_frame,
    text="Character Types:",
    font=("Arial", 12, "bold")
).grid(
    row=1,
    column=0,
    columnspan=2,
    sticky="w",
    pady=(15, 5)
)


lowercase_var = tk.BooleanVar(
    value=True
)

uppercase_var = tk.BooleanVar(
    value=True
)

numbers_var = tk.BooleanVar(
    value=True
)

symbols_var = tk.BooleanVar(
    value=True
)


tk.Checkbutton(
    main_frame,
    text="Lowercase letters (a-z)",
    variable=lowercase_var,
    font=("Arial", 11)
).grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="w"
)


tk.Checkbutton(
    main_frame,
    text="Uppercase letters (A-Z)",
    variable=uppercase_var,
    font=("Arial", 11)
).grid(
    row=3,
    column=0,
    columnspan=2,
    sticky="w"
)


tk.Checkbutton(
    main_frame,
    text="Numbers (0-9)",
    variable=numbers_var,
    font=("Arial", 11)
).grid(
    row=4,
    column=0,
    columnspan=2,
    sticky="w"
)


tk.Checkbutton(
    main_frame,
    text="Symbols (!@#$...)",
    variable=symbols_var,
    font=("Arial", 11)
).grid(
    row=5,
    column=0,
    columnspan=2,
    sticky="w"
)


# ============================================================
# AMBIGUOUS CHARACTERS
# ============================================================

ambiguous_var = tk.BooleanVar(
    value=False
)

tk.Checkbutton(
    main_frame,
    text="Exclude ambiguous characters (0, O, 1, l, I)",
    variable=ambiguous_var,
    font=("Arial", 11)
).grid(
    row=6,
    column=0,
    columnspan=2,
    sticky="w",
    pady=10
)


# ============================================================
# GENERATE BUTTON
# ============================================================

generate_button = tk.Button(
    root,
    text="Generate Secure Password",
    command=generate_password,
    width=28,
    font=("Arial", 12, "bold")
)

generate_button.pack(
    pady=15
)


# ============================================================
# PASSWORD DISPLAY
# ============================================================

password_var = tk.StringVar()

password_entry = tk.Entry(
    root,
    textvariable=password_var,
    width=45,
    font=("Consolas", 14),
    justify="center"
)

password_entry.pack(
    pady=10
)


# ============================================================
# STRENGTH
# ============================================================

strength_label = tk.Label(
    root,
    text="Strength: --",
    font=("Arial", 14, "bold")
)

strength_label.pack(
    pady=5
)


# ============================================================
# CLIPBOARD STATUS
# ============================================================

clipboard_label = tk.Label(
    root,
    text="",
    font=("Arial", 10)
)

clipboard_label.pack(
    pady=3
)


# ============================================================
# COPY BUTTON
# ============================================================

copy_button = tk.Button(
    root,
    text="Copy to Clipboard",
    command=copy_password,
    width=22,
    font=("Arial", 11)
)

copy_button.pack(
    pady=5
)


# ============================================================
# HISTORY
# ============================================================

history_title = tk.Label(
    root,
    text="Last 5 Generated Passwords (Current Session)",
    font=("Arial", 12, "bold")
)

history_title.pack(
    pady=(20, 5)
)


history_listbox = tk.Listbox(
    root,
    width=55,
    height=6,
    font=("Consolas", 10)
)

history_listbox.pack(
    pady=5
)


# ============================================================
# CLEAR HISTORY
# ============================================================

clear_button = tk.Button(
    root,
    text="Clear History",
    command=clear_history,
    width=18
)

clear_button.pack(
    pady=5
)


# ============================================================
# SECURITY NOTE
# ============================================================

security_label = tk.Label(
    root,
    text="Passwords are generated using Python's cryptographically secure secrets module.",
    font=("Arial", 9)
)

security_label.pack(
    pady=15
)


root.mainloop()