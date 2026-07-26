# Author: Harshal Joshi
# Purpose: To create a GUI application for Byte and Bolt Tech Hire
# Date: 29 - 5 - 2026 (first edited)

# Import libraries here.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import os
from datetime import date, datetime, timedelta
from pathlib import Path
import re


os.environ["TK_SILENCE_DEPRECATION"] = "1"

# Main window setup
root = tk.Tk()
root.title("Byte & Bolt Tech Hire")
root.geometry("500x600")

# Savefile that stores all orders
filename = "savefile.txt"

# List of all possible items available for purchase
item_list = [
    ["ACC 1 Keyboard", 20], ["ACC 1 Mouse", 15], ["Execute PC", 60], ["ARD4T 672a Laptop", 32], ["33Gi Headset", 17],
    ["ACT 2 Keyboard", 25], ["ACT 2 Mouse", 25], ["Muscle PC", 70], ["TR4G0N 884b Laptop", 38], ["36I8 Headset", 27],
    ["ANe 3 Keyboard", 15], ["ANe 3 Mouse", 10], ["Bright PC", 45], ["CRYPT 438c Laptop", 26], ["33rT Headset", 10],
    ["ARf 4 Keyboard", 22], ["ARf 4 Mouse", 17], ["Torrential PC", 65], ["TAB1TH 553d Laptop", 35], ["25yR Headset", 22]
]

# Declaring variables that will be used throughout the entire corder_datee here.
checkbox_vars = []
selected_items = []
entry_name_new_order = None
entry_name_return = None
entry_quantity = None
order_date = None
search_matches = []

# Date picker widgets
day_combo_box = None
month_combo_box = None
year_combo_box = None
follow_up_var = None

# New tracking for return-by-item feature
orders_listbox = None
order_items_frame = None
item_checkbox_vars = []
loaded_order_index = None
loaded_order_text = None

# Declaring frames to display parts of the gui.
# The setup works by refreshing a single frame with other frames of the program.

# Main menu frame which essentially acts as a gateway to the other frames.
def main_menu_build():
    """Brings up the starting screen."""
    new_order_menu_frame.pack_forget()
    return_order_menu_frame.pack_forget()
    main_menu_frame.pack(padx=20, pady=20, fill="both", expand=True)

def new_order_menu_build():
    # Switches the window space over to the order construction morder_dateule.
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
    """Switches the view over to the prorder_dateuct tracking return system."""
    main_menu_frame.pack_forget()
    new_order_menu_frame.pack_forget()
    return_order_menu_frame.pack(padx=20, pady=20, fill="both", expand=True)


# End of frame building, now starts the main backbone; processing orders, saving orders,
# showing orders, and returing orders.

# Processes orders to be ready for saving
def process_item_data(index):
    # Tracks checklist manipulations in real time.
    item_name = item_list[index][0]
    if checkbox_vars[index].get() == 1:
        if item_name not in selected_items:
            selected_items.append(item_name)
    else:
        if item_name in selected_items:
            selected_items.remove(item_name)

# Rewrites the savefile to add a new order.
def save_order_action():
    # Validates inputs and saves data directly to flat text files
    if entry_name_new_order is None:
        messagebox.showerror("Error", "The new order form is not ready yet.")
        return

    name_entry = str(entry_name_new_order.get()).strip()
    qty = str(entry_quantity.get()).strip()
    receipt_number = str(generate_receipt_number()).strip()
    
    if name_entry == "":
        messagebox.showerror("Error", "Please enter your name.")
        return
    # Name must contain only letters and spaces
    if not re.match(r"^[A-Za-z ]+$", name_entry):
        messagebox.showerror("Error", "Name must contain only letters and spaces.")
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
        # Determine order date from date picker if available
        try:
            if day_combo_box and month_combo_box and year_combo_box:
                d = int(day_combo_box.get())
                m = int(month_combo_box.get())
                y = int(year_combo_box.get())
                order_date = datetime(year=y, month=m, day=d)
            else:
                order_date = datetime.now()
        except Exception:
            messagebox.showerror("Error", "Please select a valid order date.")
            return

        order_date = order_date.strftime("%d-%m-%Y")
        order_time = order_date.strftime("%H:%M:%S")
        follow_up_date = (order_date.date() + timedelta(days=7)).strftime("%d-%m-%Y")
        items_ordered = ", ".join(selected_items)

        with open(filename, "a") as f:
            f.write(f"Date Ordered: {order_date} {order_time} | Follow-Up By: {follow_up_date} | Customer: {name_entry} | Items: {items_ordered} | Qty: {qty} | Receipt Number: {receipt_number}\n")
        
        messagebox.showinfo("Success", f"Order saved successfully!\nFollow-up by: {follow_up_date}")
        main_menu_build()  # Route user back to home panel on success
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {str(e)}")


# Shows all orders written into the savefile.
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

# Rewrites the savefile to not include returned orders.
def return_order_action():
    # Finds one matching order by customer name or receipt number and removes that one record.
    name_entry = str(entry_name_return.get()).strip()
    receipt_number = str(entry_receipt.get()).strip()

    if name_entry == "" and receipt_number == "":
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
            elif name_entry and f"customer: {name_entry}".lower() in line_lower:
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


# Searches savefile for return
def search_order_return():
    """Populate the orders_listbox with matching orders by name or receipt."""
    global search_matches
    search_matches.clear()
    orders_listbox.delete(0, tk.END)

    name_entry = str(entry_name_return.get()).strip()
    receipt_number = str(entry_receipt.get()).strip()

    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        messagebox.showerror("Error", "No orders found.")
        return

    with open(filename, "r") as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]

    for idx, line in enumerate(lines):
        line_lower = line.lower()
        matched = False
        if receipt_number and receipt_number.lower() in line_lower:
            matched = True
        elif name_entry and f"customer: {name_entry}".lower() in line_lower:
            matched = True
        elif (not receipt_number and not name_entry):
            matched = True

        if matched:
            search_matches.append((idx, line))
            display_text = f"{idx}: {line}"
            orders_listbox.insert(tk.END, display_text)

    if not search_matches:
        messagebox.showinfo("No Matches", "No orders matched your search.")



# Loads item orders for the things needed to be returned.
def load_order_items():
    """Load items for the selected order into the item checkbox panel."""
    global item_checkbox_vars, loaded_order_index, loaded_order_text
    item_checkbox_vars.clear()
    for w in order_items_frame.winfo_children():
        w.destroy()

    sel = orders_listbox.curselection()
    if not sel:
        messagebox.showerror("Error", "Please select an order from the list first.")
        return

    sel_idx = sel[0]
    try:
        loaded_order_index, loaded_order_text = search_matches[sel_idx]
    except Exception:
        messagebox.showerror("Error", "Selected order could not be located.")
        return

    # Parse items from the order line
    parts = [p.strip() for p in loaded_order_text.split("|")]
    items_field = None
    for p in parts:
        if p.lower().startswith("items:"):
            items_field = p
            break

    if not items_field:
        messagebox.showinfo("No Items", "No items field found in this order.")
        return

    items_text = items_field.split(":", 1)[1].strip()
    if items_text == "":
        messagebox.showinfo("No Items", "This order has no listed items.")
        return

    items = [it.strip() for it in items_text.split(",") if it.strip()]

    for i, it in enumerate(items):
        var = tk.IntVar()
        item_checkbox_vars.append((var, it))
        chk = tk.Checkbutton(order_items_frame, text=it, variable=var, anchor='w', bg='white')
        chk.pack(fill='x', anchor='w', padx=4, pady=1)

    messagebox.showinfo("Loaded", f"Loaded {len(items)} item(s) for return.")


def return_selected_items():
    """Return selected individual items from the loaded order."""
    global loaded_order_index, loaded_order_text
    if loaded_order_index is None or loaded_order_text is None:
        messagebox.showerror("Error", "No order loaded. Please load an order first.")
        return

    selected = [it for var, it in item_checkbox_vars if var.get() == 1]
    if not selected:
        messagebox.showerror("Error", "Please select at least one item to return.")
        return

    try:
        # Read current lines
        with open(filename, "r") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]

        # Ensure index is valid
        if loaded_order_index < 0 or loaded_order_index >= len(lines):
            messagebox.showerror("Error", "The order could not be found in the file anymore.")
            return

        orig_line = lines[loaded_order_index]
        parts = [p.strip() for p in orig_line.split("|")]

        # extract items and qty
        items_field_idx = None
        qty_field_idx = None
        for i, p in enumerate(parts):
            if p.lower().startswith("items:"):
                items_field_idx = i
            if p.lower().startswith("qty:"):
                qty_field_idx = i

        if items_field_idx is None:
            messagebox.showerror("Error", "Could not parse items from the order.")
            return

        items_text = parts[items_field_idx].split(":", 1)[1].strip()
        current_items = [it.strip() for it in items_text.split(",") if it.strip()]

        # Remove selected items
        remaining_items = [it for it in current_items if it not in selected]

        if not remaining_items:
            # remove whole order
            del lines[loaded_order_index]
            with open(filename, "w") as f:
                if lines:
                    f.write("\n".join(lines) + "\n")
            messagebox.showinfo("Returned", "All selected items returned and order removed.")
        else:
            # update items field and adjust qty (best-effort)
            parts[items_field_idx] = f"Items: {', '.join(remaining_items)}"
            if qty_field_idx is not None:
                try:
                    orig_qty = int(parts[qty_field_idx].split(":", 1)[1].strip())
                    new_qty = max(1, orig_qty - len(selected))
                    parts[qty_field_idx] = f"Qty: {new_qty}"
                except Exception:
                    pass

            new_line = " | ".join(parts)
            lines[loaded_order_index] = new_line
            with open(filename, "w") as f:
                f.write("\n".join(lines) + "\n")
            messagebox.showinfo("Returned", "Selected items returned and order updated.")

        # Clear loaded state and UI
        loaded_order_index = None
        loaded_order_text = None
        orders_listbox.delete(0, tk.END)
        for w in order_items_frame.winfo_children():
            w.destroy()
        item_checkbox_vars.clear()

    except Exception as e:
        messagebox.showerror("Error", f"Could not process item returns: {str(e)}")


# Frame 1: Home Screen Layout Setup
main_menu_frame = tk.Frame(root, bg="#aeb0b1", borderwidth=10, relief="ridge")
tk.Label(main_menu_frame, text="Welcome to Byte & Bolt!", font=("Garamond", 18, "bold"), bg="#bdbdbd").pack(pady=20)

tk.Button(main_menu_frame, text="New Order Page", bg="#635dff", fg="white", command=new_order_menu_build, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Show Existing Orders", bg="#635dff", fg="white", command=show_order_action, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Return Order Page", bg="#635dff", fg="white", command=return_order_menu_build, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Exit Application", bg="#e81313", fg="white", command=root.destroy, width=25).pack(pady=20)

# Frame 2: New Order Screen Layout Setup
new_order_menu_frame = tk.Frame(root, bg="#9e9e9e", borderwidth=10, relief="ridge")
tk.Label(new_order_menu_frame, text="Create New Hire Order", font=("Garamond", 14, "bold"), bg="#9aa0a7").pack(pady=5)

# Customer metadata forms
tk.Label(new_order_menu_frame, text="Customer Name:", bg="#9aa0a7").pack()
entry_name_new_order = tk.Entry(new_order_menu_frame)
entry_name_new_order.pack(pady=2)

tk.Label(new_order_menu_frame, text="Quantity Wanted:", bg="#9aa0a7").pack()
entry_quantity = ttk.Combobox(new_order_menu_frame,values=[str(i) for i in range(1, 21)])
entry_quantity.pack(pady=2)

# Date picker (day, month, year) with follow-up calculation
tk.Label(new_order_menu_frame, text="Order Date:", bg="#9aa0a7").pack(pady=2)
torder_dateay = date.torder_dateay()
day_values = [str(i).zfill(2) for i in range(1, 32)]
month_values = [str(i).zfill(2) for i in range(1, 13)]
year_values = [str(i) for i in range(torder_dateay.year, torder_dateay.year + 3)]

day_combo_box = ttk.Combobox(new_order_menu_frame, values=day_values, width=4)
day_combo_box.set(str(torder_dateay.day).zfill(2))
day_combo_box.pack(pady=1)

month_combo_box = ttk.Combobox(new_order_menu_frame, values=month_values, width=4)
month_combo_box.set(str(torder_dateay.month).zfill(2))
month_combo_box.pack(pady=1)

year_combo_box = ttk.Combobox(new_order_menu_frame, values=year_values, width=6)
year_combo_box.set(str(torder_dateay.year))
year_combo_box.pack(pady=1)

follow_up_var = tk.StringVar(value=(torder_dateay + timedelta(days=7)).strftime("%d-%m-%Y"))
tk.Label(new_order_menu_frame, textvariable=follow_up_var, bg="#9aa0a7").pack(pady=2)

def _update_follow_up(event=None):
    try:
        d = int(day_combo_box.get())
        m = int(month_combo_box.get())
        y = int(year_combo_box.get())
        order_date = date(year=y, month=m, day=d)
        follow_up_var.set((order_date + timedelta(days=7)).strftime("%d-%m-%Y"))
    except Exception:
        follow_up_var.set("Invalid date")

for cb in (day_combo_box, month_combo_box, year_combo_box):
    cb.bind("<<ComboboxSelected>>", _update_follow_up)

# Random receipt generator
def generate_receipt_number():
    return f"R{random.randint(0000, 9999)}"

tk.Label(new_order_menu_frame, text=f"Receipt Number: {generate_receipt_number()}", bg="#9aa0a7").pack(pady=5)

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


# Functional return components arranged into top, middle and bottom frames
return_top_frame = tk.Frame(return_order_menu_frame, bg=return_order_menu_frame.cget('bg'))
return_top_frame.pack(fill='x', pady=2)
tk.Button(return_top_frame, text="Show Existing Orders & Search Orders", bg="#635dff", fg="white", command=show_order_action).pack(side='left', padx=5, pady=5)
tk.Button(return_top_frame, text="Return 1 Order", bg = "#635dff", fg="white", command=return_order_action).pack(side='left', padx=5, pady=5)
tk.Button(return_top_frame, text="Return to Main Menu", bg="#e81313", fg="white", command=main_menu_build).pack(side='right', padx=5, pady=5)

# Individual item release (middle area)
listbox_container = tk.Frame(return_order_menu_frame)
listbox_container.pack(pady=5, fill='both', expand=False)
orders_listbox = tk.Listbox(listbox_container, height=6, width=70)
orders_listbox.pack(side='left', fill='both', expand=True)
listbox_scroll = tk.Scrollbar(listbox_container, orient='vertical', command=orders_listbox.yview)
listbox_scroll.pack(side='right', fill='y')
orders_listbox.configure(yscrollcommand=listbox_scroll.set)

tk.Button(return_order_menu_frame, text="Search Matching Orders", bg="#4aa3ff", fg="white", command=lambda: search_order_return()).pack(pady=5)
tk.Button(return_order_menu_frame, text="Load Selected Order Items", bg="#4aa3ff", fg="white", command=lambda: load_order_items()).pack(pady=5)

# Frame where individual item checkboxes will be placed; allow it to expand so bottom buttons remain visible
order_items_frame = tk.Frame(return_order_menu_frame, bd=1, relief='sunken', bg='white')
order_items_frame.pack(fill='both', pady=5, padx=5, expand=True)

# Bottom frame with actions that must remain visible
return_bottom_frame = tk.Frame(return_order_menu_frame, bg=return_order_menu_frame.cget('bg'))
return_bottom_frame.pack(fill='x', side='bottom', pady=5)
tk.Button(return_bottom_frame, text="Return Selected Items", bg="#635dff", fg="white", command=lambda: return_selected_items()).pack(side='left', padx=5)



# Run layout generator initializer sequence
main_menu_build()
root.mainloop()
