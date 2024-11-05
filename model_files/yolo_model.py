import os
import yaml
from pathlib import Path
import torch
import subprocess
import shutil

def setup_yolov5():
    """Clone YOLOv5 if it doesn't exist and install requirements"""
    if not os.path.exists('yolov5'):
        subprocess.run(['git', 'clone', 'https://github.com/ultralytics/yolov5.git'])
    
    # Install requirements
    subprocess.run(['pip', 'install', '-r', 'yolov5/requirements.txt'])

def prepare_training_data(labeled_data_path):
    """Prepare the data configuration file for training"""
    # Find data.yaml in the labeled data directory
    data_yaml_path = os.path.join(labeled_data_path, 'data.yaml')
    
    if not os.path.exists(data_yaml_path):
        raise FileNotFoundError(f"data.yaml not found in {labeled_data_path}")
    
    # Load and modify the data.yaml file
    with open(data_yaml_path, 'r') as f:
        data_config = yaml.safe_load(f)
    
    # Update paths to be absolute
    data_config['train'] = str(Path(labeled_data_path) / 'train' / 'images')
    data_config['val'] = str(Path(labeled_data_path) / 'train' / 'images')  # Using same for validation
    
    # Save modified config
    modified_yaml_path = 'dataset_config.yaml'
    with open(modified_yaml_path, 'w') as f:
        yaml.dump(data_config, f)
    
    return modified_yaml_path, data_config['nc']

def train_yolo(data_yaml_path, num_classes, epochs=20, batch_size=16, img_size=640):
    """Train YOLOv5 model"""
    # Select appropriate model size based on dataset
    if num_classes < 5:
        model_type = 'yolov5s'  # Small model for simple datasets
    elif num_classes < 20:
        model_type = 'yolov5m'  # Medium model for moderate datasets
    else:
        model_type = 'yolov5l'  # Large model for complex datasets
    
    print(f"Training {model_type} model for {num_classes} classes...")
    
    # Training command
    train_command = [
        'python', 'yolov5/train.py',
        '--img', str(img_size),
        '--batch', str(batch_size),
        '--epochs', str(epochs),
        '--data', data_yaml_path,
        '--weights', f'{model_type}.pt',
        '--cache'
    ]
    
    # Run training
    subprocess.run(train_command)

def main():
    # Path to your labeled dataset
    labeled_data_path = r"C:\Users\Suman_PC\Documents\GitHub\smart_checkout_system\model_files\yolo_dataset_20241105_134756"  # Update this with your dataset timestamp
    
    try:
        # Setup YOLOv5
        setup_yolov5()
        
        # Prepare data
        data_yaml_path, num_classes = prepare_training_data(labeled_data_path)
        
        # Train model
        train_yolo(
            data_yaml_path=data_yaml_path,
            num_classes=num_classes,
            epochs=10,
            batch_size=16,  # Adjust based on your GPU memory
            img_size=640
        )
        
        print("Training completed! Check the 'runs/train' folder for results.")
        
    except Exception as e:
        print(f"Error during training: {str(e)}")

if __name__ == "__main__":
    main()