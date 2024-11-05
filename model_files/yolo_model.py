import tensorflow as tf
import cv2
import numpy as np
import os
from tensorflow.keras.preprocessing.image import img_to_array

# Set paths for dataset and YOLO configuration files
dataset_path = r"D:\projects\smart_checkout_system\augmented_datasets"
model_save_path = r"D:\projects\smart_checkout_system\yolo_model_output\cart_model.h5"

# YOLO model parameters
IMG_SIZE = (416, 416)  # Size required by YOLO
BATCH_SIZE = 8
EPOCHS = 30
NUM_CLASSES = 4  # Adjust this based on your dataset

# Preprocessing function
def preprocess_image(image_path):
    """Read and preprocess an image for YOLO"""
    image = cv2.imread(image_path)
    if image is None:
        return None
    # Resize to required YOLO input size
    image_resized = cv2.resize(image, IMG_SIZE)
    # Normalize the image to [0, 1] range for YOLO
    image_normalized = image_resized / 255.0
    return image_normalized

def load_data(dataset_path):
    """Load and preprocess images and labels from dataset"""
    images = []
    labels = []
    class_folders = os.listdir(dataset_path)
    label_map = {name: idx for idx, name in enumerate(class_folders)}  # Map each folder name to a unique integer

    for class_folder in class_folders:
        class_path = os.path.join(dataset_path, class_folder)
        if not os.path.isdir(class_path):
            continue

        label = label_map[class_folder]  # Get the label from the map
        for img_file in os.listdir(class_path):
            img_path = os.path.join(class_path, img_file)
            processed_image = preprocess_image(img_path)
            if processed_image is not None:
                images.append(processed_image)
                labels.append(label)

    images = np.array(images, dtype="float32")
    labels = np.array(labels)
    return images, labels


# Load dataset
train_images, train_labels = load_data(dataset_path)
train_labels = tf.keras.utils.to_categorical(train_labels, NUM_CLASSES)  # One-hot encode labels

# Build YOLOv4-tiny model (simplified, can customize if using pre-trained weights)
model = tf.keras.applications.MobileNetV2(input_shape=IMG_SIZE + (3,), weights='imagenet', include_top=False)
model = tf.keras.models.Sequential([
    model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_images, train_labels, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.2)

# Save the model
model.save(model_save_path)
print("Model saved successfully!")
