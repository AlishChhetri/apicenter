import os
import base64
from apicenter.universal_api_caller import apicenter


def test_image():
    """Main function to test universal_api_caller with YOLOv8 for computer vision."""

    # Define the prompt for the computer vision task
    prompt = {
        "task_type": "image",  # Can be "image", "video", or "realtime"
        "source": "test_media/test_image.png",  # Path to the image file
    }

    # Use YOLOv8 models with fail-safe options
    response = apicenter.computer_vision(
        provider="ultralytics",
        model="golov8n",  # YOLOv8 nano model
        prompt=prompt,
        fail_safe=[
            ("ultralytics", "golov8s"),  # Small model as backup
            ("ultralytics", "yolov8m"),  # Medium model as final fallback
        ],
    )

    # Add error handling for the response
    try:
        if isinstance(response, dict) and "detections" in response:
            print("Detections Summary:")
            for detection in response["detections"]:
                if len(detection) >= 6:
                    x_min, y_min, x_max, y_max, confidence, class_id = detection[:6]
                    print(
                        f"Label: {int(class_id)}, Confidence: {confidence:.2f}, "
                        f"Bounding Box: [{x_min:.2f}, {y_min:.2f}, {x_max:.2f}, {y_max:.2f}]"
                    )

            # Ensure the output directory exists
            output_dir = "test_media"
            os.makedirs(output_dir, exist_ok=True)

            # Save the processed image with bounding boxes
            output_image_path = os.path.join(
                output_dir, "processed_image_with_detections.png"
            )
            try:
                with open(output_image_path, "wb") as f:
                    f.write(base64.b64decode(response["image_base64"]))
                print("Processed image saved as:", output_image_path)
            except Exception as e:
                print(f"Error saving processed image: {e}")
        else:
            print("Unexpected response format:", response)

    except Exception as e:
        print(f"Error processing detections: {e}")


if __name__ == "__main__":
    test_image()
