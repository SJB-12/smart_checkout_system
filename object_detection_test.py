import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# Load the trained model
model_path = "D:/projects/smart_checkout_system/yolo_model_output/cart_model.h5"
model = load_model(model_path)

# Class names for the trained model's labels
class_names = ["appy", "lays_orange_pack", "maggi", "monaco"]

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set up matplotlib for real-time display
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots(figsize=(8, 6))
img_plot = ax.imshow(np.zeros((480, 640, 3), dtype=np.uint8))  # Placeholder for initial frame

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Resize the frame to match model's input shape
        input_frame = cv2.resize(frame, (416, 416))
        input_frame = np.expand_dims(input_frame, axis=0) / 255.0

        # Run prediction on the input frame
        predictions = model.predict(input_frame)

        # Clear existing detections
        detections = []

        # Parse the prediction output (assuming bounding boxes and classes are included)
        for prediction in predictions:
            class_id = np.argmax(prediction[:len(class_names)])
            score = prediction[class_id]
            if score > 0.5:  # Adjust threshold as needed
                label = class_names[class_id]
                
                # Extract bounding box coordinates (assuming your model outputs them)
                x, y, width, height = prediction[-4:]  # assuming last 4 values are bounding box coords
                
                # Convert bounding box coordinates to original frame size
                h_ratio, w_ratio = frame.shape[0] / 416, frame.shape[1] / 416
                x = int(x * w_ratio)
                y = int(y * h_ratio)
                width = int(width * w_ratio)
                height = int(height * h_ratio)
                
                # Store the detection for drawing
                detections.append((label, score, x, y, width, height))

        # Draw detections on the frame
        for label, score, x, y, width, height in detections:
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
            cv2.putText(frame, f"{label}: {score:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Convert frame to RGB for matplotlib display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_plot.set_data(frame_rgb)
        plt.draw()
        plt.pause(0.001)

except KeyboardInterrupt:
    print("Stream stopped.")

# Release the webcam and close all windows
cap.release()
plt.close()
