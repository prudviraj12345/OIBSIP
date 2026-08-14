import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


# ============================================================
# DATABASE
# ============================================================

DB_NAME = "bmi_records.db"


def create_database():
    """Create the BMI database and table if they do not exist."""

    try:
        connection = sqlite3.connect(DB_NAME)

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not create database:\n{error}"
        )


# ============================================================
# BMI CALCULATION
# ============================================================

def calculate_bmi(weight, height):
    """Calculate BMI."""

    return weight / (height ** 2)


def get_category(bmi):
    """Return the standard BMI category."""

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


# ============================================================
# COLOR
# ============================================================

def get_category_color(category):

    if category == "Underweight":
        return "orange"

    elif category == "Normal":
        return "green"

    elif category == "Overweight":
        return "orange"

    else:
        return "red"


# ============================================================
# SAVE RECORD
# ============================================================

def save_record(name, weight, height, bmi, category):

    try:

        connection = sqlite3.connect(DB_NAME)

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO bmi_records
            (name, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            weight,
            height,
            bmi,
            category,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        connection.commit()
        connection.close()

        return True

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not save BMI record:\n{error}"
        )

        return False


# ============================================================
# CALCULATE BUTTON
# ============================================================

def calculate():

    name = name_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    # Name validation
    if not name:

        messagebox.showerror(
            "Input Error",
            "Please enter a user's name."
        )

        return

    # Weight validation
    try:

        weight = float(weight_text)

    except ValueError:

        messagebox.showerror(
            "Input Error",
            "Weight must be a numeric value."
        )

        return

    # Height validation
    try:

        height = float(height_text)

    except ValueError:

        messagebox.showerror(
            "Input Error",
            "Height must be a numeric value."
        )

        return

    # Negative / zero validation
    if weight <= 0:

        messagebox.showerror(
            "Input Error",
            "Weight must be greater than zero."
        )

        return

    if height <= 0:

        messagebox.showerror(
            "Input Error",
            "Height must be greater than zero."
        )

        return

    # BMI calculation
    bmi = calculate_bmi(
        weight,
        height
    )

    category = get_category(
        bmi
    )

    # Display result
    result_label.config(
        text=f"BMI: {bmi:.2f}\nCategory: {category}",
        foreground=get_category_color(category)
    )

    # Save database record
    save_record(
        name,
        weight,
        height,
        bmi,
        category
    )


# ============================================================
# SHOW HISTORY
# ============================================================

def show_history():

    name = name_entry.get().strip()

    if not name:

        messagebox.showerror(
            "Input Error",
            "Enter a user's name first."
        )

        return

    try:

        connection = sqlite3.connect(DB_NAME)

        cursor = connection.cursor()

        cursor.execute("""
            SELECT date, weight, height, bmi, category
            FROM bmi_records
            WHERE name = ?
            ORDER BY date ASC
        """, (name,))

        records = cursor.fetchall()

        connection.close()

        if not records:

            messagebox.showinfo(
                "History",
                f"No BMI records found for {name}."
            )

            return

        history_window = tk.Toplevel(root)

        history_window.title(
            f"BMI History - {name}"
        )

        history_window.geometry(
            "650x400"
        )

        columns = (
            "Date",
            "Weight",
            "Height",
            "BMI",
            "Category"
        )

        tree = ttk.Treeview(
            history_window,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=120
            )

        for record in records:

            tree.insert(
                "",
                tk.END,
                values=(
                    record[0],
                    record[1],
                    record[2],
                    f"{record[3]:.2f}",
                    record[4]
                )
            )

        tree.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not read BMI history:\n{error}"
        )


# ============================================================
# SHOW GRAPH
# ============================================================

def show_graph():

    name = name_entry.get().strip()

    if not name:

        messagebox.showerror(
            "Input Error",
            "Enter a user's name first."
        )

        return

    try:

        connection = sqlite3.connect(DB_NAME)

        cursor = connection.cursor()

        cursor.execute("""
            SELECT date, bmi
            FROM bmi_records
            WHERE name = ?
            ORDER BY date ASC
        """, (name,))

        records = cursor.fetchall()

        connection.close()

        if not records:

            messagebox.showinfo(
                "BMI Trend",
                f"No BMI records found for {name}."
            )

            return

        dates = [
            record[0]
            for record in records
        ]

        bmi_values = [
            record[1]
            for record in records
        ]

        plt.figure(
            figsize=(9, 5)
        )

        plt.plot(
            dates,
            bmi_values,
            marker="o"
        )

        plt.title(
            f"BMI Trend - {name}"
        )

        plt.xlabel(
            "Date"
        )

        plt.ylabel(
            "BMI"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.grid(
            True
        )

        plt.tight_layout()

        plt.show()

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not read BMI data:\n{error}"
        )

    except Exception as error:

        messagebox.showerror(
            "Graph Error",
            f"Could not display graph:\n{error}"
        )


# ============================================================
# CLEAR INPUTS
# ============================================================

def clear_fields():

    name_entry.delete(
        0,
        tk.END
    )

    weight_entry.delete(
        0,
        tk.END
    )

    height_entry.delete(
        0,
        tk.END
    )

    result_label.config(
        text="BMI: --\nCategory: --",
        foreground="black"
    )


# ============================================================
# GUI
# ============================================================

create_database()

root = tk.Tk()

root.title(
    "BMI Calculator"
)

root.geometry(
    "520x600"
)

root.resizable(
    False,
    False
)


# Title

title_label = tk.Label(
    root,
    text="BMI CALCULATOR",
    font=("Arial", 24, "bold")
)

title_label.pack(
    pady=20
)


subtitle_label = tk.Label(
    root,
    text="Track BMI for multiple users",
    font=("Arial", 11)
)

subtitle_label.pack(
    pady=5
)


# Main frame

frame = tk.Frame(
    root,
    padx=30,
    pady=20
)

frame.pack()


# Name

tk.Label(
    frame,
    text="User Name:",
    font=("Arial", 12)
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

name_entry = tk.Entry(
    frame,
    width=25,
    font=("Arial", 12)
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Weight

tk.Label(
    frame,
    text="Weight (kg):",
    font=("Arial", 12)
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

weight_entry = tk.Entry(
    frame,
    width=25,
    font=("Arial", 12)
)

weight_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Height

tk.Label(
    frame,
    text="Height (m):",
    font=("Arial", 12)
).grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

height_entry = tk.Entry(
    frame,
    width=25,
    font=("Arial", 12)
)

height_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


# Calculate button

calculate_button = tk.Button(
    root,
    text="Calculate BMI",
    command=calculate,
    width=20,
    font=("Arial", 12, "bold")
)

calculate_button.pack(
    pady=15
)


# Result

result_label = tk.Label(
    root,
    text="BMI: --\nCategory: --",
    font=("Arial", 18, "bold")
)

result_label.pack(
    pady=15
)


# History button

history_button = tk.Button(
    root,
    text="View History",
    command=show_history,
    width=20,
    font=("Arial", 11)
)

history_button.pack(
    pady=5
)


# Graph button

graph_button = tk.Button(
    root,
    text="View BMI Trend",
    command=show_graph,
    width=20,
    font=("Arial", 11)
)

graph_button.pack(
    pady=5
)


# Clear button

clear_button = tk.Button(
    root,
    text="Clear",
    command=clear_fields,
    width=20,
    font=("Arial", 11)
)

clear_button.pack(
    pady=5
)


# Footer

footer = tk.Label(
    root,
    text="BMI = Weight (kg) / Height² (m)",
    font=("Arial", 9)
)

footer.pack(
    pady=15
)


root.mainloop()