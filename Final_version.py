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
import re
from PIL import Image, ImageTk

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

# Shopping cart system (new order page)
shopping_cart = {}  # {item_name: quantity}
cart_display_frame = None
cart_total_var = None
item_spinners = {}  # {item_name: StringVar for quantity}

## Declaring frames to display parts of the GUI.

# Main menu frame - central frame to connect all others.
def main_menu_build():
     # Starting screen
    new_order_menu_frame.pack_forget()
    return_order_menu_frame.pack_forget()
    main_menu_frame.pack(padx=20, pady=20, fill="both", expand=True)

# New order frame - frame where ordering happens
def new_order_menu_build():
    # Switches window via buttons on the main menu
    global shopping_cart
    shopping_cart.clear()
    if entry_name_new_order is not None:
        entry_name_new_order.delete(0, tk.END)
    
    main_menu_frame.pack_forget()
    return_order_menu_frame.pack_forget()
    new_order_menu_frame.pack(padx=20, pady=20, fill="both", expand=True)
    update_cart_display()

# Return order frame - frame where anti ordering happens
def return_order_menu_build():
    # Switches window via buttons on the main menu
    main_menu_frame.pack_forget()
    new_order_menu_frame.pack_forget()
    return_order_menu_frame.pack(padx=20, pady=20, fill="both", expand=True)


## Functions that are essential to the program.

def get_order_datetime():
    if day_combo_box and month_combo_box and year_combo_box:
        try:
            d = int(day_combo_box.get())
            m = int(month_combo_box.get())
            y = int(year_combo_box.get())
            return datetime(year=y, month=m, day=d)
        except Exception as exc:
            raise ValueError("Please select a valid order date.") from exc
    return datetime.now()


def get_cart_totals():
    total_price = 0
    total_items = 0

    for item_name in shopping_cart:
        qty = shopping_cart[item_name]
        price = next((item[1] for item in item_list if item[0] == item_name), 0)
        item_total = qty * price
        total_price += item_total
        total_items += qty

    return total_price, total_items


def read_order_lines():
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return []

    with open(filename, "r") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def get_matching_order_entries(name_entry="", receipt_number=""):
    lines = read_order_lines()
    matches = []

    for idx, line in enumerate(lines):
        line_lower = line.lower()
        if receipt_number and receipt_number.lower() in line_lower:
            matches.append((idx, line))
        elif name_entry and f"customer: {name_entry}".lower() in line_lower:
            matches.append((idx, line))
        elif not receipt_number and not name_entry:
            matches.append((idx, line))

    return matches


# Adds item to the new order cart
def add_item_to_cart(item_name, item_price):
    # Add item in goorder_date quantity
    global shopping_cart
    qty_text = item_spinners[item_name].get().strip()
    try:
        qty = int(qty_text)
        if qty < 1 or qty > 20:
            messagebox.showerror("Error", "Quantity must be between 1 and 20.")
            return
    except ValueError:
        messagebox.showerror("Error", f"Invalid quantity for {item_name}.")
        return

    # Check in place to stop from double quantity ordering - where a prorder_dateuct that is oredered twice is mistakenly
    # recorded twice, rather than showing as a second iteration of the prorder_dateuct. E.g ACC 1 Keyboard x1 ACC 1 Keyboard
    # -> ACC 1 Keyboard x2
    if item_name in shopping_cart:
        shopping_cart[item_name] += qty
    else:
        shopping_cart[item_name] = qty
    
    item_spinners[item_name].set("1")  # Reset spinner to 1
    update_cart_display()
    messagebox.showinfo("Added", f"Added {qty}x {item_name} to cart.")


# Removes item fom the new order cart
def remove_item_from_cart(item_name):
    # Remove item(s) from the new order shopping cart
    global shopping_cart
    if item_name in shopping_cart:
        del shopping_cart[item_name]
        update_cart_display()

# Updates the cart display
def update_cart_display():
    # Clear previous cart display
    for widget in cart_display_frame.winfo_children():
        widget.destroy()

    # No values in shopping cart? Sends error message
    if not shopping_cart:
        tk.Label(cart_display_frame, text="Cart is empty", bg="white", fg="gray").pack(pady=20)
        cart_total_var.set("Total: $0.00")
        return

    total_price, total_items = get_cart_totals()

    # Display each item in cart through a for loop
    for item_name in shopping_cart:
        qty = shopping_cart[item_name]
        price = next((item[1] for item in item_list if item[0] == item_name), 0)
        item_total = qty * price

        item_row = tk.Frame(cart_display_frame, bg="white", relief="solid", bd=1)
        item_row.pack(fill="x", padx=5, pady=2)

        # Item info
        item_info = f"{item_name} x{qty} = ${item_total}"
        tk.Label(item_row, text=item_info, bg="white", anchor="w", justify="left").pack(side="left", fill="x", expand=True, padx=5, pady=5)

        # Remove button
        tk.Button(item_row, text="Remove", bg="#e81313", fg="white", width=8,
                 command=lambda name=item_name: remove_item_from_cart(name)).pack(side="right", padx=5, pady=2)

    cart_total_var.set(f"Total ({total_items} items): ${total_price:.2f}")

# Rewrites the savefile to add a new order.
def save_order_action():
    # Validates inputs and saves data directly to text file
    if entry_name_new_order is None:
        messagebox.showerror("Error", "The new order form is not ready yet.")
        return

    name_entry = str(entry_name_new_order.get()).strip()
    receipt_number = str(generate_receipt_number()).strip()

    if name_entry == "":
        messagebox.showerror("Error", "Please enter your name.")
        return
    if not re.match(r"^[A-Za-z ]+$", name_entry):
        messagebox.showerror("Error", "Name must contain only letters and spaces.")
        return

    if not shopping_cart:
        messagebox.showerror("Error", "Please add at least one item to cart.")
        return

    try:
        order_dt = get_order_datetime()
        order_date_text = order_dt.strftime("%d-%m-%Y")
        order_time = order_dt.strftime("%H:%M:%S")
        follow_up_date = (order_dt.date() + timedelta(days=7)).strftime("%d-%m-%Y")

        items_ordered = ", ".join([f"{item} x{qty}" for item, qty in shopping_cart.items()])
        total_qty = sum(shopping_cart.values())

        with open(filename, "a") as f:
            f.write(f"Date Ordered: {order_date_text} {order_time} | Follow-Up By: {follow_up_date} | Customer: {name_entry} | Items: {items_ordered} | Qty: {total_qty} | Receipt Number: {receipt_number}\n")

        messagebox.showinfo("Success", f"Order saved successfully!\nFollow-up by: {follow_up_date}")
        main_menu_build()
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {str(e)}")


# Receipt generation function
def generate_receipt():
    # Creates a receipt for the user to view once order is complete
    if not shopping_cart:
        messagebox.showerror("Error", "Cart is empty. Cannot generate receipt.")
        return

    name_entry = str(entry_name_new_order.get()).strip()
    if name_entry == "":
        messagebox.showerror("Error", "Please enter customer name first.")
        return

    try:
        order_dt = get_order_datetime()
    except Exception:
        messagebox.showerror("Error", "Invalid order date.")
        return

    receipt_number = generate_receipt_number()
    order_date_text = order_dt.strftime("%d-%m-%Y")
    order_time = order_dt.strftime("%H:%M:%S")
    follow_up_date = (order_dt.date() + timedelta(days=7)).strftime("%d-%m-%Y")

    receipt_text = f"""
{'='*50}
         BYTE & BOLT TECH HIRE RECEIPT
{'='*50}

Receipt Number: {receipt_number}
Date: {order_date_text}
Time: {order_time}
Customer: {name_entry}
Follow-up by: {follow_up_date}

{'-'*50}
ITEMS ORDERED:
{'-'*50}
"""

    total_price, total_items = get_cart_totals()

    for item_name in shopping_cart:
        qty = shopping_cart[item_name]
        price = next((item[1] for item in item_list if item[0] == item_name), 0)
        item_total = qty * price
        receipt_text += f"{item_name}\n  Qty: {qty} x ${price} = ${item_total}\n"

    receipt_text += f"""
{'-'*50}
Total Items: {total_items}
Total Amount: ${total_price:.2f}

{'='*50}
Thank you for your business!
{'='*50}
"""

    messagebox.showinfo("Order Receipt", receipt_text)


# Shows all orders written into the savefile.
def show_order_action():
    # Reads transactional customer logs out loud via native OS alerts.
    lines = read_order_lines()
    data = "\n".join(lines).strip()

    if data == "":
        messagebox.showerror("No Data", "No files or records found or empty file.")
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
        lines = read_order_lines()
        matching_entries = get_matching_order_entries(name_entry, receipt_number)

        if not matching_entries:
            messagebox.showerror("Error", "No matching order found.")
            return

        if len(matching_entries) > 1:
            messagebox.showwarning("Multiple Matches", "More than one order matched. Please use the receipt number for an exact result.")
            return

        matched_order = matching_entries[0][1]
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
    # Searched by either using a name entry or a receipt number entry
    global search_matches
    search_matches.clear()
    orders_listbox.delete(0, tk.END)

    name_entry = str(entry_name_return.get()).strip()
    receipt_number = str(entry_receipt.get()).strip()

    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        messagebox.showerror("Error", "No orders found.")
        return

    matching_entries = get_matching_order_entries(name_entry, receipt_number)

    for index, line in matching_entries:
        search_matches.append((index, line))
        display_text = f"{index}: {line}"
        orders_listbox.insert(tk.END, display_text)

    if not search_matches:
        messagebox.showinfo("No Matches", "No orders matched your search.")



# Loads item orders for the things needed to be returned in the checkbox which is scrollable.
def load_order_items():
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


# Return only a select few items
def return_selected_items():
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

# 1. Open the original image file
raw_img = Image.open("Images/Logo.png")

# 2. Extract dimensions safely
orig_width, orig_height = raw_img.size

# 3. Calculate new dimensions (simulating your original .subsample(5, 5))
new_width = orig_width // 5
new_height = orig_height // 5

# 4. Create the resized raw Pillow object
resized_pil_img = raw_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

# 5. CONVERT to Tkinter format (This variable MUST be used in your widget)
png_image = ImageTk.PhotoImage(resized_pil_img)

# 6. Create the layout frame using standard tkinter (tk)
image_frame = tk.Frame(root)  # Replace 'root' with your parent window variable name if different
image_frame.pack()

# 7. Create the display Label using the correct 'png_image' variable
image_label = tk.Label(image_frame, image=png_image)
image_label.image = png_image  # Explicitly save reference to prevent garbage collection
image_label.pack()


tk.Button(main_menu_frame, text="New Order Page", bg="#635dff", fg="white", command=new_order_menu_build, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Show Existing Orders", bg="#635dff", fg="white", command=show_order_action, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Return Order Page", bg="#635dff", fg="white", command=return_order_menu_build, width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Exit Application", bg="#e81313", fg="white", command=root.destroy, width=25).pack(pady=20)

# Frame 2: New Order Screen Layout Setup (Shopping Cart System)
new_order_menu_frame = tk.Frame(root, bg="#9e9e9e", borderwidth=10, relief="ridge")

# Compact header with customer info and date on one row
header_frame = tk.Frame(new_order_menu_frame, bg="#9aa0a7")
header_frame.pack(fill="x", padx=5, pady=3)
tk.Label(header_frame, text="Create New Hire Order", font=("Garamond", 12, "bold"), bg="#9aa0a7").pack(side="left", padx=5)

# Customer name entry
tk.Label(new_order_menu_frame, text="Name:", bg="#9aa0a7").pack()
entry_name_new_order = tk.Entry(new_order_menu_frame, width=40)
entry_name_new_order.pack(pady=1)

# Date picker on one line
date_frame = tk.Frame(new_order_menu_frame, bg="#9aa0a7")
date_frame.pack(fill="x", padx=5, pady=1)
tk.Label(date_frame, text="Order Date:", bg="#9aa0a7", width=10).pack(side="left")

today = date.today()
day_values = [str(i).zfill(2) for i in range(1, 32)]
month_values = [str(i).zfill(2) for i in range(1, 13)]
year_values = [str(i) for i in range(today.year, today.year + 3)]

day_combo_box = ttk.Combobox(date_frame, values=day_values, width=3)
day_combo_box.set(str(today.day).zfill(2))
day_combo_box.pack(side="left", padx=2)

month_combo_box = ttk.Combobox(date_frame, values=month_values, width=3)
month_combo_box.set(str(today.month).zfill(2))
month_combo_box.pack(side="left", padx=2)

year_combo_box = ttk.Combobox(date_frame, values=year_values, width=4)
year_combo_box.set(str(today.year))
year_combo_box.pack(side="left", padx=2)

follow_up_var = tk.StringVar(value=(today + timedelta(days=7)).strftime("%d-%m-%Y"))
tk.Label(date_frame, textvariable=follow_up_var, bg="#9aa0a7", width=12).pack(side="left", padx=5)

# Calculates the follow up date to the date entered in the new order menu.
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

# Items and cart vertically stacked (cart gets more prominence)
content_frame = tk.Frame(new_order_menu_frame, bg="#9e9e9e")
content_frame.pack(fill="both", expand=True, padx=5, pady=3)

# Top section - Available Items (smaller)
tk.Label(content_frame, text="Available Items", bg="#9aa0a7", font=("Garamond", 9, "bold")).pack(fill="x")
canvas_container = tk.Frame(content_frame, bd=1, relief="sunken")
canvas_container.pack(fill="x", expand=False, pady=2)

canvas = tk.Canvas(canvas_container, bg="white", height=60)
scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Build item list with quantity spinners and add buttons
for item_data in item_list:
    item_name = item_data[0]
    item_price = item_data[1]
    
    item_frame = tk.Frame(scrollable_frame, bg="white")
    item_frame.pack(fill="x", padx=2, pady=1)
    
    # Item name and price (compact)
    tk.Label(item_frame, text=f"{item_name[:20]} ${item_price}", bg="white", anchor="w", width=24, font=("Garamond", 8)).pack(side="left", fill="x", expand=True)
    
    # Quantity spinner
    qty_var = tk.StringVar(value="1")
    item_spinners[item_name] = qty_var
    spinbox = tk.Spinbox(item_frame, from_=1, to=20, textvariable=qty_var, width=3, font=("Garamond", 8))
    spinbox.pack(side="left", padx=1)
    
    # Add button
    tk.Button(item_frame, text="Add", bg="#4aa3ff", fg="white", width=3, font=("Garamond", 7),
             command=lambda name=item_name, price=item_price: add_item_to_cart(name, price)).pack(side="left", padx=1)

# Bottom section - Shopping Cart (larger, takes remaining space)
tk.Label(content_frame, text="Shopping Cart", bg="#9aa0a7", font=("Garamond", 9, "bold")).pack(fill="x", pady=(5, 0))
cart_container = tk.Frame(content_frame, bd=1, relief="sunken", bg="white")
cart_container.pack(fill="both", expand=True)

# Scrollable cart canvas
cart_canvas = tk.Canvas(cart_container, bg="white", highlightthickness=0)
cart_scrollbar = tk.Scrollbar(cart_container, orient="vertical", command=cart_canvas.yview)
cart_display_frame = tk.Frame(cart_canvas, bg="white")

cart_display_frame.bind("<Configure>", lambda e: cart_canvas.configure(scrollregion=cart_canvas.bbox("all")))
cart_canvas.create_window((0, 0), window=cart_display_frame, anchor="nw")
cart_canvas.configure(yscrollcommand=cart_scrollbar.set)

cart_canvas.pack(side="left", fill="both", expand=True)
cart_scrollbar.pack(side="right", fill="y")

# Cart total label
cart_total_var = tk.StringVar(value="Total: $0.00")
tk.Label(new_order_menu_frame, textvariable=cart_total_var, bg="#9aa0a7", font=("Garamond", 9, "bold")).pack(pady=1)

# Execution navigation triggers inside Order panel
button_frame = tk.Frame(new_order_menu_frame, bg="#9e9e9e")
button_frame.pack(fill="x", pady=2)
tk.Button(button_frame, text="View Receipt", bg="#4aa3ff", fg="white", font=("Garamond", 8), command=generate_receipt).pack(side="left", padx=3, expand=True, fill="x")
tk.Button(button_frame, text="Commit Order", bg="#635dff", fg="white", font=("Garamond", 8), command=save_order_action).pack(side="left", padx=3, expand=True, fill="x")
tk.Button(button_frame, text="Cancel", bg="#e81313", fg="white", font=("Garamond", 8), command=main_menu_build).pack(side="left", padx=3, expand=True, fill="x")


# Frame 3: Return Order Screen Layout Setup
return_order_menu_frame = tk.Frame(root, bg="#707a7a", borderwidth=10, relief="ridge")
tk.Label(return_order_menu_frame, text="Equipment Return Portal", font=("Garamond", 12, "bold"), bg="#B6B6B6").pack(pady=3)

# Compact input section
input_frame = tk.Frame(return_order_menu_frame, bg="#707a7a")
input_frame.pack(fill="x", padx=5, pady=1)

tk.Label(input_frame, text="Name:", bg="#BDBCBC", width=8).pack(side="left")
entry_name_return = tk.Entry(input_frame, width=20)
entry_name_return.pack(side="left", padx=2)

tk.Label(input_frame, text="Receipt:", bg="#BDBCBC", width=8).pack(side="left")
entry_receipt = tk.Entry(input_frame, width=15)
entry_receipt.pack(side="left", padx=2)

# Top buttons for navigation
return_top_frame = tk.Frame(return_order_menu_frame, bg=return_order_menu_frame.cget('bg'))
return_top_frame.pack(fill='x', pady=1, padx=5)
tk.Button(return_top_frame, text="Search", bg="#4aa3ff", fg="white", font=("Garamond", 8), command=lambda: search_order_return()).pack(side='left', padx=2, expand=True, fill="x")
tk.Button(return_top_frame, text="Load Items", bg="#635dff", fg="white", font=("Garamond", 8), command=lambda: load_order_items()).pack(side='left', padx=2, expand=True, fill="x")
tk.Button(return_top_frame, text="Back", bg="#e81313", fg="white", font=("Garamond", 8), command=main_menu_build).pack(side='right', padx=2, expand=True, fill="x")

# Order list section
tk.Label(return_order_menu_frame, text="Orders:", bg="#BDBCBC", font=("Garamond", 8)).pack(anchor='w', padx=5, pady=(2, 0))
listbox_container = tk.Frame(return_order_menu_frame, bd=1, relief='sunken')
listbox_container.pack(pady=2, fill='both', expand=False, padx=5)
orders_listbox = tk.Listbox(listbox_container, height=3, width=60, font=("Garamond", 7))
orders_listbox.pack(side='left', fill='both', expand=True)
listbox_scroll = tk.Scrollbar(listbox_container, orient='vertical', command=orders_listbox.yview)
listbox_scroll.pack(side='right', fill='y')
orders_listbox.configure(yscrollcommand=listbox_scroll.set)

# Items to return section
tk.Label(return_order_menu_frame, text="Items:", bg="#BDBCBC", font=("Garamond", 8)).pack(anchor='w', padx=5, pady=(2, 0))
order_items_container = tk.Frame(return_order_menu_frame, bd=1, relief='sunken', bg='white')
order_items_container.pack(fill='both', expand=True, pady=2, padx=5)

# Scrollable items frame
items_canvas = tk.Canvas(order_items_container, bg='white', highlightthickness=0)
items_scrollbar = tk.Scrollbar(order_items_container, orient='vertical', command=items_canvas.yview)
order_items_frame = tk.Frame(items_canvas, bg='white')

order_items_frame.bind("<Configure>", lambda e: items_canvas.configure(scrollregion=items_canvas.bbox("all")))
items_canvas.create_window((0, 0), window=order_items_frame, anchor="nw")
items_canvas.configure(yscrollcommand=items_scrollbar.set)

items_canvas.pack(side='left', fill='both', expand=True)
items_scrollbar.pack(side='right', fill='y')

# Bottom buttons - always visible
return_bottom_frame = tk.Frame(return_order_menu_frame, bg=return_order_menu_frame.cget('bg'))
return_bottom_frame.pack(fill='x', pady=2, padx=5)
tk.Button(return_bottom_frame, text="Return Order", bg="#635dff", fg="white", font=("Garamond", 8), command=return_order_action).pack(side='left', padx=2, expand=True, fill="x")
tk.Button(return_bottom_frame, text="Return Items", bg="#635dff", fg="white", font=("Garamond", 8), command=lambda: return_selected_items()).pack(side='left', padx=2, expand=True, fill="x")



# Run layout generator initializer sequence
main_menu_build()
root.mainloop()