import cv2
import numpy as np
import os
from tqdm import tqdm

def add_gaussian_noise(image, mean=0, sigma=50):  # Increased sigma from 25 to 50
    """Add Gaussian noise to an image"""
    noise = np.random.normal(mean, sigma, image.shape)
    noisy_image = image + noise
    return np.clip(noisy_image, 0, 255).astype(np.uint8)

def add_salt_pepper_noise(image, prob=0.05):  # Increased probability from 0.02 to 0.05
    """Add salt and pepper noise to an image"""
    noisy_image = image.copy()
    # Salt noise
    salt_mask = np.random.random(image.shape) < prob
    noisy_image[salt_mask] = 255
    # Pepper noise
    pepper_mask = np.random.random(image.shape) < prob
    noisy_image[pepper_mask] = 0
    return noisy_image

def adjust_brightness_contrast(image, brightness=0, contrast=1):
    """Adjust brightness and contrast of an image"""
    adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    return adjusted

def apply_blur(image, kernel_size=3):
    """Apply Gaussian blur to an image"""
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def rotate_image(image, angle):
    """Rotate image by given angle"""
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (width, height))

def preprocess_dataset(input_path, output_path, target_size=(480, 480)):  # Changed size to 480x480
    """
    Preprocess all images in the dataset with various augmentations
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Process each class folder
    for class_name in os.listdir(input_path):
        class_path = os.path.join(input_path, class_name)
        if not os.path.isdir(class_path):
            continue
            
        # Create output class directory
        output_class_path = os.path.join(output_path, class_name)
        if not os.path.exists(output_class_path):
            os.makedirs(output_class_path)
            
        # Process each image in the class folder
        images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        for img_name in tqdm(images, desc=f"Processing {class_name}"):
            img_path = os.path.join(class_path, img_name)
            
            # Read image
            image = cv2.imread(img_path)
            if image is None:
                print(f"Could not read image: {img_path}")
                continue
                
            # Resize image
            resized = cv2.resize(image, target_size)
            
            # Generate augmented versions
            augmentations = {
                'original': resized,
                'gaussian': add_gaussian_noise(resized),
                'gaussian_strong': add_gaussian_noise(resized, sigma=75),  # Added stronger gaussian noise
                'salt_pepper': add_salt_pepper_noise(resized),
                'salt_pepper_strong': add_salt_pepper_noise(resized, prob=0.08),  # Added stronger salt & pepper noise
                'bright': adjust_brightness_contrast(resized, brightness=30),
                'dark': adjust_brightness_contrast(resized, brightness=-30),
                'contrast': adjust_brightness_contrast(resized, contrast=1.3),
                'blur': apply_blur(resized, kernel_size=5),
                'rotate90': rotate_image(resized, 90),
                'rotate180': rotate_image(resized, 180),
                'rotate270': rotate_image(resized, 270)
            }
            
            # Save all versions
            basename = os.path.splitext(img_name)[0]
            for aug_name, aug_image in augmentations.items():
                output_name = f"{basename}_{aug_name}.jpg"
                output_path_full = os.path.join(output_class_path, output_name)
                cv2.imwrite(output_path_full, aug_image)

if __name__ == "__main__":
    # Replace these paths with your actual paths
    input_dataset_path = r"D:\projects\smart_checkout_system\datasets\Images"
    output_dataset_path = r"D:\projects\smart_checkout_system\augmented_datasets"
    
    preprocess_dataset(input_dataset_path, output_dataset_path)