import tkinter as tk
from tkinter import messagebox
import csv
from PIL import Image, ImageTk

# Function to reset the form
def reset_form():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

# Function to submit the form and save data to CSV
def submit_form():
    name = name_entry.get()
    phone = phone_entry.get()
    
    if name and phone:
        with open('user_cart_items.csv', 'a', newline='') as csvfile:
            fieldnames = ['Name', 'Phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Name': name, 'Phone': phone})
        messagebox.showinfo("Success", "Data submitted successfully!")
        reset_form()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

# Create the main window
root = tk.Tk()
root.title("User Cart Items")
root.geometry("1080x720")
root.resizable(False, False)

# Load the background image
bg_image = Image.open(r"D:\projects\smart_checkout_system\bg_img.jpg")
bg_image = bg_image.resize((1080, 720), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Label to display the background image
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame for the content
content_frame = tk.Frame(root, bg='blue', bd=10, relief=tk.RAISED)
content_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

# User Details section
user_details_label = tk.Label(content_frame, text="User Details", font=("Arial", 18), bg='blue', fg='white')
user_details_label.pack(pady=10)

name_label = tk.Label(content_frame, text="Name:", font=("Arial", 14), bg='blue', fg='white')
name_label.pack()
name_entry = tk.Entry(content_frame, font=("Arial", 14))
name_entry.pack(pady=5)

phone_label = tk.Label(content_frame, text="Contact Number:", font=("Arial", 14), bg='blue', fg='white')
phone_label.pack()
phone_entry = tk.Entry(content_frame, font=("Arial", 14))
phone_entry.pack(pady=5)

# Buttons for reset and submit
button_frame = tk.Frame(content_frame, bg='blue')
button_frame.pack(pady=20)

reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 14), bg='blue', fg='white', command=reset_form)
reset_button.pack(side=tk.LEFT, padx=10)

submit_button = tk.Button(button_frame, text="Submit", font=("Arial", 14), bg='blue', fg='white', command=submit_form)
submit_button.pack(side=tk.LEFT, padx=10)

# Cart Items section
cart_items_label = tk.Label(content_frame, text="Cart Items", font=("Arial", 18), bg='blue', fg='white')
cart_items_label.pack(pady=20)

add_item_button = tk.Button(content_frame, text="+ Add Item", font=("Arial", 14), bg='blue', fg='white')
add_item_button.pack(pady=5)

# Run the application
root.mainloop()
