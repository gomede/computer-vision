import os
from ultralytics import YOLO

# Ensure the model path is correctly specified for cross-platform compatibility
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'weights', 'best.pt')

# Attempt to load a custom model with error handling
try:
    model = YOLO(model_path)  # Load a custom model
    print(f"Model loaded successfully from {model_path}.")
except Exception as e:
    print(f"Failed to load model from {model_path}: {e}")
    exit(1)

# Validate the model
try:
    metrics = model.val()  # Perform validation; assumes dataset and settings are predefined
    # Print validation metrics
    print(f"Validation Metrics:")
    print(f"- mAP50-95: {metrics.box.map:.4f}")
    print(f"- mAP50: {metrics.box.map50:.4f}")
    print(f"- mAP75: {metrics.box.map75:.4f}")
    print(f"- mAPs by Category: {metrics.box.maps}")
except Exception as e:
    print(f"Validation failed: {e}")
    exit(1)
