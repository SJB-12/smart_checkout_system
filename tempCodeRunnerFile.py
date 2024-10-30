import tkinter as tk
from tkinter import messagebox
import csv
import os
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
        file_exists = os.path.isfile('user_cart_items.csv')
        
        with open('user_cart_items.csv', 'a', newline='') as csvfile:
            fieldnames = ['Name', 'Phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:  # Write header only if the file does not exist
                writer.writeheader()
            
            writer.writerow({'Name': name, 'Phone': phone})
        
        messagebox.showinfo("Success", "Data submitted successfully!")
        reset_form()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

# Function to create rounded corners on canvas
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

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

# Create a canvas for rounded corner sections
canvas = tk.Canvas(root, bg="white", highlightthickness=0)
canvas.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

# Draw the left rounded rectangle
create_rounded_rectangle(canvas, 20, 20, 480, 680, radius=50, fill='#51E2F5')

# Draw the right rounded rectangle
create_rounded_rectangle(canvas, 500, 20, 980, 680, radius=50, fill='#51E2F5')

# Create a frame inside the left rounded rectangle (for the left section)
left_frame = tk.Frame(canvas, bg='#51E2F5')
left_frame.place(x=40, y=40, width=420, height=640)

# Create a frame inside the right rounded rectangle (for the right section)
right_frame = tk.Frame(canvas, bg='#51E2F5')
right_frame.place(x=520, y=40, width=420, height=640)

# Left Section - User Details and Cart Items
user_details_label = tk.Label(left_frame, text="User Details", font=("Arial", 18), fg='white', bg='#51E2F5', anchor='w')  # Left-aligned, no bg
user_details_label.pack(pady=10, anchor='w')

name_label = tk.Label(left_frame, text="Name:", font=("Arial", 14), fg='white', bg='#51E2F5')
name_label.pack(anchor='w')
name_entry = tk.Entry(left_frame, font=("Arial", 14))
name_entry.pack(pady=5, anchor='w')

phone_label = tk.Label(left_frame, text="Contact Number:", font=("Arial", 14), fg='white', bg='#51E2F5')
phone_label.pack(anchor='w')
phone_entry = tk.Entry(left_frame, font=("Arial", 14))
phone_entry.pack(pady=5, anchor='w')

# Buttons for reset and submit
button_frame = tk.Frame(left_frame, bg='#51E2F5')
button_frame.pack(pady=20, anchor='w')

reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 14), bg='blue', fg='white', command=reset_form)
reset_button.pack(side=tk.LEFT, padx=10)

submit_button = tk.Button(button_frame, text="Submit", font=("Arial", 14), bg='blue', fg='white', command=submit_form)
submit_button.pack(side=tk.LEFT, padx=10)

# Cart Items section with Add Item button on the right
cart_items_frame = tk.Frame(left_frame, bg='#51E2F5')
cart_items_frame.pack(pady=20, fill=tk.X)

cart_items_label = tk.Label(cart_items_frame, text="Cart Items", font=("Arial", 18), fg='white', bg='#51E2F5', anchor='w')
cart_items_label.pack(side=tk.LEFT)

add_item_button = tk.Button(cart_items_frame, text="+ Add Item", font=("Arial", 14), bg='blue', fg='white')
add_item_button.pack(side=tk.RIGHT, padx=10)

# Right Section - Camera Placeholder aligned to the top-left corner
camera_placeholder_label = tk.Label(right_frame, text="Camera Feed Placeholder", font=("Arial", 18), fg='white', bg='#51E2F5', anchor='nw')
camera_placeholder_label.place(x=10, y=10)

# Run the application
root.mainloop()
