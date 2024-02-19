import os
import cv2
import json
import requests
from datetime import datetime
from ultralytics import YOLO
from getmac import get_mac_address as gma

def post_monitoring_data(class_field, evidence, access_token, refresh_token):
    """
    Posts monitoring data to the specified endpoint.
    
    Args:
        class_field (str): The class of the detected object.
        evidence (str): The filepath to the image evidence of the detected object.
    """

    # Preparing the POST request to send monitoring data
    url = "http://localhost:8000/api/monitoring/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    data = {
        "mac": gma(),
        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "class_field": class_field,
        "evidence": evidence
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 401 and refresh_token: 
        # Attempt to renew the token if necessary and if refresh_token is available
        renew_response = requests.post('http://localhost:8000/api/authentication/renovate/', data={'refresh_token': refresh_token})
        if renew_response.status_code == 200:
            new_tokens = renew_response.json()
            access_token = new_tokens.get('Token_access')
            headers['Authorization'] = f'Bearer {access_token}'
            response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # Check for success status codes (200 OK or 201 Created)
    if response.status_code in (200, 201):
        print("Data posted successfully.")
        return response.json()
    else:
        print(f"Failed to post data. Status code: {response.status_code}")
        return None

# Main function to perform object detection and handle video capture
def main(video_path, model_path, access_token, refresh_token, threshold=0.1):
    """
    Captures video frames, performs object detection, and posts data for each detected object.

    Args:
        video_path (str): Path to the video file or device index for the webcam.
        model_path (str): Path to the YOLO model weights file.
        threshold (float): Detection threshold for filtering weak detections.
    """

    model = YOLO(model_path)  # Load a custom model

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
                    evidence = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs', 'cropped_images', str(i) + '.jpg')
                  
                    cv2.imwrite(evidence, crop_object)
                    post_monitoring_data('Mouse', evidence, access_token, refresh_token)

        # Display the processed frame
        cv2.imshow("Detections", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    credentials = {'username': 'admin', 'password': 'Senai@2023'}
    login_response = requests.post('http://localhost:8000/api/authentication/login/', data=credentials)
    access_token = None  # Initialize access_token to None to guarantee definition

    if login_response.status_code == 200:
        tokens = login_response.json()
        access_token = tokens.get('Token_access')
        refresh_token = tokens.get('Token_renovation') 
    else:
        print("Login failed with status code:", login_response.status_code)

    if not access_token:
        # If access_token was not obtained, it is not required
        print("Access token not obtained.")
    else:
        video_path = 0  # Change to your video path or keep 0 for webcam
        #video_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'test', 'desk_with_mouse.mp4')
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'weights', 'best.pt')
        main(video_path, model_path, access_token, refresh_token)    