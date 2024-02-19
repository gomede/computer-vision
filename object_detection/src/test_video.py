import cv2
from ultralytics import YOLO

video_path = r'object_detection/data/test/desk_with_mouse.mp4'

# Load the model
model_path = r'object_detection/models/weights/best.pt'
model = YOLO(model_path)  # Load a custom model

# Detection threshold
threshold = 0.1

# Initialize video capture
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit the loop if no frames are left

    # Perform detection
    results = model(frame)[0]
    # Extract bounding boxes
    boxes = results.boxes.xyxy.tolist()

    # Draw bounding boxes and labels on the frame
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            
            # Iterate through the bounding boxes
            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = box
                # Crop the object using the bounding box coordinates
                crop_object = frame[int(y1):int(y2), int(x1):int(x2)]
                # Save the cropped object as an image
                cv2.imwrite('object_detection/outputs/cropped_images/crop_object_' + str(i) + '.jpg', crop_object)

    # Display the processed frame
    cv2.imshow("Detections", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
