# Author: Harshal Joshi
# Purpose: To create a GUI application for Byte and Bolt Tech Hire
# Date: 29 - 5 - 2026 (first edited)
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import os
import datetime
from PIL import Image, ImageTk

# Main window setup
root = tk.Tk()
root.title("Byte & Bolt Tech Hire")
root.geometry("500x600")  # Slightly taller to accommodate the single-window layout

# Persistent storage configurations
filename = "savefile.txt"
item_list = [
    ["ACC 1 Keyboard", 20], ["ACC 1 Mouse", 15], ["Execute PC", 60], ["ARD4T 672a Laptop", 32], ["33Gi Headset", 17],
    ["ACT 2 Keyboard", 25], ["ACT 2 Mouse", 25], ["Muscle PC", 70], ["TR4G0N 884b Laptop", 38], ["36I8 Headset", 27],
    ["ANe 3 Keyboard", 15], ["ANe 3 Mouse", 10], ["Bright PC", 45], ["CRYPT 438c Laptop", 26], ["33rT Headset", 10],
    ["ARf 4 Keyboard", 22], ["ARf 4 Mouse", 17], ["Torrential PC", 65], ["TAB1TH 553d Laptop", 35], ["25yR Headset", 22]
]

# Tracking states
checkbox_vars = []
selected_items = []
entry_name_new_order = None
entry_name_return = None
entry_quantity = None

# --- NAVIGATION FLOW CONTROLLERS ---

def main_menu_build():
    """Brings up the starting screen."""
    new_order_menu_frame.pack_forget()
    return_order_menu_frame.pack_forget()
    main_menu_frame.pack(padx=20, pady=20, fill="both", expand=True)

def new_order_menu_build():
    # Switches the window space over to the order construction module.
    # Reset tracking arrays for a clean user entry state
    global checkbox_vars, selected_items
    checkbox_vars.clear()
    selected_items.clear()
    if entry_name_new_order is not None:
        entry_name_new_order.delete(0, tk.END)
    if entry_quantity is not None:
        entry_quantity.delete(0, tk.END)
    
    # Rebuild item checklist inside the scrollable container
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
        
    for i, item_data in enumerate(item_list):
        var = tk.IntVar()
        checkbox_vars.append(var)
        chk = tk.Checkbutton(
            scrollable_frame, 
            text=f"{item_data[0]} (${item_data[1]})", 
            variable=var, 
            bg="white", 
            anchor='w', 
            command=lambda i=i: process_item_data(i)
        )
        chk.pack(fill='x', anchor='w', pady=2, padx=5)

    main_menu_frame.pack_forget()
    return_order_menu_frame.pack_forget()
    new_order_menu_frame.pack(padx=20, pady=20, fill="both", expand=True)

def return_order_menu_build():
    """Switches the view over to the product tracking return system."""
    main_menu_frame.pack_forget()
    new_order_menu_frame.pack_forget()
    return_order_menu_frame.pack(padx=20, pady=20, fill="both", expand=True)


# --- DATA LOGIC CONSTRUCTORS ---

def process_item_data(index):
    """Tracks checklist manipulations in real time."""
    item_name = item_list[index][0]
    if checkbox_vars[index].get() == 1:
        if item_name not in selected_items:
            selected_items.append(item_name)
    else:
        if item_name in selected_items:
            selected_items.remove(item_name)

def save_order_action():
    """Validates inputs and saves data directly to flat text files."""
    if entry_name_new_order is None:
        messagebox.showerror("Error", "The new order form is not ready yet.")
        return

    name_a = str(entry_name_new_order.get()).strip()
    qty = str(entry_quantity.get()).strip()
    receipt_number = str(generate_receipt_number()).strip()
    
    if name_a == "":
        messagebox.showerror("Error", "Please enter your name.")
        return
        
    if not selected_items:
        messagebox.showerror("Error", "Please select at least one item.")
        return
        
    if qty == "" or not qty.isdigit() or int(qty) <= 0:
        messagebox.showerror("Error", "Please enter a valid numeric quantity.")
        return

    try:
        with open(filename, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            items_ordered = ", ".join(selected_items)
            f.write(f"Date: {timestamp} | Customer: {name_a} | Items: {items_ordered} | Qty: {qty} | Receipt Number: {receipt_number}\n")
        
        messagebox.showinfo("Success", "Order saved successfully!")
        main_menu_build()  # Route user back to home panel on success
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {str(e)}")

def show_order_action():
    """Reads transactional customer logs out loud via native OS alerts."""
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        messagebox.showerror("No Data", "No files or records found.")
        return
    
    with open(filename, "r") as f:
        data = f.read().strip()

    if data == "":
        messagebox.showerror("No Data", "Empty File.")
    else:
        messagebox.showinfo("Data", data)


def return_order_action():
    # Return process - involves deleting a record from the savefile based on receipt number and/or name - needs to be integrated with search order
    name_a = str(entry_name_return.get()).strip()
    receipt_number = str(entry_receipt.get()).strip()

    if name_a == "" and receipt_number == "":
        messagebox.showerror("Error", "Please enter a customer name or receipt number.")
        return

    try:
        with open(filename, "w") as f:
            messagebox.showinfo("Success", "Return processed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not process return: {str(e)}")


# Frame 1: Home Screen Layout Setup
main_menu_frame = tk.Frame(root, bg="#dbdee2", borderwidth=10, relief="ridge")
tk.Label(main_menu_frame, text="Welcome to Byte & Bolt!", font=("Bahnschrift", 18, "bold"), bg="#929292").pack(pady=20)

tk.Button(main_menu_frame, text="New Order Page", bg="#635dff", fg="white", command=new_order_menu_build, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Show Existing Orders", bg="#635dff", fg="white", command=show_order_action, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Return Order Page", bg="#635dff", fg="white", command=return_order_menu_build, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Exit Application", bg="#e81313", fg="white", command=root.destroy, width=25).pack(pady=20)


# Frame 2: New Order Screen Layout Setup
new_order_menu_frame = tk.Frame(root, bg="#fff6d6", borderwidth=10, relief="ridge")
new_order_menu_frame.rowconfigure(1, weight=1)
new_order_menu_frame.columnconfigure(0, weight=1)
new_order_menu_frame.columnconfigure(1, weight=1)
new_order_menu_frame.rowconfigure(2, weight=0)

tk.Label(new_order_menu_frame, text="Create New Hire Order", font=("Garamond", 14, "bold"), bg="#eddea7").grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

left_side = tk.Frame(new_order_menu_frame, bg="#F1F3F5")
left_side.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
left_side.columnconfigure(0, weight=1)

right_side = tk.Frame(new_order_menu_frame, bg="#F1F3F5")
right_side.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
right_side.columnconfigure(0, weight=1)
right_side.rowconfigure(1, weight=1)

# Customer metadata forms
tk.Label(left_side, text="Customer Name:", bg="#eddea7").grid(row=0, column=0, sticky="w", pady=2, padx=5)
entry_name_new_order = tk.Entry(left_side)
entry_name_new_order.grid(row=1, column=0, sticky="ew", pady=2, padx=5)

tk.Label(left_side, text="Quantity Wanted:", bg="#eddea7").grid(row=2, column=0, sticky="w", pady=2, padx=5)
entry_quantity = ttk.Combobox(left_side, values=[str(i) for i in range(1, 21)])
entry_quantity.grid(row=3, column=0, sticky="ew", pady=2, padx=5)

# Random receipt generator
def generate_receipt_number():
    return f"R{random.randint(0, 9999):04d}"

tk.Label(right_side, text=f"Receipt Number: {generate_receipt_number()}", bg="#eddea7").grid(row=0, column=0, sticky="w", pady=5, padx=5)

# Dynamic scrollable container block for equipment listings
canvas_container = tk.Frame(right_side, bd=1, relief="sunken")
canvas_container.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)

canvas = tk.Canvas(canvas_container, bg="white", height=150)
scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Execution navigation triggers inside Order panel
button_frame = tk.Frame(new_order_menu_frame, bg="#fff6d6")
button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

tk.Button(button_frame, text="Commit Order Records", bg="#635dff", fg="white", command=save_order_action).grid(row=0, column=0, sticky="ew", padx=10)
tk.Button(button_frame, text="Cancel & Back", bg="#e81313", fg="white", command=main_menu_build).grid(row=0, column=1, sticky="ew", padx=10)


# Frame 3: Return Order Screen Layout Setup
return_order_menu_frame = tk.Frame(root, bg="#d4c893", borderwidth=10, relief="ridge")
tk.Label(return_order_menu_frame, text="Equipment Return Portal", font=("Garamond", 14, "bold"), bg="#AFA273").pack(pady=10)

tk.Label(return_order_menu_frame, text="Customer Name:", bg="#AFA273").pack()
entry_name_return = tk.Entry(return_order_menu_frame)
entry_name_return.pack(pady=2)

tk.Label(return_order_menu_frame, text="Receipt Number", bg= "#AFA273").pack()
entry_receipt = tk.Entry(return_order_menu_frame)
entry_receipt.pack(pady=2)


# Functional return components can be expanded directly down here
tk.Button(return_order_menu_frame, text="Show Existing Orders & Search Orders", bg="#635dff", fg="white", command=show_order_action).pack(pady=5)
tk.Button(return_order_menu_frame, text="Return 1 Order", bg = "#635dff", fg="white", command=return_order_action).pack(pady=5)
tk.Button(return_order_menu_frame, text="Return to Main Menu", bg="#e81313", fg="white", command=main_menu_build).pack(pady=5)



# Run layout generator initializer sequence
main_menu_build()
root.mainloop()
