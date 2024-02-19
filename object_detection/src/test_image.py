import cv2
from ultralytics import YOLO

# Define paths using os.path.join for cross-platform compatibility
model_path = r'object_detection/models/weights/best.pt'
image_path = r'object_detection/data/test/desk_with_mouse.jpg'

# Initialize the YOLO model for inference
infer = YOLO(model_path)

# Perform prediction and optionally save the resulting image and detection data
results = infer.predict(image_path, save=True, save_txt=True)

# Ensure the results have a 'boxes' attribute before proceeding
if hasattr(results[0], 'boxes'):
    # Load the original image
    img = cv2.imread(image_path)

    # Extract bounding boxes
    boxes = results[0].boxes.xyxy.tolist()

    # Iterate through the bounding boxes to crop and save each detected object
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)  # Convert coordinates to integers
        # Crop the object using the bounding box coordinates
        crop_object = img[y1:y2, x1:x2]
        # Define a unique filename for each cropped image
        crop_filename = f'object_detection/outputs/cropped_images/crop_object_{i}.jpg'
        # Save the cropped object as an image
        cv2.imwrite(crop_filename, crop_object)
    print(f"{len(boxes)} objects cropped and saved.")
else:
    print("No bounding box information found in results.")
