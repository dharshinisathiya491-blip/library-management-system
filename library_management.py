
import tkinter as tk
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT
)
""")
con.commit()

def insert():
    try:
        cur.execute("INSERT INTO books VALUES (?, ?, ?)",
                    (int(e1.get()), e2.get(), e3.get()))
        con.commit()
        messagebox.showinfo("Success", "Book added")
        view()
    except (ValueError, sqlite3.Error) as err:
        messagebox.showerror("Error", str(err))

def view():
    output.delete("1.0", tk.END)
    cur.execute("SELECT * FROM books")
    for row in cur.fetchall():
        output.insert(tk.END, str(row) + "\n")

def search():
    output.delete("1.0", tk.END)
    cur.execute("SELECT * FROM books WHERE id=?", (e1.get(),))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            output.insert(tk.END, str(row) + "\n")
    else:
        output.insert(tk.END, "Book not found")

def delete():
    cur.execute("DELETE FROM books WHERE id=?", (e1.get(),))
    con.commit()
    messagebox.showinfo("Success", "Book deleted")
    view()

root = tk.Tk()
root.title("Library Management System")
root.geometry("400x400")

tk.Label(root, text="Library Management System",
         font=("Arial", 15, "bold")).pack(pady=10)

tk.Label(root, text="Book ID").pack()
e1 = tk.Entry(root)
e1.pack()

tk.Label(root, text="Book Title").pack()
e2 = tk.Entry(root)
e2.pack()

tk.Label(root, text="Author").pack()
e3 = tk.Entry(root)
e3.pack()

tk.Button(root, text="Insert Book", command=insert).pack(pady=3)
tk.Button(root, text="View Books", command=view).pack(pady=3)
tk.Button(root, text="Search Book", command=search).pack(pady=3)
tk.Button(root, text="Delete Book", command=delete).pack(pady=3)

output = tk.Text(root, height=8, width=40)
output.pack(pady=10)

view()
root.mainloop()
con.close()
