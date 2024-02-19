import os
import yaml
import logging
from ultralytics import YOLO

# Define the log directory and file
log_directory = r'object_detection/outputs/logs'
log_file = r'object_detection/outputs/logs/training_log.txt'

# Create the directory if it doesn't exist
os.makedirs(log_directory, exist_ok=True)

# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Define the model configuration and weights file paths
# Use os.path.join for cross-platform compatibility
model_config_path = 'yolov8n.yaml'
model_weights_path = 'yolov8n.pt'

# Define the path to the data configuration file
# Adjust the path as necessary for your project structure
current_dir = os.path.dirname(__file__)  # Get the directory where the script is located
project_root = os.path.dirname(current_dir)  # Navigate up to the project root directory
data_config_path = os.path.join(project_root, 'dataset.yaml')  # Construct the path to 'dataset.yaml'

# Now open the file using the corrected path
with open(data_config_path) as f:
    config = yaml.safe_load(f)

# Load the YOLO model with the specified configuration
# The load method is used to load the pre-trained weights
model = YOLO(model_config_path).load(model_weights_path)

# Log the start of training
logging.info("Starting training process.")

try:
    # Train the model with the specified data and parameters
    # - data: Path to the dataset configuration file
    # - epochs: Number of training epochs
    # - imgsz: Input image size
    results = model.train(data=data_config_path, epochs=150, imgsz=640)
    
    # Log training results using attribute access or methods
    logging.info("Training completed successfully.")
    
    # Perform validation; assumes dataset and settings are predefined
    metrics = model.val()  

    # Print validation metrics
    logging.info(f"Validation Metrics:")
    logging.info(f"- mAP50-95: {metrics.box.map:.4f}")
    logging.info(f"- mAP50: {metrics.box.map50:.4f}")
    logging.info(f"- mAP75: {metrics.box.map75:.4f}")
    logging.info(f"- mAPs by Category: {metrics.box.maps}")
except Exception as e:
    # Log any errors that occur
    logging.error(f"An error occurred during training: {e}")
