import tkinter as tk
from tkinter import messagebox
import os
import datetime

# main window base template
root = tk.Tk()
root.title("Byte & Bolt Tech Hire (Home Page)")
root.geometry("500x500")
root.configure(bg="#e8e2c8")


def process_item_data(index):
    if selected_items[index].get():
        selected_items.append(item_list[index][0])
    else:
        if item_list[index][0] in selected_items:
            selected_items.remove(item_list[index][0])

item_var = 0
selected_items = []
entry1 = 0

# New order. This function will allow the user to place a new order.
def n_o():
    r = tk.Toplevel(root)
    r.title("Byte and Bolt Tech Hire - New Order Page")
    r.geometry("1000x1000")
    r.configure(bg="#fff6d6")

    # Name input of applicant
    tk.Label(r, text = "Enter your name:", font = ("Garamond", 14, "bold"), fg = "#635dff", bg= "#eddea7").pack(pady=10)
    entry1 = tk.Entry(r)
    entry1.pack()
    name = str(entry1.get())

    # Item input
    tk.Label(r,text="-- Items --", font = ("Garamond", 14, "bold"),fg = "#635dff", bg = "#eddea7").pack(pady=10)
    
    # Show items
    for i, (items) in enumerate(item_list):
        var=tk.IntVar()
        selected_items.append(var)
        chk = tk.Checkbutton(r, text=items, variable=var, compound="left", padx=10, bg="white", command= lambda i=i:process_item_data(i), font=("Arial",10))
        chk.pack(anchor='w', pady=4)

    # Save button
    save_order1 = tk.Button(r, text = "Save Order", bg = "#635dff", command=s_o)
    save_order1.pack(pady=5, padx=5)

    
    # Close new order window
    close1 = tk.Button(r,text = "Close Window", bg = "#e81313", command=r.destroy)
    close1.pack(pady=5)


# Save order. This function will allow the program to save orders
def s_o():
    global entry1, item_var, selected_items
    item_var = selected_items
    entry1 = entry1.get()
    # Check if name is empty
    if entry1 == "":
        tk.messagebox.showerror("Error", "Please enter your name.")
        return




def show_o():
    if os.path.exists(filename) == False:
        messagebox.showerror("No Data", "No file")
        return
    
    f= open(filename, "r")
    data = f.read()
    f.close()

    if data == " ":
        messagebox.showerror("No Data", "Empty File.")
        return
    
    else:
        messagebox.showinfo("Data", data)





""" DECLARE LIST OF ITEMS, PRICES, AND MAIN FUNCTIONS. Prices are going to be calculated on a 10% day to day basis,  
meaning the price of the hired quantity will increase day by day by 10%. E.g. the ACC 1 Keyboard has a renting 
price of $10, which means per day rented, the cost price will increase by 10%. If rented for a whole 7 days,
the rent price will be $17, as 10 * 10% is $1 and 1 * 7 is 7, 7+10 = 17."""


filename = "savefile.txt"
item_list = [
    
             # SET 1
             ["ACC 1 Keyboard", 20],
             ["ACC 1 Mouse", 15],
             ["Execute PC", 60],
             ["ARD4T 672a Laptop", 32],
             ["33Gi Headset", 17],
             # SET 2
             ["ACT 2 Keyboard", 25],
             ["ACT 2 Mouse", 25],
             ["Muscle PC", 70],
             ["TR4G0N 884b Laptop", 38],
             ["36I8 Headset", 27],
             # SET 3
             ["ANe 3 Keyboard", 15],
             ["ANe 3 Mouse", 10],
             ["Bright PC", 45],
             ["CRYPT 438c Laptop", 26],
             ["33rT Headset", 10],
             # SET 4
             ["ARf 4 Keyboard", 22],
             ["ARf 4 Mouse", 17],
             ["Torrential PC", 65],
             ["TAB1TH 553d Laptop", 35],
             ["25yR Headset", 22]
             ]
cart = []


# BUTTONS
new_order = tk.Button(root, text = "New Order", bg = "#635dff", command = n_o)
new_order.pack(pady=5, padx=5)


show_order = tk.Button(root, text = "Show Order", bg = "#635dff", command = show_o)
show_order.pack(pady=5, padx=5)


close_app = tk.Button(root, text = "Close Application", bg = "#e81313", command = root.destroy)
close_app.pack(pady=5, padx=5)


# Main menu. This acts as a central hub between different functions in the program, such as new order to return order, etc
#def main_menu():

# Return order. This function will allow the user to return their order.
#def return_order():






# Show order. This function will allow the user to view all orders, completed and current. This will also allow the user to delete or edit the orders.
#def show_order():

root.mainloop()