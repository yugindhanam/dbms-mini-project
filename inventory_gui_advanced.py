import tkinter as tk
from tkinter import ttk, messagebox
import oracledb

# Database Connection
connection = oracledb.connect(
    user="system",
    password="Yugin@1263",
    dsn="localhost/XEPDB1"
)
cursor = connection.cursor()
cursor.execute("SELECT user FROM dual")
print("Connected User:", cursor.fetchone())

# Main Window
window = tk.Tk()
window.title("EMart Inventory System")
window.geometry("900x550")
window.configure(bg="#ecf0f1")

# ---------- Title ----------
title = tk.Label(window,
                 text="EMart Inventory Management System",
                 font=("Segoe UI", 22, "bold"),
                 bg="#34495e",
                 fg="white",
                 pady=10)
title.pack(fill="x")

# ---------- Main Frame ----------
main_frame = tk.Frame(window, bg="#ecf0f1")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# ---------- Left Frame (Form) ----------
form_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge")
form_frame.pack(side="left", fill="y", padx=10)

tk.Label(form_frame, text="Product Details",
         font=("Segoe UI", 14, "bold"),
         bg="white").grid(row=0, columnspan=2, pady=10)

# Entry Fields
labels = ["Product ID", "Product Name", "Category", "Price", "Quantity", "Supplier ID"]
entries = []

for i, text in enumerate(labels):
    tk.Label(form_frame, text=text, bg="white",
             font=("Segoe UI", 10)).grid(row=i+1, column=0, padx=10, pady=8, sticky="w")

    entry = tk.Entry(form_frame, width=25)
    entry.grid(row=i+1, column=1, padx=10)
    entries.append(entry)

id_entry, name_entry, category_entry, price_entry, qty_entry, supplier_entry = entries

# ---------- Functions ----------
def clear_fields():
    for entry in entries:
        entry.delete(0, tk.END)

def validate_inputs():
    if not id_entry.get() or not name_entry.get():
        messagebox.showwarning("Validation Error", "ID and Name are required!")
        return False
    return True

def add_product():
    if not validate_inputs():
        return

    try:
        cursor.execute("""
        INSERT INTO product
        (product_id, product_name, category, price, quantity, supplier_id)
        VALUES (:1,:2,:3,:4,:5,:6)
        """, (
            id_entry.get(),
            name_entry.get(),
            category_entry.get(),
            price_entry.get(),
            qty_entry.get(),
            supplier_entry.get()
        ))

        connection.commit()
        messagebox.showinfo("Success", "Product Added")
        show_products()
        clear_fields()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_product():
    pid = id_entry.get()

    if not pid:
        messagebox.showwarning("Error", "Enter Product ID")
        return

    try:
        cursor.execute("DELETE FROM product WHERE product_id=:1", (pid,))
        connection.commit()

        messagebox.showinfo("Success", "Product Deleted")
        show_products()
        clear_fields()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_products():
    for row in table.get_children():
        table.delete(row)

    cursor.execute("SELECT * FROM system.product")
    rows = cursor.fetchall()

    for r in rows:
        table.insert("", tk.END, values=r)

# ---------- Buttons ----------
btn_frame = tk.Frame(form_frame, bg="white")
btn_frame.grid(row=8, columnspan=2, pady=15)

tk.Button(btn_frame, text="Add",
          bg="#2ecc71", fg="white", width=12,
          command=add_product).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Delete",
          bg="#e74c3c", fg="white", width=12,
          command=delete_product).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Clear",
          bg="#95a5a6", fg="white", width=12,
          command=clear_fields).grid(row=1, column=0, padx=5, pady=5)

tk.Button(btn_frame, text="Refresh",
          bg="#3498db", fg="white", width=12,
          command=show_products).grid(row=1, column=1, padx=5, pady=5)

# ---------- Right Frame (Table) ----------
table_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge")
table_frame.pack(side="right", fill="both", expand=True)

columns = ("ID", "Name", "Category", "Price", "Quantity", "Supplier")

table = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=100)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscroll=scrollbar.set)

table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Load Data
show_products()

window.mainloop()