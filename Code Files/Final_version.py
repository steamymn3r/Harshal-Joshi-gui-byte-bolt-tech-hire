# Author: Harshal Joshi
# Purpose: To create a GUI application for Byte and Bolt Tech Hire
# Date (first edited): 29/05/2026


# Import spam here
import os
os.environ["TK_SILENCE_DEPRECATION"] = "1"
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import random
from datetime import date, datetime
from pathlib import Path
import re

# Main root - basically a starter for all GUI frames
root = tk.Tk()
root.title("Byte & Bolt Tech Hire")
root.geometry("500x600")


## Main menu - GUI's first frame
main_menu_frame = tk.Frame(root, bg="#aeb0b1", borderwidth=10, relief="ridge")
tk.Label(main_menu_frame, text=" Byte and Bolt Tech Hire", font=("Garamond", 18, "bold"), bg="#bdbdbd").pack(pady=20)

# Buttons to use to get around the program
tk.Button(main_menu_frame, text="New Order", bg="#635dff", fg="white", width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Show Orders", bg="#635dff", fg="white", width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Return Orders", bg="#635dff", fg="white", width=25).pack(pady=5)
tk.Button(main_menu_frame, text="Exit", bg="#e81313", fg="white", command=root.destroy, width=25).pack(pady=5)

## New Order - Ordering and checkout frame.
new_order_frame = tk.Frame(root, bg="#9e9e9e", borderwidth=10, relief="ridge")
tk.Label(new_order_frame, text = "New Order", font=("Garamond", 18, "bold"), bg="#9aa0a7").pack(pady=5)

# Entry fields: Name, Quantity
entry_name1 = tk.Entry(new_order_frame)
entry_name1.insert(0, "Enter Name")
entry_name1.pack(pady=2)

entry_quantity1 = tk.Entry(new_order_frame)
entry_quantity1.insert(0, "Enter Quantity")
entry_quantity1.pack(pady=2)

# Date picker - calculates next date, allows for ordering upto 2 weeks in advance
 


root.mainloop()