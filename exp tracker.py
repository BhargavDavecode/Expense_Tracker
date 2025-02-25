import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
def setup_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL,
                        category TEXT,
                        description TEXT,
                        date TEXT)''')
    conn.commit()
    conn.close()

setup_db()

# Function to add expense
def add_expense():
    amount = entry_amount.get()
    category = combo_category.get()
    description = entry_description.get()
    date = entry_date.get()
    
    if not amount or not category or not date:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return
    
    try:
        amount = float(amount)
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                       (amount, category, description, date))
        conn.commit()
        conn.close()
        entry_amount.delete(0, tk.END)
        entry_description.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        messagebox.showinfo("Success", "Expense added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.")

# Function to view expenses
def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    records = cursor.fetchall()
    conn.close()
    
    text_output.delete(1.0, tk.END)
    for row in records:
        text_output.insert(tk.END, f"{row[1]} - {row[2]}: {row[3]} ({row[4]})\n")

# Function to view expense summary
def view_summary():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    summary = cursor.fetchall()
    conn.close()
    
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, "Expense Summary:\n")
    for category, total in summary:
        text_output.insert(tk.END, f"{category}: {total}\n")

# GUI setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x500")

# Widgets
label_amount = tk.Label(root, text="Amount:")
label_amount.pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

label_category = tk.Label(root, text="Category:")
label_category.pack()
combo_category = ttk.Combobox(root, values=["Food", "Transport", "Entertainment", "Bills", "Other"])
combo_category.pack()

label_description = tk.Label(root, text="Description:")
label_description.pack()
entry_description = tk.Entry(root)
entry_description.pack()

label_date = tk.Label(root, text="Date (YYYY-MM-DD):")
label_date.pack()
entry_date = tk.Entry(root)
entry_date.pack()

button_add = tk.Button(root, text="Add Expense", command=add_expense)
button_add.pack()

button_view = tk.Button(root, text="View Expenses", command=view_expenses)
button_view.pack()

button_summary = tk.Button(root, text="View Summary", command=view_summary)
button_summary.pack()

text_output = tk.Text(root, height=10, width=50)
text_output.pack()

root.mainloop()
