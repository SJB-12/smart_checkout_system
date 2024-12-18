import tkinter as tk
from PIL import Image, ImageTk
import cv2
from tkinter import messagebox
import os
import csv

#defining the resolution for the application
root= tk.Tk()
root.title("Smart Checkout System")
root.geometry("1080x720")

#bg of the application
bg_image = Image.open(r"assets\bg_img.jpg")
bg_image = bg_image.resize((1080, 720), Image.Resampling.LANCZOS)

bg = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width = 1080, height = 720)
canvas.pack(fill = "both", expand = True)

canvas.create_image(0,0,image = bg, anchor="nw")

#making the main frame
main_frame = Image.open(r"assets\main_frame.png")
main_frame = main_frame.resize((1000, 650), Image.Resampling.LANCZOS)
main_frame_bg = ImageTk.PhotoImage(main_frame)

canvas.create_image(40,25, image=main_frame_bg,anchor="nw")

#making heading frame
heading_frame = Image.open(r"assets\heading_frame.png")
heading_frame = heading_frame.resize((980,70), Image.Resampling.LANCZOS)
heading_frame_bg = ImageTk.PhotoImage(heading_frame)
canvas.create_image(50,40, image = heading_frame_bg,anchor = "nw")

#making 1st frame on left side
frame_1 = Image.open(r"assets\frame_1.png")
frame_1 = frame_1.resize((480,200), Image.Resampling.LANCZOS)
frame1_bg = ImageTk.PhotoImage(frame_1)
canvas.create_image(50,140, image = frame1_bg,anchor = "nw")

#defining forms in the 1st frame
name_label = tk.Label(
    root, 
    text="Name:", 
    font=("Arial", 14),
    bg="#ffffff"  # White background to match frame
)
name_label.place(x=70, y=200)  # Adjust coordinates as needed

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
    bg="#ffffff"  # White background to match frame
)
contact_label.place(x=70, y=240)  # Adjust coordinates as needed

contact_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=25,
    bd=2,
    relief="groove"
)
contact_entry.place(x=180, y=240)

#making 2nd frame on left side of the main frame
frame_2 = Image.open(r"assets\frame_2.png")
frame_2 = frame_2.resize((480,300), Image.Resampling.LANCZOS)
frame2_bg = ImageTk.PhotoImage(frame_2)
canvas.create_image(50,360, image = frame2_bg,anchor = "nw")

#making 3rd frame on right side of the main frame
frame_3 = tk.Canvas(root, width=480, height=520)
frame_3.place(x=550, y=140)

# Add background image to frame_3
frame_3_image = Image.open(r"assets\frame_3.png")
frame_3_image = frame_3_image.resize((480, 520), Image.Resampling.LANCZOS)
frame3_bg = ImageTk.PhotoImage(frame_3_image)
frame_3.create_image(0, 0, image=frame3_bg, anchor="nw")

# Initialize camera
cap = cv2.VideoCapture(0)

def show_camera():
    ret, frame = cap.read()  # Capture frame-by-frame
    if ret:
        # Convert the frame to RGB format (Tkinter uses RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update camera label with new frame
        camera_label.imgtk = imgtk  # Keep a reference
        camera_label.config(image=imgtk)

    # Schedule the function to run again after a short delay
    camera_label.after(10, show_camera)

# Create a Label widget on frame_3 to display the camera feed
camera_label = tk.Label(frame_3)
camera_label.place(x=30, y=90, width=420, height=310)  # Adjust as necessary
show_camera()

canvas.create_image(550,140, image = frame3_bg,anchor = "nw")

def button_action():
    print("Button clicked!")


def initialize_csv():
    csv_file = "customer_details.csv"
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Contact"])  # Write headers
    return csv_file

# Modified button_action function for submit button
def submit_action():
    name = name_entry.get().strip()
    contact = contact_entry.get().strip()
    
    # Input validation
    if not name or not contact:
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    
    # Validate contact number (assuming Indian phone number format)
    if not contact.isdigit() or len(contact) != 10:
        messagebox.showerror("Error", "Please enter a valid 10-digit contact number!")
        return
    
    try:
        csv_file = initialize_csv()
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, contact])
        
        messagebox.showinfo("Success", "Details saved successfully!")
        reset_action()  # Clear the form after successful submission
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Modified reset_action function
def reset_action():
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    name_entry.focus()  # Set focus back to name field

#submit button in 1st frame
submit_button = Image.open(r"assets\Submit_button.png")
submit_button = submit_button.resize((100, 35), Image.Resampling.LANCZOS)
submit_bg = ImageTk.PhotoImage(submit_button)
sbutton = tk.Button(root, image=submit_bg, command=submit_action, borderwidth=0)
sbutton.place(x=70, y=290)

#reset button in 2nd frame
reset_button = Image.open(r"assets\Reset_button.png")
reset_button = reset_button.resize((100, 35), Image.Resampling.LANCZOS)
reset_bg = ImageTk.PhotoImage(reset_button)
rbutton = tk.Button(root, image=reset_bg, command=reset_action, borderwidth=0)
rbutton.place(x=180, y=290)

#add button in 3rd frame
add_button = Image.open(r"assets\Add_button.png")
add_button = add_button.resize((150, 50), Image.Resampling.LANCZOS)
add_bg = ImageTk.PhotoImage(add_button)
abutton = tk.Button(root, image=add_bg, command=button_action, borderwidth=0)
abutton.place(x=580, y=570)

root.mainloop()
