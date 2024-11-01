import os
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import shutil
from pathlib import Path
import time
import yaml

class ImageLabeler:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.classes = self._get_classes()
        if not self.classes:
            raise ValueError("No classes found in dataset directory!")
            
        print(f"Found classes: {self.classes}")
        
        self.current_class = 0
        self.current_image_index = 0
        self.images = []
        self.current_image = None
        self.drawing = False
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        self.image_width = 800
        self.image_height = 600
        
        # Setup directories with timestamp
        self.timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.setup_directories()
        
        # Save class information
        self.save_class_info()
        
        # Setup GUI
        self.setup_gui()

    def _get_classes(self):
        """Get class names from dataset folders"""
        classes = [folder for folder in sorted(os.listdir(self.dataset_path)) 
                  if os.path.isdir(os.path.join(self.dataset_path, folder))]
        return classes

    def setup_directories(self):
        """Create YOLO format directories"""
        self.yolo_path = Path(f'yolo_dataset_{self.timestamp}')
        for split in ['train', 'valid']:
            (self.yolo_path / split / 'images').mkdir(parents=True, exist_ok=True)
            (self.yolo_path / split / 'labels').mkdir(parents=True, exist_ok=True)
        print(f"Created dataset directory: {self.yolo_path}")

    def save_class_info(self):
        """Save class information in multiple formats"""
        # Save classes.txt
        classes_txt = self.yolo_path / 'classes.txt'
        with open(classes_txt, 'w') as f:
            for class_name in self.classes:
                f.write(f"{class_name}\n")
        
        # Save classes.yaml
        classes_yaml = self.yolo_path / 'classes.yaml'
        class_dict = {i: name for i, name in enumerate(self.classes)}
        with open(classes_yaml, 'w') as f:
            yaml.dump(class_dict, f)
        
        # Save data.yaml
        data_yaml = self.yolo_path / 'data.yaml'
        data_dict = {
            'path': str(self.yolo_path.absolute()),
            'train': str(self.yolo_path / 'train' / 'images'),
            'val': str(self.yolo_path / 'valid' / 'images'),
            'names': class_dict,
            'nc': len(self.classes)
        }
        with open(data_yaml, 'w') as f:
            yaml.dump(data_dict, f)
        
        print(f"Saved class information:")
        print(f"- Classes file: {classes_txt}")
        print(f"- Classes YAML: {classes_yaml}")
        print(f"- Data YAML: {data_yaml}")
        print(f"Total classes: {len(self.classes)}")
        for i, class_name in enumerate(self.classes):
            print(f"  {i}: {class_name}")

    def setup_gui(self):
        """Setup the GUI for image labeling"""
        self.root = tk.Tk()
        self.root.title("Image Labeling Tool")
        
        # Main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for image
        self.canvas = tk.Canvas(self.main_frame, width=self.image_width, height=self.image_height)
        self.canvas.pack(side=tk.LEFT)
        
        # Control panel
        self.control_panel = tk.Frame(self.main_frame)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Class selector
        self.class_var = tk.StringVar(value=self.classes[0])
        tk.Label(self.control_panel, text="Select Class:").pack(pady=5)
        self.class_menu = tk.OptionMenu(self.control_panel, self.class_var, *self.classes)
        self.class_menu.pack(pady=5)
        
        # Image counter
        self.counter_label = tk.Label(self.control_panel, text="Image: 0/0")
        self.counter_label.pack(pady=5)
        
        # Navigation buttons
        button_frame = tk.Frame(self.control_panel)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Previous", command=self.prev_image).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Next", command=self.next_image).pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        tk.Button(self.control_panel, text="Save Annotation", command=self.save_annotation).pack(pady=5)
        tk.Button(self.control_panel, text="Clear Box", command=self.clear_box).pack(pady=5)
        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
        # Load first class images
        self.load_class_images()

    def load_class_images(self):
        """Load images for current class"""
        current_class = self.class_var.get()
        class_path = os.path.join(self.dataset_path, current_class)
        self.images = [os.path.join(class_path, f) for f in os.listdir(class_path) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        
        if self.images:
            self.current_image_index = 0
            self.load_image(self.images[0])
            self.update_counter()
        else:
            messagebox.showwarning("Warning", f"No images found in class folder: {current_class}")

    def load_image(self, image_path):
        """Load and display image on canvas"""
        if not os.path.exists(image_path):
            messagebox.showerror("Error", f"Image not found: {image_path}")
            return
            
        try:
            self.current_image = cv2.imread(image_path)
            self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            
            # Resize for display while maintaining aspect ratio
            height, width = self.current_image.shape[:2]
            scaling = min(self.image_width/width, self.image_height/height)
            new_width, new_height = int(width*scaling), int(height*scaling)
            
            self.display_image = cv2.resize(self.current_image, (new_width, new_height))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.display_image))
            
            # Clear canvas and display new image
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def update_counter(self):
        """Update image counter display"""
        self.counter_label.config(text=f"Image: {self.current_image_index + 1}/{len(self.images)}")

    def start_drawing(self, event):
        """Initialize rectangle drawing"""
        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y
        self.clear_box()

    def draw_rectangle(self, event):
        """Draw rectangle as user drags mouse"""
        if not self.drawing:
            return
            
        if self.current_rect:
            self.canvas.delete(self.current_rect)
            
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            event.x, event.y,
            outline="red",
            width=2
        )

    def stop_drawing(self, event):
        """Finish drawing rectangle"""
        if self.drawing:
            self.drawing = False
            self.roi_points = [(self.start_x, self.start_y), (event.x, event.y)]

    def clear_box(self):
        """Clear the current bounding box"""
        if hasattr(self, 'current_rect') and self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = None
        self.roi_points = []

    def save_annotation(self):
        """Save annotation in YOLO format"""
        if not hasattr(self, 'roi_points') or len(self.roi_points) != 2:
            messagebox.showwarning("Warning", "Please draw a bounding box first!")
            return
            
        try:
            # Get original image dimensions
            img_height, img_width = self.current_image.shape[:2]
            
            # Convert coordinates to YOLO format
            x1, y1 = self.roi_points[0]
            x2, y2 = self.roi_points[1]
            
            # Adjust coordinates based on display scaling
            display_height, display_width = self.display_image.shape[:2]
            x1 = x1 * (img_width / display_width)
            x2 = x2 * (img_width / display_width)
            y1 = y1 * (img_height / display_height)
            y2 = y2 * (img_height / display_height)
            
            # Calculate YOLO format values (normalized)
            x_center = ((x1 + x2) / 2) / img_width
            y_center = ((y1 + y2) / 2) / img_height
            width = abs(x2 - x1) / img_width
            height = abs(y2 - y1) / img_height
            
            # Ensure values are between 0 and 1
            x_center = max(0, min(1, x_center))
            y_center = max(0, min(1, y_center))
            width = max(0, min(1, width))
            height = max(0, min(1, height))
            
            # Save annotation
            image_name = os.path.basename(self.images[self.current_image_index])
            label_path = self.yolo_path / 'train' / 'labels' / f"{image_name.rsplit('.', 1)[0]}.txt"
            
            with open(label_path, 'w') as f:
                class_id = self.classes.index(self.class_var.get())
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
            
            # Copy image
            shutil.copy(
                self.images[self.current_image_index],
                self.yolo_path / 'train' / 'images' / image_name
            )
            
            messagebox.showinfo("Success", "Annotation saved!")
            self.next_image()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save annotation: {str(e)}")

    def next_image(self):
        """Load next image"""
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.load_image(self.images[self.current_image_index])
            self.update_counter()
            self.clear_box()

    def prev_image(self):
        """Load previous image"""
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image(self.images[self.current_image_index])
            self.update_counter()
            self.clear_box()

    def run(self):
        """Start the labeling tool"""
        self.root.mainloop()

if __name__ == "__main__":
    # Replace with your dataset path
    dataset_path = r"augmented_datasets"  # Replace with your actual dataset path
    labeler = ImageLabeler(dataset_path)
    labeler.run()