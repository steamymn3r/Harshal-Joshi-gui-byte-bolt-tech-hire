# Author: Harshal Joshi
# Purpose: To create a GUI application for Byte and Bolt Tech Hire
# Date: 29 - 5 - 2026 
import tkinter as tk
from tkinter import messagebox
import os
import datetime

# main window base template
root = tk.Tk()
root.title("Byte & Bolt Tech Hire (Home Page)")
root.geometry("500x500")
root.configure(bg="#e8e2c8")

# FIX: Keep tracks of Tkinter variables separately from text strings
checkbox_vars = []
selected_items = []
entry1 = None
quantity_vars = []
filename = "savefile.txt"

def process_item_data(index):
    # If the checkbox is checked, add the item name to our selection list
    if checkbox_vars[index].get() == 1:
        if item_list[index][0] not in selected_items:
            selected_items.append(item_list[index][0])
    # If unchecked, remove it
    else:
        if item_list[index][0] in selected_items:
            selected_items.remove(item_list[index][0])

# New order. This function will allow the user to place a new order.
def new_order():
    global entry1, checkbox_vars, selected_items
    
    # Reset tracking arrays for a clean new window session
    checkbox_vars = []
    selected_items = []
    
    r = tk.Toplevel(root)
    r.title("Byte and Bolt Tech Hire - New Order Page")
    r.geometry("1000x1000")
    r.configure(bg="#fff6d6")

    # Name input of applicant
    tk.Label(r, text="Enter your name:", font=("Garamond", 14, "bold"), fg="#635dff", bg="#eddea7").pack(pady=10)
    entry1 = tk.Entry(r)
    entry1.pack()

    # Item input
    tk.Label(r, text="-- Items --", font=("Garamond", 14, "bold"), fg="#635dff", bg="#eddea7").pack(pady=10)
    
    # Show items
    for i, item_data in enumerate(item_list):
        var = tk.IntVar()
        checkbox_vars.append(var)  # Track the IntVars separately
        chk = tk.Checkbutton(root, text=f"{item_data[0]} (${item_data[1]})", variable=var, compound="left", padx=10, bg="white", command=lambda i=i: process_item_data(i), font=("Arial", 10))
        chk.pack(anchor='w', pady=4)


    # Quantity button - How much of each item does the applicant want?
    tk.Label(r, text="Quantity", font=("Garamond", 14), anchor="e").pack(pady=10)

    # Save button - FIX: Pass window reference 'root' so we can close it upon saving
    save_order1 = tk.Button(r, text="Save Order", bg="#635dff", command=lambda: save_order(r))
    save_order1.pack(pady=5, padx=5)
    
    # Close new order window
    close1 = tk.Button(r, text="Close Window", bg="#e81313", command=r.destroy)
    close1.pack(pady=5)

# Save order. This function will now successfully write to your file
def save_order(window_to_close):
    global entry1, selected_items
    name_a = str(entry1.get()).strip()
    
    # Check if name is empty
    if name_a == "":
        messagebox.showerror("Error", "Please enter your name.")
        return
        
    # Check if no items were chosen
    if not selected_items:
        messagebox.showerror("Error", "Please select at least one item.")
        return

    # --- FIX: WRITE DATA TO THE FILE ---
    try:
        # 'a' appends new orders to the end of the file instead of wiping old data
        with open(filename, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            items_ordered = ", ".join(selected_items)
            f.write(f"Date: {timestamp} | Customer: {name_a} | Items: {items_ordered}\n")
        
        messagebox.showinfo("Success", "Order saved successfully!")
        window_to_close.destroy()  # Automatically close order window on save
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {str(e)}")

def show_order():
    # Check if file doesn't exist or is empty
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        messagebox.showerror("No Data", "No files or records found.")
        return
    
    with open(filename, "r") as f:
        data = f.read().strip()

    if data == "":
        messagebox.showerror("No Data", "Empty File.")
    else:
        messagebox.showinfo("Data", data)


def return_order():
    r = tk.Toplevel(root)
    r.title("Byte and Bolt Tech Hire - Return Order Page")
    r.geometry("500x500")
    r.configure(bg="#d4c893")
    tk.Label(root, text="Return Order Page", font= ("Garamond", 14, "bold"), bg="#AFA273").pack(pady=10)




    # Close return order window
    close1 = tk.Button(root, text="Close Window", bg="#e81313", command=root.destroy)
    close1.pack(pady=5)



filename = "savefile.txt"
item_list = [
    ["ACC 1 Keyboard", 20], ["ACC 1 Mouse", 15], ["Execute PC", 60], ["ARD4T 672a Laptop", 32], ["33Gi Headset", 17],
    ["ACT 2 Keyboard", 25], ["ACT 2 Mouse", 25], ["Muscle PC", 70], ["TR4G0N 884b Laptop", 38], ["36I8 Headset", 27],
    ["ANe 3 Keyboard", 15], ["ANe 3 Mouse", 10], ["Bright PC", 45], ["CRYPT 438c Laptop", 26], ["33rT Headset", 10],
    ["ARf 4 Keyboard", 22], ["ARf 4 Mouse", 17], ["Torrential PC", 65], ["TAB1TH 553d Laptop", 35], ["25yR Headset", 22]
]

# BUTTONS


tk.Label(root, text="Welcome to Byte and Bolt Tech Hire!", font=("Garamond", 20, "bold"), bg="#cbc2a3", width = 50).pack(pady=20)
# Button to New Order window
new_order = tk.Button(root, text="New Order", bg="#635dff", command=new_order, width = 25)
new_order.pack(pady=5, padx=5)

# Button to Show Order Window
show_order = tk.Button(root, text="Show Order", bg="#635dff", command=show_order, width = 25)
show_order.pack(pady=5, padx=5)

# Button to Return Order Window (under construction)
return_order = tk.Button(root, text="Return Order", bg="#635dff", command=return_order, width = 25)
return_order.pack(pady=5, padx=5)

# Button to kill the application
close_app = tk.Button(root, text="Close Application", bg="#e81313", command=root.destroy, width = 25)
close_app.pack(pady=5, padx=5)

root.mainloop()
