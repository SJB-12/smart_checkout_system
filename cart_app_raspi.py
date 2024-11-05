import tkinter as tk
from PIL import Image, ImageTk
from picamera2 import Picamera2
from libcamera import controls, Transform
import time
from tkinter import messagebox
import os
import csv
import numpy as np
import cv2

# Initialize camera with correct color format
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"},
    transform=Transform(vflip=False, hflip=False)
)
picam2.configure(preview_config)
picam2.set_controls({"AwbEnable": True})
picam2.set_controls({"ColourGains": (1.0, 1.0)})
picam2.start()
time.sleep(1)

# Define the resolution for the application
root = tk.Tk()
root.title("Smart Checkout System")

# Set fixed window size instead of fullscreen
root.geometry("1080x720")
# Center the window
root.update_idletasks()
width = 1080
height = 720
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

# Adjust paths for Raspberry Pi
script_dir = os.path.dirname(os.path.abspath(__file__))

# bg of the application
bg_image = Image.open(os.path.join(script_dir, "assets", "bg_img.jpg"))
bg_image = bg_image.resize((1080, 720), Image.Resampling.LANCZOS)
bg = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=1080, height=720)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")

# Making the main frame
main_frame = Image.open(os.path.join(script_dir, "assets", "main_frame.png"))
main_frame = main_frame.resize((1000, 650), Image.Resampling.LANCZOS)
main_frame_bg = ImageTk.PhotoImage(main_frame)
canvas.create_image(40, 25, image=main_frame_bg, anchor="nw")

# Making heading frame
heading_frame = Image.open(os.path.join(script_dir, "assets", "heading_frame.png"))
heading_frame = heading_frame.resize((980, 70), Image.Resampling.LANCZOS)
heading_frame_bg = ImageTk.PhotoImage(heading_frame)
canvas.create_image(50, 40, image=heading_frame_bg, anchor="nw")

# Making 1st frame on left side
frame_1 = Image.open(os.path.join(script_dir, "assets", "frame_1.png"))
frame_1 = frame_1.resize((480, 200), Image.Resampling.LANCZOS)
frame1_bg = ImageTk.PhotoImage(frame_1)
canvas.create_image(50, 140, image=frame1_bg, anchor="nw")

# Defining forms in the 1st frame
name_label = tk.Label(
    root,
    text="Name:",
    font=("Arial", 14),
    bg="#ffffff"
)
name_label.place(x=70, y=200)

name_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=25,
    bd=2,
    relief="groove"
)
name_entry.place(x=180, y=200)

contact_label = tk.Label(
    root,
    text="Contact No.:",
    font=("Arial", 14),
    bg="#ffffff"
)
contact_label.place(x=70, y=240)

contact_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=25,
    bd=2,
    relief="groove"
)
contact_entry.place(x=180, y=240)

# Making 2nd frame on left side
frame_2 = Image.open(os.path.join(script_dir, "assets", "frame_2.png"))
frame_2 = frame_2.resize((480, 300), Image.Resampling.LANCZOS)
frame2_bg = ImageTk.PhotoImage(frame_2)
canvas.create_image(50, 360, image=frame2_bg, anchor="nw")

# Making 3rd frame for camera
frame_3 = tk.Canvas(root, width=480, height=520)
frame_3.place(x=550, y=140)

frame_3_image = Image.open(os.path.join(script_dir, "assets", "frame_3.png"))
frame_3_image = frame_3_image.resize((480, 520), Image.Resampling.LANCZOS)
frame3_bg = ImageTk.PhotoImage(frame_3_image)
frame_3.create_image(0, 0, image=frame3_bg, anchor="nw")

def show_camera():
    # Capture frame from PiCamera2
    frame = picam2.capture_array()
    
    # Convert to PIL Image directly (since we're capturing in RGB888 format)
    img = Image.fromarray(frame)
    
    # Resize to fit the frame
    img = img.resize((420, 310), Image.Resampling.LANCZOS)
    
    # Convert to PhotoImage
    imgtk = ImageTk.PhotoImage(image=img)
    
    # Update camera label
    camera_label.imgtk = imgtk
    camera_label.configure(image=imgtk)
    
    # Schedule next update
    camera_label.after(10, show_camera)

# Create camera label
camera_label = tk.Label(frame_3)
camera_label.place(x=30, y=90, width=420, height=310)
show_camera()

def initialize_csv():
    csv_file = os.path.join(script_dir, "customer_details.csv")
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Contact"])
    return csv_file

def submit_action():
    name = name_entry.get().strip()
    contact = contact_entry.get().strip()
    
    if not name or not contact:
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    
    if not contact.isdigit() or len(contact) != 10:
        messagebox.showerror("Error", "Please enter a valid 10-digit contact number!")
        return
    
    csv_file = initialize_csv()
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, contact])
    
    messagebox.showinfo("Success", "Details saved successfully!")
    reset_action()

def reset_action():
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    name_entry.focus()

def cleanup():
    picam2.stop()
    root.destroy()

# Button images
submit_button = Image.open(os.path.join(script_dir, "assets", "Submit_button.png"))
submit_button = submit_button.resize((100, 35), Image.Resampling.LANCZOS)
submit_bg = ImageTk.PhotoImage(submit_button)
sbutton = tk.Button(root, image=submit_bg, command=submit_action, borderwidth=0)
sbutton.place(x=70, y=290)

reset_button = Image.open(os.path.join(script_dir, "assets", "Reset_button.png"))
reset_button = reset_button.resize((100, 35), Image.Resampling.LANCZOS)
reset_bg = ImageTk.PhotoImage(reset_button)
rbutton = tk.Button(root, image=reset_bg, command=reset_action, borderwidth=0)
rbutton.place(x=180, y=290)

add_button = Image.open(os.path.join(script_dir, "assets", "Add_button.png"))
add_button = add_button.resize((150, 50), Image.Resampling.LANCZOS)
add_bg = ImageTk.PhotoImage(add_button)
abutton = tk.Button(root, image=add_bg, command=lambda: None, borderwidth=0)
abutton.place(x=580, y=570)

# Bind cleanup function to window closing
root.protocol("WM_DELETE_WINDOW", cleanup)

root.mainloop()