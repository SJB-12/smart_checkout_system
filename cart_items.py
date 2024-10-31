import tkinter as tk
from PIL import Image, ImageTk
import cv2

root= tk.Tk()
root.title("Smart Checkout System")
root.geometry("1080x720")



bg_image = Image.open(r"C:\Users\Suman_PC\Documents\GitHub\smart_checkout_system\assets\bg_img.jpg")
bg_image = bg_image.resize((1080, 720), Image.ANTIALIAS)

bg = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width = 1080, height = 720)
canvas.pack(fill = "both", expand = True)

canvas.create_image(0,0,image = bg, anchor="nw")


main_frame = Image.open(r"C:\Users\Suman_PC\Documents\GitHub\smart_checkout_system\assets\main_frame.png")
main_frame = main_frame.resize((1000, 650), Image.ANTIALIAS)
main_frame_bg = ImageTk.PhotoImage(main_frame)

canvas.create_image(40,25, image=main_frame_bg,anchor="nw")

heading_frame = Image.open(r"C:\Users\Suman_PC\Documents\GitHub\smart_checkout_system\assets\heading_frame.png")
heading_frame = heading_frame.resize((980,70), Image.ANTIALIAS)
heading_frame_bg = ImageTk.PhotoImage(heading_frame)

canvas.create_image(50,40, image = heading_frame_bg,anchor = "nw")

frame_1 = Image.open(r"C:\Users\Suman_PC\Documents\GitHub\smart_checkout_system\assets\frame_1.png")
frame_1 = frame_1.resize((480,200), Image.ANTIALIAS)
frame1_bg = ImageTk.PhotoImage(frame_1)

canvas.create_image(50,140, image = frame1_bg,anchor = "nw")

frame_2 = Image.open(r"C:\Users\Suman_PC\Documents\GitHub\smart_checkout_system\assets\frame_2.png")
frame_2 = frame_2.resize((480,300), Image.ANTIALIAS)
frame2_bg = ImageTk.PhotoImage(frame_2)

canvas.create_image(50,360, image = frame2_bg,anchor = "nw")

frame_3 = tk.Canvas(root, width=480, height=520)
frame_3.place(x=550, y=140)

# Add background image to frame_3
frame_3_image = Image.open(r"C:\Users\Suman_PC\Documents\GitHub\smart_checkout_system\assets\frame_3.png")
frame_3_image = frame_3_image.resize((480, 520), Image.ANTIALIAS)
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

def submit_action():
    name = name_entry.get()
    contact = contact_entry.get()
    
    # Append data to CSV file
    with open('details.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, contact])
    
    # Clear entry fields after submission
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)

def reset_action():
    # Clear entry fields
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)



submit_button = Image.open(r"C:\Users\Suman_PC\Documents\GitHub\smart_checkout_system\assets\Submit_button.png")
submit_button = submit_button.resize((110, 40), Image.ANTIALIAS)
submit_bg = ImageTk.PhotoImage(submit_button)
sbutton = tk.Button(root, image=submit_bg, command=submit_action, borderwidth=0)
sbutton.place(x=70, y=280)

reset_button = Image.open(r"C:\Users\Suman_PC\Documents\GitHub\smart_checkout_system\assets\Reset_button.png")
reset_button = reset_button.resize((110, 40), Image.ANTIALIAS)
reset_bg = ImageTk.PhotoImage(reset_button)
rbutton = tk.Button(root, image=reset_bg, command=reset_action, borderwidth=0)
rbutton.place(x=200, y=280)

add_button = Image.open(r"C:\Users\Suman_PC\Documents\GitHub\smart_checkout_system\assets\Add_button.png")
add_button = add_button.resize((150, 50), Image.ANTIALIAS)
add_bg = ImageTk.PhotoImage(add_button)

abutton = tk.Button(root, image=add_bg, command=button_action, borderwidth=0)
abutton.place(x=580, y=570)



root.mainloop()
