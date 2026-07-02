# Author: Harshal Joshi
# Purpose: To create a GUI application for Byte and Bolt Tech Hire
# Date: 29 - 5 - 2026 (first edited)
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import os
from datetime import date, datetime, timedelta
from pathlib import Path

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
order_date = None
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
    # Tracks checklist manipulations in real time.
    item_name = item_list[index][0]
    if checkbox_vars[index].get() == 1:
        if item_name not in selected_items:
            selected_items.append(item_name)
    else:
        if item_name in selected_items:
            selected_items.remove(item_name)

def save_order_action():
    # Validates inputs and saves data directly to flat text files
    if entry_name_new_order is None:
        messagebox.showerror("Error", "The new order form is not ready yet.")
        return

    name_a = str(entry_name_new_order.get()).strip()
    qty = str(entry_quantity.get()).strip()
    receipt_number = str(generate_receipt_number()).strip()
    
    if name_a == "":
        messagebox.showerror("Error", "Please enter your name.")
        return

    if any(char.isdigit() for char in name_a):
        messagebox.showerror("Error", "Name cannot contain numbers.")
        return
        
    if not selected_items:
        messagebox.showerror("Error", "Please select at least one item.")
        return
        
    if qty == "" or not qty.isdigit():
        messagebox.showerror("Error", "Please enter a valid numeric quantity.")
        return
    if int(qty) < 1 or int(qty) > 20:
        messagebox.showerror("Error", "Please enter a quantity between 1 and 20.")
        return
    try:
        order_date = date.today().strftime("%d-%m-%Y")
        order_time = datetime.now().strftime("%H:%M:%S")
        follow_up_date = (date.today() + timedelta(days=7)).strftime("%d-%m-%Y")
        items_ordered = ", ".join(selected_items)

        with open(filename, "a") as f:
            f.write(f"Date Ordered: {order_date} {order_time} | Follow-Up By: {follow_up_date} | Customer: {name_a} | Items: {items_ordered} | Qty: {qty} | Receipt Number: {receipt_number}\n")
        
        messagebox.showinfo("Success", f"Order saved successfully!\nFollow-up by: {follow_up_date}")
        main_menu_build()  # Route user back to home panel on success
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {str(e)}")

def show_order_action():
    # Reads transactional customer logs out loud via native OS alerts.
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
    # Finds one matching order by customer name or receipt number and removes that one record.
    name_a = str(entry_name_return.get()).strip()
    receipt_number = str(entry_receipt.get()).strip()

    if name_a == "" and receipt_number == "":
        messagebox.showerror("Error", "Please enter a customer name or receipt number.")
        return

    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        messagebox.showerror("Error", "No orders found to return.")
        return

    try:
        with open(filename, "r") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]

        matching_lines = []
        for line in lines:
            line_lower = line.lower()
            if receipt_number and receipt_number.lower() in line_lower:
                matching_lines.append(line)
            elif name_a and f"customer: {name_a}".lower() in line_lower:
                matching_lines.append(line)

        if not matching_lines:
            messagebox.showerror("Error", "No matching order found.")
            return

        if len(matching_lines) > 1:
            messagebox.showwarning("Multiple Matches", "More than one order matched. Please use the receipt number for an exact result.")
            return

        matched_order = matching_lines[0]
        messagebox.showinfo("Order Found", f"Returning this order:\n{matched_order}")

        remaining_lines = [line for line in lines if line != matched_order]
        with open(filename, "w") as f:
            if remaining_lines:
                f.write("\n".join(remaining_lines) + "\n")

        messagebox.showinfo("Success", "One order returned successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not process return: {str(e)}")


# Frame 1: Home Screen Layout Setup
main_menu_frame = tk.Frame(root, bg="#aeb0b1", borderwidth=10, relief="ridge")
tk.Label(main_menu_frame, text="Welcome to Byte & Bolt!", font=("Garamond", 18, "bold"), bg="#cdd4d4").pack(pady=20)

tk.Button(main_menu_frame, text="New Order Page", bg="#635dff", fg="white", command=new_order_menu_build, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Show Existing Orders", bg="#635dff", fg="white", command=show_order_action, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Return Order Page", bg="#635dff", fg="white", command=return_order_menu_build, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Exit Application", bg="#e81313", fg="white", command=root.destroy, width=25).pack(pady=20)


file_path = Path(__file__).resolve().parent.parent / "Images" / "Logo.png"
if file_path.exists():
    try:
        png_image = tk.PhotoImage(file=str(file_path))
        try:
            image_to_use = png_image.subsample(9, 9)
        except Exception:
            image_to_use = png_image
        image_frame = tk.Frame(main_menu_frame)
        image_label = tk.Label(image_frame, image=image_to_use)
        image_frame.place(x=350, y=10)
        image_frame.configure(bg="#edf5ff")
        image_label.pack()
    except Exception as e:
        print(f"Warning: could not load image: {e}")
else:
    print(f"Warning: image not found at {file_path}")
# Frame 2: New Order Screen Layout Setup
new_order_menu_frame = tk.Frame(root, bg="#9e9e9e", borderwidth=10, relief="ridge")
tk.Label(new_order_menu_frame, text="Create New Hire Order", font=("Garamond", 14, "bold"), bg="#a7dded").pack(pady=5)

# Customer metadata forms
tk.Label(new_order_menu_frame, text="Customer Name:", bg="#9aa0a7").pack()
entry_name_new_order = tk.Entry(new_order_menu_frame)
entry_name_new_order.pack(pady=2)

tk.Label(new_order_menu_frame, text="Quantity Wanted:", bg="#9aa0a7").pack()
entry_quantity = ttk.Combobox(new_order_menu_frame,values=[str(i) for i in range(1, 21)])
entry_quantity.pack(pady=2)

current_date = date.today().strftime("%d-%m-%Y")
follow_up_date = (date.today() + timedelta(days=7)).strftime("%d-%m-%Y")
tk.Label(new_order_menu_frame, text=f"Order Date: {current_date}", bg="#a7adaf").pack(pady=2)
tk.Label(new_order_menu_frame, text=f"Follow-Up By: {follow_up_date}", bg="#a7adaf").pack(pady=2)

# Random receipt generator
def generate_receipt_number():
    return f"R{random.randint(0000, 9999)}"

tk.Label(new_order_menu_frame, text=f"Receipt Number: {generate_receipt_number()}", bg="#a7dded").pack(pady=5)

# Dynamic scrollable container block for equipment listings
canvas_container = tk.Frame(new_order_menu_frame, bd=1, relief="sunken")
canvas_container.pack(fill="both", expand=True, pady=5)

canvas = tk.Canvas(canvas_container, bg="white", height=150)
scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Execution navigation triggers inside Order panel
tk.Button(new_order_menu_frame, text="Commit Order Records", bg="#635dff", fg="white", command=save_order_action).pack(side="left", padx=10, pady=5, expand=True, fill="x")
tk.Button(new_order_menu_frame, text="Cancel & Back", bg="#e81313", fg="white", command=main_menu_build).pack(side="right", padx=10, pady=5, expand=True, fill="x")


# Frame 3: Return Order Screen Layout Setup
return_order_menu_frame = tk.Frame(root, bg="#707a7a", borderwidth=10, relief="ridge")
tk.Label(return_order_menu_frame, text="Equipment Return Portal", font=("Garamond", 14, "bold"), bg="#B6B6B6").pack(pady=10)

tk.Label(return_order_menu_frame, text="Customer Name:", bg="#BDBCBC").pack()
entry_name_return = tk.Entry(return_order_menu_frame)
entry_name_return.pack(pady=2)

tk.Label(return_order_menu_frame, text="Receipt Number", bg= "#BDBCBC").pack()
entry_receipt = tk.Entry(return_order_menu_frame)
entry_receipt.pack(pady=2)


# Functional return components can be expanded directly down here
tk.Button(return_order_menu_frame, text="Show Existing Orders & Search Orders", bg="#635dff", fg="white", command=show_order_action).pack(pady=5)
tk.Button(return_order_menu_frame, text="Return 1 Order", bg = "#635dff", fg="white", command=return_order_action).pack(pady=5)
tk.Button(return_order_menu_frame, text="Return to Main Menu", bg="#e81313", fg="white", command=main_menu_build).pack(pady=5)



# Run layout generator initializer sequence
main_menu_build()
root.mainloop()
