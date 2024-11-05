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
import torch
import yaml

class SmartCheckout:
    def __init__(self):
        # Initialize variables first
        self.detected_items = []
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Setup main window first
        self.root = tk.Tk()
        self.root.title("Smart Checkout System")
        self.root.geometry("1080x720")
        
        # Center window
        width = 1080
        height = 720
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        # Initialize camera before setting up GUI
        self.setup_camera()
        
        # Initialize YOLO model
        self.model = self.load_yolo_model()
        
        # Setup GUI components
        self.setup_frames()
        self.setup_forms()
        self.setup_buttons()

    def load_yolo_model(self):
        try:
            # Update these paths to your trained model and data.yaml
            weights_path = "runs/train/exp/weights/best.pt"
            data_yaml = "dataset_config.yaml"
            
            # Load class names
            with open(data_yaml, 'r') as f:
                self.class_names = yaml.safe_load(f)['names']
            
            # Load model
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path)
            model.conf = 0.25  # Confidence threshold
            print("YOLO model loaded successfully")
            return model
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            return None

    def setup_camera(self):
        try:
            self.picam2 = Picamera2()
            preview_config = self.picam2.create_preview_configuration(
                main={"size": (640, 480), "format": "RGB888"},
                transform=Transform(vflip=False, hflip=False)
            )
            self.picam2.configure(preview_config)
            self.picam2.set_controls({"AwbEnable": True})
            self.picam2.set_controls({"ColourGains": (1.0, 1.0)})
            self.picam2.start()
            time.sleep(1)
            print("Camera initialized successfully")
        except Exception as e:
            print(f"Error initializing camera: {e}")
            messagebox.showerror("Error", "Failed to initialize camera!")
            self.root.destroy()
            exit(1)

    def setup_frames(self):
        try:
            # Background
            bg_image = Image.open(os.path.join(self.script_dir, "assets", "bg_img.jpg"))
            bg_image = bg_image.resize((1080, 720), Image.Resampling.LANCZOS)
            self.bg = ImageTk.PhotoImage(bg_image)

            self.canvas = tk.Canvas(self.root, width=1080, height=720)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

            # Main frame
            main_frame = Image.open(os.path.join(self.script_dir, "assets", "main_frame.png"))
            main_frame = main_frame.resize((1000, 650), Image.Resampling.LANCZOS)
            self.main_frame_bg = ImageTk.PhotoImage(main_frame)
            self.canvas.create_image(40, 25, image=self.main_frame_bg, anchor="nw")

            # Heading frame
            heading_frame = Image.open(os.path.join(self.script_dir, "assets", "heading_frame.png"))
            heading_frame = heading_frame.resize((980, 70), Image.Resampling.LANCZOS)
            self.heading_frame_bg = ImageTk.PhotoImage(heading_frame)
            self.canvas.create_image(50, 40, image=self.heading_frame_bg, anchor="nw")

            # Frame 1 (Customer Details)
            frame_1 = Image.open(os.path.join(self.script_dir, "assets", "frame_1.png"))
            frame_1 = frame_1.resize((480, 200), Image.Resampling.LANCZOS)
            self.frame1_bg = ImageTk.PhotoImage(frame_1)
            self.canvas.create_image(50, 140, image=self.frame1_bg, anchor="nw")

            # Frame 2 (Items List)
            frame_2 = Image.open(os.path.join(self.script_dir, "assets", "frame_2.png"))
            frame_2 = frame_2.resize((480, 300), Image.Resampling.LANCZOS)
            self.frame2_bg = ImageTk.PhotoImage(frame_2)
            self.canvas.create_image(50, 360, image=self.frame2_bg, anchor="nw")

            # Frame 3 (Camera Feed)
            self.frame_3 = tk.Canvas(self.root, width=480, height=520)
            self.frame_3.place(x=550, y=140)

            frame_3_image = Image.open(os.path.join(self.script_dir, "assets", "frame_3.png"))
            frame_3_image = frame_3_image.resize((480, 520), Image.Resampling.LANCZOS)
            self.frame3_bg = ImageTk.PhotoImage(frame_3_image)
            self.frame_3.create_image(0, 0, image=self.frame3_bg, anchor="nw")

            # Create items listbox in frame 2
            self.items_listbox = tk.Listbox(
                self.root,
                font=("Arial", 12),
                width=40,
                height=10,
                bg='white'
            )
            self.items_listbox.place(x=70, y=380)

            # Add label above listbox
            self.items_label = tk.Label(
                self.root,
                text="Detected Items:",
                font=("Arial", 12, "bold"),
                bg='white'
            )
            self.items_label.place(x=70, y=355)

            # Create camera label
            self.camera_label = tk.Label(self.frame_3)
            self.camera_label.place(x=30, y=90, width=420, height=310)
            
        except Exception as e:
            print(f"Error setting up frames: {e}")
            messagebox.showerror("Error", "Failed to setup application frames!")
            self.cleanup()

    def setup_forms(self):
        # Name input
        self.name_label = tk.Label(
            self.root,
            text="Name:",
            font=("Arial", 14),
            bg="#ffffff"
        )
        self.name_label.place(x=70, y=200)

        self.name_entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            width=25,
            bd=2,
            relief="groove"
        )
        self.name_entry.place(x=180, y=200)

        # Contact input
        self.contact_label = tk.Label(
            self.root,
            text="Contact No.:",
            font=("Arial", 14),
            bg="#ffffff"
        )
        self.contact_label.place(x=70, y=240)

        self.contact_entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            width=25,
            bd=2,
            relief="groove"
        )
        self.contact_entry.place(x=180, y=240)

    def setup_buttons(self):
        try:
            # Submit button
            submit_button = Image.open(os.path.join(self.script_dir, "assets", "Submit_button.png"))
            submit_button = submit_button.resize((100, 35), Image.Resampling.LANCZOS)
            self.submit_bg = ImageTk.PhotoImage(submit_button)
            self.sbutton = tk.Button(
                self.root,
                image=self.submit_bg,
                command=self.submit_action,
                borderwidth=0
            )
            self.sbutton.place(x=70, y=290)

            # Reset button
            reset_button = Image.open(os.path.join(self.script_dir, "assets", "Reset_button.png"))
            reset_button = reset_button.resize((100, 35), Image.Resampling.LANCZOS)
            self.reset_bg = ImageTk.PhotoImage(reset_button)
            self.rbutton = tk.Button(
                self.root,
                image=self.reset_bg,
                command=self.reset_action,
                borderwidth=0
            )
            self.rbutton.place(x=180, y=290)

            # Add item button
            add_button = Image.open(os.path.join(self.script_dir, "assets", "Add_button.png"))
            add_button = add_button.resize((150, 50), Image.Resampling.LANCZOS)
            self.add_bg = ImageTk.PhotoImage(add_button)
            self.abutton = tk.Button(
                self.root,
                image=self.add_bg,
                command=self.add_detected_item,
                borderwidth=0
            )
            self.abutton.place(x=580, y=570)
            
        except Exception as e:
            print(f"Error setting up buttons: {e}")
            messagebox.showerror("Error", "Failed to setup buttons!")
            self.cleanup()

    def detect_objects(self, frame):
        if self.model is None:
            return []
        
        try:
            # Run inference
            results = self.model(frame)
            
            # Process results
            detections = []
            if len(results.pred[0]):
                for *xyxy, conf, cls in results.pred[0]:
                    class_id = int(cls)
                    confidence = float(conf)
                    class_name = self.class_names[class_id]
                    detections.append({
                        'class': class_name,
                        'confidence': confidence,
                        'bbox': [int(x) for x in xyxy]
                    })
            
            return detections
        except Exception as e:
            print(f"Error in object detection: {e}")
            return []

    def draw_detections(self, frame, detections):
        try:
            img = frame.copy()
            for det in detections:
                x1, y1, x2, y2 = det['bbox']
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{det['class']} {det['confidence']:.2f}"
                cv2.putText(img, label, (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            return img
        except Exception as e:
            print(f"Error drawing detections: {e}")
            return frame

    def show_camera(self):
        try:
            # Capture frame
            frame = self.picam2.capture_array()
            
            # Run detection
            detections = self.detect_objects(frame)
            
            # Store latest detections
            self.current_detections = detections
            
            # Draw detections
            frame = self.draw_detections(frame, detections)
            
            # Convert to PIL Image
            img = Image.fromarray(frame)
            img = img.resize((420, 310), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update camera label
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
            
            # Schedule next update
            self.camera_label.after(10, self.show_camera)
            
        except Exception as e:
            print(f"Error in camera feed: {e}")
            self.camera_label.after(1000, self.show_camera)  # Retry after 1 second

    def add_detected_item(self):
        if hasattr(self, 'current_detections') and self.current_detections:
            for detection in self.current_detections:
                item = f"{detection['class']} ({detection['confidence']:.2f})"
                if item not in self.detected_items:
                    self.detected_items.append(item)
                    self.items_listbox.insert(tk.END, item)

    def submit_action(self):
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        
        if not name or not contact:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        if not contact.isdigit() or len(contact) != 10:
            messagebox.showerror("Error", "Please enter a valid 10-digit contact number!")
            return
        
        if not self.detected_items:
            messagebox.showwarning("Warning", "No items have been added!")
            return
        
        try:
            # Save to CSV with detected items
            csv_file = self.initialize_csv()
            with open(csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                items_str = ', '.join(self.detected_items)
                writer.writerow([name, contact, items_str])
            
            messagebox.showinfo("Success", "Details and items saved successfully!")
            self.reset_action()
            
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            messagebox.showerror("Error", "Failed to save details!")

    def reset_action(self):
        self.name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.items_listbox.delete(0, tk.END)
        self.detected_items = []
        self.name_entry.focus()

    def initialize_csv(self):
        csv_file = os.path.join(self.script_dir, "customer_details.csv")
        if not os.path.exists(csv_file):
            with open(csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Contact", "Items"])
        return csv_file

    def cleanup(self):
        try:
            if hasattr(self, 'picam2'):
                self.picam2.stop()
            self.root.destroy()
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def run(self):
        try:
            # Start camera feed
            self.show_camera()
            
            # Bind cleanup
            self.root.protocol("WM_DELETE_WINDOW", self.cleanup)
            
            # Start main loop
            self.root.mainloop()
        except Exception as e:
            print(f"Error running application: {e}")
            self.cleanup()

if __name__ == "__main__":
    try:
        print("Starting Smart Checkout System...")
        app = SmartCheckout()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")