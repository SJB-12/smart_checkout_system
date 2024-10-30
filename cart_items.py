import tkinter as tk
from tkinter import messagebox
import csv
import os
from PIL import Image, ImageTk
import cv2

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

# Function to update the camera feed
def update_camera_feed():
    global camera_frame
    ret, frame = camera.read()
    if ret:
        # Convert frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert to Image and resize
        frame = Image.fromarray(frame)
        frame = frame.resize((400, 300), Image.LANCZOS)  # Adjust size as needed
        camera_frame = ImageTk.PhotoImage(frame)

        # Display the frame in the label
        camera_label.config(image=camera_frame)
    
    # Schedule the next frame update
    camera_label.after(10, update_camera_feed)

# Create the main window
root = tk.Tk()
root.title("Smart Checkout System")
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
user_details_label = tk.Label(left_frame, text="User Details", font=("Arial", 22, 'bold'), fg='#0A4E8E', bg='#51E2F5', anchor='w')  # Left-aligned, no bg
user_details_label.pack(pady=10, anchor='w')

name_label = tk.Label(left_frame, text="Name:", font=("Arial", 16), fg='#0A4E8E', bg='#51E2F5')
name_label.pack(anchor='w')
name_entry = tk.Entry(left_frame, font=("Arial", 16), bd=2, relief=tk.GROOVE)
name_entry.pack(pady=5, anchor='w')

phone_label = tk.Label(left_frame, text="Contact Number:", font=("Arial", 16), fg='#0A4E8E', bg='#51E2F5')
phone_label.pack(anchor='w')
phone_entry = tk.Entry(left_frame, font=("Arial", 16), bd=2, relief=tk.GROOVE)
phone_entry.pack(pady=5, anchor='w')

# Buttons for reset and submit
button_frame = tk.Frame(left_frame, bg='#51E2F5')
button_frame.pack(pady=20, anchor='w')

reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 16), bg='#FF5733', fg='white', command=reset_form)
reset_button.pack(side=tk.LEFT, padx=10)

submit_button = tk.Button(button_frame, text="Submit", font=("Arial", 16), bg='#28A745', fg='white', command=submit_form)
submit_button.pack(side=tk.LEFT, padx=10)

# Cart Items section with Add Item button on the right
cart_items_frame = tk.Frame(left_frame, bg='#51E2F5')
cart_items_frame.pack(pady=20, fill=tk.X)

cart_items_label = tk.Label(cart_items_frame, text="Cart Items", font=("Arial", 22, 'bold'), fg='#0A4E8E', bg='#51E2F5', anchor='w')
cart_items_label.pack(side=tk.LEFT)

add_item_button = tk.Button(cart_items_frame, text="+ Add Item", font=("Arial", 16), bg='#007BFF', fg='white')
add_item_button.pack(side=tk.RIGHT, padx=10)

# Right Section - Camera Feed
camera_label = tk.Label(right_frame, bg='#51E2F5')
camera_label.place(x=10, y=10, width=400, height=300)

# Initialize the webcam
camera = cv2.VideoCapture(0)

# Start updating the camera feed
update_camera_feed()

# Run the application
root.mainloop()

# Release the webcam when the application is closed
camera.release()
cv2.destroyAllWindows()
