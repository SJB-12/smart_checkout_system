import tkinter as tk
from PIL import Image, ImageTk

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

left_frame = tk.Frame(root, width=420, height=550, bg="lightblue")
right_frame = tk.Frame(root, width=420, height=550, bg="lightgreen")


canvas.create_window(100, 150, anchor="nw", window=left_frame)   # Left frame position
canvas.create_window(600, 150, anchor="nw", window=right_frame)


root.mainloop()
