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
        
        # Initialize variables
        self.current_class_index = 0
        self.current_image_index = 0
        self.images = {}  # Dictionary to store images for each class
        self.current_image = None
        self.photo = None
        self.drawing = False
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        self.image_width = 800
        self.image_height = 600
        
        # Create YOLO dataset directory
        self.timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.yolo_path = Path(f'yolo_dataset_{self.timestamp}')
        self.setup_directories()
        self.save_class_info()
        
        # Load all images
        self._load_all_class_images()
        self.setup_gui()

    def _get_classes(self):
        return [folder for folder in sorted(os.listdir(self.dataset_path)) 
                if os.path.isdir(os.path.join(self.dataset_path, folder))]

    def _load_all_class_images(self):
        self.images = {}
        for class_name in self.classes:
            class_path = os.path.join(self.dataset_path, class_name)
            self.images[class_name] = [
                os.path.join(class_path, f) for f in os.listdir(class_path)
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))
            ]
        print("Loaded images for classes:", {k: len(v) for k, v in self.images.items()})

    def setup_directories(self):
        (self.yolo_path / 'train' / 'images').mkdir(parents=True, exist_ok=True)
        (self.yolo_path / 'train' / 'labels').mkdir(parents=True, exist_ok=True)
        print(f"Created dataset directory: {self.yolo_path}")

    def save_class_info(self):
        data_yaml = self.yolo_path / 'data.yaml'
        data_dict = {
            'train': str(self.yolo_path / 'train' / 'images'),
            'val': str(self.yolo_path / 'train' / 'images'),  # Using same for validation
            'nc': len(self.classes),
            'names': self.classes
        }
        with open(data_yaml, 'w') as f:
            yaml.dump(data_dict, f)

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Image Labeling Tool")
        
        # Main layout
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas
        self.canvas = tk.Canvas(self.main_frame, width=self.image_width, height=self.image_height, bg='gray')
        self.canvas.pack(side=tk.LEFT)
        
        # Control panel
        self.control_panel = tk.Frame(self.main_frame, width=200)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Class navigation
        self.class_nav_frame = tk.Frame(self.control_panel)
        self.class_nav_frame.pack(fill=tk.X, pady=5)
        tk.Button(self.class_nav_frame, text="← Prev Class", command=self.prev_class).pack(side=tk.LEFT, padx=2)
        tk.Button(self.class_nav_frame, text="Next Class →", command=self.next_class).pack(side=tk.RIGHT, padx=2)
        
        # Current class display
        self.class_label = tk.Label(
            self.control_panel, 
            text=self.classes[0], 
            font=("Arial", 12, "bold")
        )
        self.class_label.pack(pady=5)
        
        # Progress information
        self.counter_label = tk.Label(self.control_panel, text="Image: 0/0")
        self.counter_label.pack(pady=5)
        
        # Navigation buttons
        tk.Button(self.control_panel, text="Previous Image (←)", command=self.prev_image).pack(pady=2)
        tk.Button(self.control_panel, text="Next Image (→)", command=self.next_image).pack(pady=2)
        tk.Button(self.control_panel, text="Save (S)", command=self.save_annotation).pack(pady=2)
        tk.Button(self.control_panel, text="Clear Box (C)", command=self.clear_box).pack(pady=2)
        
        # Add instructions label
        instructions = """
        Instructions:
        1. Draw box around object
        2. Press 'S' to save
        3. Use arrows to navigate
        4. Press 'C' to clear box
        """
        tk.Label(self.control_panel, text=instructions, justify=tk.LEFT, wraplength=180).pack(pady=10)
        
        # Bindings
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        self.root.bind('<Left>', lambda e: self.prev_image())
        self.root.bind('<Right>', lambda e: self.next_image())
        self.root.bind('s', lambda e: self.save_annotation())
        self.root.bind('c', lambda e: self.clear_box())
        
        # Load initial image
        self.update_display()

    def update_display(self):
        current_class = self.classes[self.current_class_index]
        self.class_label.config(text=f"Class: {current_class}")
        
        if current_class in self.images and self.images[current_class]:
            self.load_image(self.images[current_class][self.current_image_index])
            total_images = len(self.images[current_class])
            self.counter_label.config(text=f"Image: {self.current_image_index + 1}/{total_images}")
        else:
            self.canvas.delete("all")
            messagebox.showwarning("Warning", f"No images found in class: {current_class}")

    def load_image(self, image_path):
        self.current_image = cv2.imread(image_path)
        self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        
        # Resize for display
        height, width = self.current_image.shape[:2]
        scaling = min(self.image_width/width, self.image_height/height)
        new_width, new_height = int(width*scaling), int(height*scaling)
        
        self.display_image = cv2.resize(self.current_image, (new_width, new_height))
        
        # Convert to PhotoImage
        image = Image.fromarray(self.display_image)
        self.photo = ImageTk.PhotoImage(image=image)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        self.canvas.create_image(
            (self.image_width - new_width) // 2,
            (self.image_height - new_height) // 2,
            image=self.photo, 
            anchor="nw"
        )

    def next_class(self):
        if self.current_class_index < len(self.classes) - 1:
            self.current_class_index += 1
            self.current_image_index = 0
            self.clear_box()
            self.update_display()

    def prev_class(self):
        if self.current_class_index > 0:
            self.current_class_index -= 1
            self.current_image_index = 0
            self.clear_box()
            self.update_display()

    def next_image(self):
        current_class = self.classes[self.current_class_index]
        if current_class in self.images:
            if self.current_image_index < len(self.images[current_class]) - 1:
                self.current_image_index += 1
                self.load_image(self.images[current_class][self.current_image_index])
                self.clear_box()

    def prev_image(self):
        current_class = self.classes[self.current_class_index]
        if current_class in self.images:
            if self.current_image_index > 0:
                self.current_image_index -= 1
                self.load_image(self.images[current_class][self.current_image_index])
                self.clear_box()

    def start_drawing(self, event):
        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y
        self.clear_box()

    def draw_rectangle(self, event):
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
        if self.drawing:
            self.drawing = False
            self.roi_points = [(self.start_x, self.start_y), (event.x, event.y)]

    def clear_box(self):
        if hasattr(self, 'current_rect') and self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = None
        if hasattr(self, 'roi_points'):
            del self.roi_points

    def save_annotation(self):
        if not hasattr(self, 'roi_points'):
            messagebox.showwarning("Warning", "Please draw a bounding box first!")
            return
            
        # Get dimensions
        img_height, img_width = self.current_image.shape[:2]
        display_height, display_width = self.display_image.shape[:2]
        
        # Get coordinates
        x1, y1 = self.roi_points[0]
        x2, y2 = self.roi_points[1]
        
        # Adjust for image position in canvas
        canvas_x = (self.image_width - display_width) // 2
        canvas_y = (self.image_height - display_height) // 2
        x1 = x1 - canvas_x
        x2 = x2 - canvas_x
        y1 = y1 - canvas_y
        y2 = y2 - canvas_y
        
        # Convert to original image scale
        x1 = x1 * (img_width / display_width)
        x2 = x2 * (img_width / display_width)
        y1 = y1 * (img_height / display_height)
        y2 = y2 * (img_height / display_height)
        
        # Convert to YOLO format
        x_center = ((x1 + x2) / 2) / img_width
        y_center = ((y1 + y2) / 2) / img_height
        width = abs(x2 - x1) / img_width
        height = abs(y2 - y1) / img_height
        
        # Ensure values are between 0 and 1
        x_center = max(0, min(1, x_center))
        y_center = max(0, min(1, y_center))
        width = max(0, min(1, width))
        height = max(0, min(1, height))
        
        current_class = self.classes[self.current_class_index]
        current_image_path = self.images[current_class][self.current_image_index]
        
        # Save files
        image_name = os.path.basename(current_image_path)
        base_name = os.path.splitext(image_name)[0]
        
        # Save label
        label_path = self.yolo_path / 'train' / 'labels' / f"{base_name}.txt"
        with open(label_path, 'w') as f:
            class_id = self.current_class_index
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        # Copy image
        shutil.copy(
            current_image_path,
            self.yolo_path / 'train' / 'images' / image_name
        )
        
        # Move to next image
        self.next_image()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Use raw string (r) prefix for Windows paths
    dataset_path = r"C:\Users\Suman_PC\Documents\GitHub\smart_checkout_system\augmented_datasets"
    labeler = ImageLabeler(dataset_path)
    labeler.run()