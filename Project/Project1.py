"""
Inventory Management System (Complete)

Features:
- SQLite DB (inventory.db) with tables: products, sales.
- Ensures `subcategory` column exists (adds it if missing).
- GUI with Tkinter:
    * Add Product (Name, Category, Subcategory, Price, Stock)
    * View Products (shows ID, Name, Category, Subcategory, Price, Stock)
    * Update Product (load existing by ID, edit fields, save)
    * Remove Product (by ID)
    * Sell Product (by ID + quantity -> reduces stock, records sale)
    * Category Chart (bar)
    * Subcategory Chart (pie)
    * Exit
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import matplotlib.pyplot as plt

DB_FILE = "inventory.db"

# -------------------- DATABASE SETUP --------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Create base products table (without subcategory may exist on older runs)
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price REAL,
            stock INTEGER
        )
    """)

    # If subcategory column missing, add it safely
    c.execute("PRAGMA table_info(products)")
    columns = [col[1] for col in c.fetchall()]
    if "subcategory" not in columns:
        try:
            c.execute("ALTER TABLE products ADD COLUMN subcategory TEXT")
        except Exception:
            # If alter fails for some reason, ignore (table might already have it)
            pass

    # Create sales table
    c.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            total REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# -------------------- UTIL --------------------
def get_db_connection():
    return sqlite3.connect(DB_FILE)

# -------------------- GUI FUNCTIONS --------------------
def add_product_window(parent):
    win = Toplevel(parent)
    win.title("Add Product")
    win.resizable(False, False)

    frm = ttk.Frame(win, padding=10)
    frm.grid(row=0, column=0)

    ttk.Label(frm, text="Name:").grid(row=0, column=0, sticky="e")
    name_e = ttk.Entry(frm, width=30); name_e.grid(row=0, column=1, pady=3)

    ttk.Label(frm, text="Category:").grid(row=1, column=0, sticky="e")
    category_e = ttk.Entry(frm, width=30); category_e.grid(row=1, column=1, pady=3)

    ttk.Label(frm, text="Subcategory:").grid(row=2, column=0, sticky="e")
    subcat_e = ttk.Entry(frm, width=30); subcat_e.grid(row=2, column=1, pady=3)

    ttk.Label(frm, text="Price:").grid(row=3, column=0, sticky="e")
    price_e = ttk.Entry(frm, width=30); price_e.grid(row=3, column=1, pady=3)

    ttk.Label(frm, text="Stock:").grid(row=4, column=0, sticky="e")
    stock_e = ttk.Entry(frm, width=30); stock_e.grid(row=4, column=1, pady=3)

    def save():
        name = name_e.get().strip()
        category = category_e.get().strip()
        subcat = subcat_e.get().strip()
        try:
            price = float(price_e.get())
            stock = int(stock_e.get())
        except ValueError:
            messagebox.showerror("Input error", "Price must be number and Stock must be integer.")
            return
        if not name or not category:
            messagebox.showwarning("Missing", "Please enter Name and Category.")
            return

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO products(name, category, subcategory, price, stock) VALUES(?,?,?,?,?)",
                    (name, category, subcat, price, stock))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Product '{name}' added.")
        win.destroy()

    ttk.Button(frm, text="Save", command=save).grid(row=5, column=0, columnspan=2, pady=8)

def view_products_window(parent):
    win = Toplevel(parent)
    win.title("All Products")
    win.geometry("820x400")

    cols = ("ID", "Name", "Category", "Subcategory", "Price", "Stock")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor="center")
    tree.pack(fill="both", expand=True, padx=8, pady=8)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, subcategory, price, stock FROM products ORDER BY id")
    for row in cur.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

    # Add a refresh button in case DB changed
    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, category, subcategory, price, stock FROM products ORDER BY id")
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    btn_frame = ttk.Frame(win)
    btn_frame.pack(fill="x", pady=4)
    ttk.Button(btn_frame, text="Refresh", command=refresh).pack(side="left", padx=6)
    ttk.Button(btn_frame, text="Close", command=win.destroy).pack(side="right", padx=6)

def delete_product_window(parent):
    win = Toplevel(parent)
    win.title("Delete Product")
    win.resizable(False, False)
    frm = ttk.Frame(win, padding=10); frm.grid(row=0, column=0)

    ttk.Label(frm, text="Product ID:").grid(row=0, column=0, sticky="e")
    id_e = ttk.Entry(frm, width=20); id_e.grid(row=0, column=1, pady=6)

    def delete():
        try:
            pid = int(id_e.get())
        except ValueError:
            messagebox.showerror("Input error", "Enter valid integer ID.")
            return
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM products WHERE id=?", (pid,))
        r = cur.fetchone()
        if not r:
            messagebox.showerror("Not found", "Product ID not found.")
            conn.close()
            return
        if not messagebox.askyesno("Confirm", f"Delete product ID={pid} ({r[0]})?"):
            conn.close()
            return
        cur.execute("DELETE FROM products WHERE id=?", (pid,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", f"Product ID {pid} deleted.")
        win.destroy()

    ttk.Button(frm, text="Delete", command=delete).grid(row=1, column=0, columnspan=2, pady=6)

def update_product_window(parent):
    win = Toplevel(parent)
    win.title("Update Product")
    win.resizable(False, False)
    frm = ttk.Frame(win, padding=10); frm.grid(row=0, column=0)

    ttk.Label(frm, text="Product ID:").grid(row=0, column=0, sticky="e")
    id_e = ttk.Entry(frm, width=20); id_e.grid(row=0, column=1, pady=4)

    # Fields to update
    ttk.Label(frm, text="Name:").grid(row=1, column=0, sticky="e")
    name_e = ttk.Entry(frm, width=30); name_e.grid(row=1, column=1, pady=3)

    ttk.Label(frm, text="Category:").grid(row=2, column=0, sticky="e")
    category_e = ttk.Entry(frm, width=30); category_e.grid(row=2, column=1, pady=3)

    ttk.Label(frm, text="Subcategory:").grid(row=3, column=0, sticky="e")
    subcat_e = ttk.Entry(frm, width=30); subcat_e.grid(row=3, column=1, pady=3)

    ttk.Label(frm, text="Price:").grid(row=4, column=0, sticky="e")
    price_e = ttk.Entry(frm, width=30); price_e.grid(row=4, column=1, pady=3)

    ttk.Label(frm, text="Stock:").grid(row=5, column=0, sticky="e")
    stock_e = ttk.Entry(frm, width=30); stock_e.grid(row=5, column=1, pady=3)

    def load():
        try:
            pid = int(id_e.get())
        except ValueError:
            messagebox.showerror("Input error", "Enter valid integer ID.")
            return
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, category, subcategory, price, stock FROM products WHERE id=?", (pid,))
        r = cur.fetchone()
        conn.close()
        if not r:
            messagebox.showerror("Not found", "Product ID not found.")
            return
        name_e.delete(0, tk.END); name_e.insert(0, r[0])
        category_e.delete(0, tk.END); category_e.insert(0, r[1])
        subcat_e.delete(0, tk.END); subcat_e.insert(0, r[2] if r[2] is not None else "")
        price_e.delete(0, tk.END); price_e.insert(0, str(r[3]))
        stock_e.delete(0, tk.END); stock_e.insert(0, str(r[4]))

    def save_update():
        try:
            pid = int(id_e.get())
        except ValueError:
            messagebox.showerror("Input error", "Enter valid integer ID.")
            return
        name = name_e.get().strip(); category = category_e.get().strip()
        subcat = subcat_e.get().strip()
        try:
            price = float(price_e.get()); stock = int(stock_e.get())
        except ValueError:
            messagebox.showerror("Input error", "Price must be number and Stock integer.")
            return
        if not name or not category:
            messagebox.showwarning("Missing", "Name and Category required.")
            return
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE products SET name=?, category=?, subcategory=?, price=?, stock=? WHERE id=?",
                    (name, category, subcat, price, stock, pid))
        conn.commit()
        conn.close()
        messagebox.showinfo("Updated", f"Product ID {pid} updated.")
        win.destroy()

    btn_frame = ttk.Frame(frm)
    btn_frame.grid(row=6, column=0, columnspan=2, pady=6)
    ttk.Button(btn_frame, text="Load", command=load).pack(side="left", padx=6)
    ttk.Button(btn_frame, text="Save Update", command=save_update).pack(side="left", padx=6)

def sell_product_window(parent):
    win = Toplevel(parent)
    win.title("Sell Product")
    win.resizable(False, False)
    frm = ttk.Frame(win, padding=10); frm.grid(row=0, column=0)

    ttk.Label(frm, text="Product ID:").grid(row=0, column=0, sticky="e")
    id_e = ttk.Entry(frm, width=20); id_e.grid(row=0, column=1, pady=4)

    ttk.Label(frm, text="Quantity:").grid(row=1, column=0, sticky="e")
    qty_e = ttk.Entry(frm, width=20); qty_e.grid(row=1, column=1, pady=4)

    def process_sale():
        try:
            pid = int(id_e.get()); qty = int(qty_e.get())
        except ValueError:
            messagebox.showerror("Input error", "Enter valid integer ID and Quantity.")
            return
        if qty <= 0:
            messagebox.showerror("Input error", "Quantity must be > 0.")
            return
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, stock, price FROM products WHERE id=?", (pid,))
        r = cur.fetchone()
        if not r:
            conn.close()
            messagebox.showerror("Not found", "Product ID not found.")
            return
        name, stock, price = r
        if stock < qty:
            conn.close()
            messagebox.showwarning("Stock error", f"Only {stock} units available.")
            return
        new_stock = stock - qty
        total = qty * price
        cur.execute("UPDATE products SET stock=? WHERE id=?", (new_stock, pid))
        cur.execute("INSERT INTO sales(product_id, quantity, total) VALUES(?,?,?)", (pid, qty, total))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sold", f"Sold {qty} of '{name}'. Total = {total}")
        win.destroy()

    ttk.Button(frm, text="Sell", command=process_sale).grid(row=2, column=0, columnspan=2, pady=6)

# -------------------- VISUALIZATIONS --------------------
def show_category_chart(parent):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT category, SUM(stock) FROM products GROUP BY category")
    data = cur.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("No data", "No products to visualize.")
        return

    categories = [d[0] if d[0] else "Uncategorized" for d in data]
    stocks = [d[1] if d[1] else 0 for d in data]

    plt.figure(figsize=(8,5))
    bars = plt.bar(categories, stocks)
    plt.xlabel("Category")
    plt.ylabel("Total Stock")
    plt.title("Category-wise Stock")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    # color bars lightly based on value (no explicit color argument required, but okay)
    plt.show()

def show_subcategory_chart(parent):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT category || ' - ' || subcategory AS label, SUM(stock) FROM products GROUP BY category, subcategory")
    data = cur.fetchall()
    conn.close()

    # Filter out empty subcategory labels (if subcategory is null or empty then label contains ' - ' or 'None')
    filtered = [(lbl if lbl and lbl.strip() and not lbl.endswith(" - ") and not lbl.endswith(" - None") else "Uncategorized", s) for lbl, s in data]
    labels = [f"{l}" for l, s in filtered]
    stocks = [s for l, s in filtered]

    if not labels:
        messagebox.showinfo("No data", "No subcategory data to visualize.")
        return

    plt.figure(figsize=(7,7))
    plt.pie(stocks, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Subcategory Stock Share")
    plt.tight_layout()
    plt.show()

# -------------------- MAIN APPLICATION --------------------
def main():
    init_db()
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("420x520")
    root.resizable(False, False)

    title = ttk.Label(root, text="Inventory Management System", font=("Arial", 16))
    title.pack(pady=10)

    # Buttons
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=6)

    ttk.Button(btn_frame, text="➕ Add Product", width=30, command=lambda: add_product_window(root)).pack(pady=6)
    ttk.Button(btn_frame, text="📋 View Products", width=30, command=lambda: view_products_window(root)).pack(pady=6)
    ttk.Button(btn_frame, text="✏️ Update Product", width=30, command=lambda: update_product_window(root)).pack(pady=6)
    ttk.Button(btn_frame, text="🗑️ Remove Product", width=30, command=lambda: delete_product_window(root)).pack(pady=6)
    ttk.Button(btn_frame, text="💰 Sell Product", width=30, command=lambda: sell_product_window(root)).pack(pady=6)

    ttk.Separator(root, orient="horizontal").pack(fill="x", pady=10)

    ttk.Label(root, text="--- Visualization ---", font=("Arial", 12)).pack()
    ttk.Button(root, text="📊 Category Chart", width=30, command=lambda: show_category_chart(root)).pack(pady=6)
    ttk.Button(root, text="📊 Subcategory Chart (Pie)", width=30, command=lambda: show_subcategory_chart(root)).pack(pady=6)

    ttk.Separator(root, orient="horizontal").pack(fill="x", pady=10)

    ttk.Button(root, text="🚪 Exit", width=30, command=root.destroy).pack(pady=12)

    root.mainloop()

if __name__ == "__main__":
    main()
