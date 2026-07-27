# Author: Harshal Joshi
# Purpose: To create a GUI based application for Byte and Bolt Tech Hire
# Date: 29/05/2026 (first edited)

# Import libraries here.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import os # allows the program to access the native OS
from datetime import date, datetime, timedelta
import re # provides support for regular expressions, allowing manipulation to the string via character specific patterns
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
checkbox_vars = [] # Checks whether a checkbox is selected or not
selected_items = [] # Stores the selected item
entry_name_new_order = None # New order entry field for name
entry_name_return = None # Entry field on return menu for name
entry_quantity = None # Entry field for quantity 
order_date = None
search_matches = [] # Used in the return order menu to find related orders.

# Date picker widgets
day_combo_box = None
month_combo_box = None
year_combo_box = None
follow_up_date = None # Follow up date

# Tracking all items
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


# Reused variables for fonts 
font_spam_size_12 = ("Garamond", 12, "bold")
font_spam_size_9 = ("Garamond", 9, "bold")
font_spam_size_8 = ("Garamond", 8)
font_spam_size_7 = ("Garamond", 7)
title_spam_size_18 = ("Garamond", 18, "bold")

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
def return_order_menu_build(order_items_container=None):
    # Switches window via buttons on the main menu
    global shopping_cart
    shopping_cart.clear()


    # Clears the listbox where orders are displayed
    if orders_listbox is not None:
        orders_listbox.delete(0, tk.END)

    # Safely resolve target container from argument or global context
    container = order_items_container if order_items_container is not None else order_items_frame

    # Safely clear existing children from the container frame
    if container is not None:
        try:
            if container.winfo_exists():
                for widget in list(container.winfo_children()):
                    try:
                        if widget.winfo_exists():
                            widget.destroy()
                    except (tk.TclError, AttributeError):
                        pass
        except (tk.TclError, AttributeError):
            pass



    # Deletes pre existing arguments within the entry fields
    if entry_name_return is not None or entry_receipt is not None:
        if entry_name_return is not None:
            entry_name_return.delete(0, tk.END)
        if entry_receipt is not None:
            entry_receipt.delete(0, tk.END)

    # Other menu interaction that deletes the others, and brings up only return menu.
    main_menu_frame.pack_forget()
    new_order_menu_frame.pack_forget()
    return_order_menu_frame.pack(padx=20, pady=20, fill="both", expand=True)

## Functions that are essential to the program.


# Declares the date of when the order was ordered
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

# Gathers the total amounts of the price and items in the order
def get_cart_totals():
    total_price = 0
    total_items = 0

    for item_name in shopping_cart:
        quantity = shopping_cart[item_name]
        price = next((item[1] for item in item_list if item[0] == item_name), 0)
        item_total = quantity * price
        total_price += item_total
        total_items += quantity

    return total_price, total_items

# Reads the savefile (does not overwrite in any way)
# Is a function to be able to be called at any given time, as there are two total buttons
# scattered throughout the program that have this exact purpose
def read_orders():
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return []

    with open(filename, "r") as f:
        return [line.rstrip("\n") for line in f if line.strip()]

# Used by the return menu to find related orders using the users' name and/ or receipt number
def get_matching_order_entries(name_entry="", receipt_number=""):
    lines = read_orders()
    matches = []

    for index, line in enumerate(lines):
        line_lower = line.lower()
        if receipt_number and receipt_number.lower() in line_lower:
            matches.append((index, line))
        elif name_entry and f"customer: {name_entry}".lower() in line_lower:
            matches.append((index, line))
        elif not receipt_number and not name_entry:
            matches.append((index, line))

    return matches


# Adds item to the new order cart
def add_item_to_cart(item_name, item_price):
    global shopping_cart
    quantity_text = item_spinners[item_name].get().strip()
    try:
        quantity = int(quantity_text)
        if quantity < 1 or quantity > 20:
            messagebox.showerror("Error", "Quantity must be between 1 and 20.")
            return
    except ValueError:
        messagebox.showerror("Error", f"Invalid quantity for {item_name}.")
        return

    # Check in place to stop from double quantity ordering - where a prorder_dateuct that is oredered twice is mistakenly
    # recorded twice, rather than showing as a second iteration of the prorder_dateuct. E.g ACC 1 Keyboard x1 ACC 1 Keyboard
    # -> ACC 1 Keyboard x2
    if item_name in shopping_cart:
        shopping_cart[item_name] += quantity
    else:
        shopping_cart[item_name] = quantity
    
    item_spinners[item_name].set("1")  # Reset spinner to 1
    update_cart_display()
    messagebox.showinfo("Added", f"Added {quantity}x {item_name} to cart.")


# Removes item fom the New Order menu cart
def remove_item_from_cart(item_name):
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
        quantity = shopping_cart[item_name]
        price = next((item[1] for item in item_list if item[0] == item_name), 0)
        item_total = quantity * price

        item_row = tk.Frame(cart_display_frame, bg="white", relief="solid", bd=1)
        item_row.pack(fill="x", padx=5, pady=2)

        # Item info
        item_info = f"{item_name} x{quantity} = ${item_total}"
        tk.Label(item_row, text=item_info, bg="white", anchor="w", justify="left").pack(side="left", fill="x", expand=True, padx=5, pady=5)

        # Remove button
        tk.Button(item_row, text="Remove", bg="#e81313", fg="white", width=8,
                 command=lambda name=item_name: remove_item_from_cart(name)).pack(side="right", padx=5, pady=2)

    cart_total_var.set(f"Total ({total_items} items): ${total_price:.2f}") # .2f allows for rounding of value to 2 decimal places (12.5 -> 12.50)

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
    if not re.match(r"^[A-Za-z ]+$", name_entry): # Goes through the name entry space to check whether or not name follows criterion
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

        items_ordered = ", ".join([f"{item} x{quantity}" for item, quantity in shopping_cart.items()])
        total_quantity = sum(shopping_cart.values())

        with open(filename, "a") as f:
            f.write(f"Date Ordered: {order_date_text} {order_time} | Follow-Up By: {follow_up_date} | Customer: {name_entry} | Items: {items_ordered} | quantity: {total_quantity} | Receipt Number: {receipt_number}\n")

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
        quantity = shopping_cart[item_name]
        price = next((item[1] for item in item_list if item[0] == item_name), 0)
        item_total = quantity * price
        receipt_text += f"{item_name}\n  quantity: {quantity} x ${price} = ${item_total}\n"

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
    lines = read_orders()
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
    # Matching entires provided by the earlier function get_matching_order_entries. 
    try:
        lines = read_orders()
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

    # sel is checking whether or not any orders in the listbox (loaded in program)
    # are actually there
    sel = orders_listbox.curselection()
    if not sel:
        messagebox.showerror("Error", "Please select an order from the list first.")
        return

    sel_index = sel[0]
    try:
        loaded_order_index, loaded_order_text = search_matches[sel_index]
    except Exception:
        messagebox.showerror("Error", "Selected order could not be located.")
        return

    # Parse items from the order line
    parts_of_order = [p.strip() for p in loaded_order_text.split("|")]
    items_field = None
    for p in parts_of_order:
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

        original_line = lines[loaded_order_index]
        parts_of_order = [p.strip() for p in original_line.split("|")]

        # Extract items and quantity
        items_field_index = None
        quantity_field_index = None
        for i, p in enumerate(parts_of_order):
            if p.lower().startswith("items:"):
                items_field_index = i
            if p.lower().startswith("quantity:"):
                quantity_field_index = i

        if items_field_index is None:
            messagebox.showerror("Error", "Could not parse items from the order.")
            return

        items_text = parts_of_order[items_field_index].split(":", 1)[1].strip()
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
            # update items field and adjust quantity (best-effort)
            parts_of_order[items_field_index] = f"Items: {', '.join(remaining_items)}"
            if quantity_field_index is not None:
                try:
                    original_quantity = int(parts_of_order[quantity_field_index].split(":", 1)[1].strip())
                    new_quantity = max(1, original_quantity - len(selected))
                    parts_of_order[quantity_field_index] = f"quantity: {new_quantity}"
                except Exception:
                    pass

            new_line = " | ".join(parts_of_order)
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
tk.Label(main_menu_frame, text="Welcome to Byte & Bolt!", font = title_spam_size_18, bg="#bdbdbd").pack(pady=20)

raw_img = Image.open("Images/Logo.png")
original_width, original_height = raw_img.size
new_width = original_width // 5
new_height = original_height // 5
resized_pil_img = raw_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
png_image = ImageTk.PhotoImage(resized_pil_img)
image_frame = tk.Frame(root)  # Replace 'root' with your parent window variable name if different
image_frame.pack()
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
tk.Label(header_frame, text="Create New Hire Order", font = font_spam_size_12, bg="#9aa0a7").pack(side="left", padx=5)

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

follow_up_date = tk.StringVar(value=(today + timedelta(days=7)).strftime("%d-%m-%Y"))
tk.Label(date_frame, textvariable=follow_up_date, bg="#9aa0a7", width=12).pack(side="left", padx=5)

# Calculates the follow up date to the date entered in the new order menu.
def _update_follow_up(event=None):
    try:
        d = int(day_combo_box.get())
        m = int(month_combo_box.get())
        y = int(year_combo_box.get())
        order_date = date(year=y, month=m, day=d)
        follow_up_date.set((order_date + timedelta(days=7)).strftime("%d-%m-%Y"))
    except Exception:
        follow_up_date.set("Invalid date")

for cb in (day_combo_box, month_combo_box, year_combo_box):
    cb.bind("<<ComboboxSelected>>", _update_follow_up)

# Random receipt generator
def generate_receipt_number():
    return f"R{random.randint(0000, 9999)}"

# Items and cart vertically stacked (cart gets more prominence)
content_frame = tk.Frame(new_order_menu_frame, bg="#9e9e9e")
content_frame.pack(fill="both", expand=True, padx=5, pady=3)

# Top section - Available Items (smaller)
tk.Label(content_frame, text="Available Items", bg="#9aa0a7", font = font_spam_size_9).pack(fill="x")
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
    tk.Label(item_frame, text=f"{item_name[:20]} ${item_price}", bg="white", anchor="w", width=24, font = font_spam_size_8).pack(side="left", fill="x", expand=True)
    
    # Quantity spinner
    quantity_var = tk.StringVar(value="1")
    item_spinners[item_name] = quantity_var
    spinbox = tk.Spinbox(item_frame, from_=1, to=20, textvariable=quantity_var, width=3, font = font_spam_size_8)
    spinbox.pack(side="left", padx=1)
    
    # Add button
    tk.Button(item_frame, text="Add", bg="#4aa3ff", fg="white", width=3, font = font_spam_size_7,
             command=lambda name=item_name, price=item_price: add_item_to_cart(name, price)).pack(side="left", padx=1)

# Bottom section - Shopping Cart (larger, takes remaining space)
tk.Label(content_frame, text="Shopping Cart", bg="#9aa0a7", font = font_spam_size_9).pack(fill="x", pady=(1, 0))
cart_container = tk.Frame(content_frame, bd=1, relief="sunken", bg="white")
cart_container.pack(fill="both", expand=True)

# Scrollable cart canvas
cart_canvas = tk.Canvas(cart_container, bg="white", highlightthickness=0, height=200)
cart_scrollbar = tk.Scrollbar(cart_container, orient="vertical", command=cart_canvas.yview)
cart_display_frame = tk.Frame(cart_canvas, bg="white")

cart_display_frame.bind("<Configure>", lambda e: cart_canvas.configure(scrollregion=cart_canvas.bbox("all")))
cart_canvas.create_window((0, 0), window=cart_display_frame, anchor="nw")
cart_canvas.configure(yscrollcommand=cart_scrollbar.set)

cart_canvas.pack(side="left", fill="x", expand=True)
cart_scrollbar.pack(side="right", fill="y", pady=(0,20))

# Cart total label
cart_total_var = tk.StringVar(value="Total: $0.00")
tk.Label(new_order_menu_frame, textvariable=cart_total_var, bg="#9aa0a7", font = font_spam_size_9).pack(pady=1)

# Execution navigation triggers inside Order panel
button_frame = tk.Frame(new_order_menu_frame, bg="#9e9e9e")
button_frame.pack(fill="x", pady=2)
tk.Button(button_frame, text="View Receipt", bg="#4aa3ff", fg="white", font = font_spam_size_8, command=generate_receipt).pack(side="left", padx=3, expand=True, fill="x")
tk.Button(button_frame, text="Commit Order", bg="#635dff", fg="white", font = font_spam_size_8, command=save_order_action).pack(side="left", padx=3, expand=True, fill="x")
tk.Button(button_frame, text="Cancel", bg="#e81313", fg="white", font = font_spam_size_8, command=main_menu_build).pack(side="left", padx=3, expand=True, fill="x")


# Frame 3: Return Order Screen Layout Setup
return_order_menu_frame = tk.Frame(root, bg="#707a7a", borderwidth=10, relief="ridge")
tk.Label(return_order_menu_frame, text="Equipment Return Portal", font = font_spam_size_12, bg="#B6B6B6").pack(pady=3)

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
tk.Button(return_top_frame, text="Search", bg="#4aa3ff", fg="white", font = font_spam_size_8, command=lambda: search_order_return()).pack(side='left', padx=2, expand=True, fill="x")
tk.Button(return_top_frame, text="Load Items", bg="#635dff", fg="white", font = font_spam_size_8, command=lambda: load_order_items()).pack(side='left', padx=2, expand=True, fill="x")
tk.Button(return_top_frame, text="Back", bg="#e81313", fg="white", font = font_spam_size_8, command=main_menu_build).pack(side='right', padx=2, expand=True, fill="x")

# Order list section
tk.Label(return_order_menu_frame, text="Orders:", bg="#BDBCBC", font = font_spam_size_8).pack(anchor='w', padx=5, pady=(2, 0))
listbox_container = tk.Frame(return_order_menu_frame, bd=1, relief='sunken')
listbox_container.pack(pady=2, fill='both', expand=False, padx=5)
orders_listbox = tk.Listbox(listbox_container, height=3, width=60, font = font_spam_size_7)
orders_listbox.pack(side='left', fill='both', expand=True)
listbox_scroll = tk.Scrollbar(listbox_container, orient='vertical', command=orders_listbox.yview)
listbox_scroll.pack(side='right', fill='y')
orders_listbox.configure(yscrollcommand=listbox_scroll.set)

# Items to return section
tk.Label(return_order_menu_frame, text="Items:", bg="#BDBCBC", font = font_spam_size_8).pack(anchor='w', padx=5, pady=(2, 0))
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

# Bottom buttons that only return (either full order or selected items)
return_bottom_frame = tk.Frame(return_order_menu_frame, bg=return_order_menu_frame.cget('bg'))
return_bottom_frame.pack(fill='x', pady=2, padx=5)
tk.Button(return_bottom_frame, text="Return Order", bg="#635dff", fg="white", font = font_spam_size_8, command=return_order_action).pack(side='left', padx=2, expand=True, fill="x")
tk.Button(return_bottom_frame, text="Return Items", bg="#635dff", fg="white", font = font_spam_size_8, command=lambda: return_selected_items()).pack(side='left', padx=2, expand=True, fill="x")



# Run layout generator initializer sequence
main_menu_build()
root.mainloop()