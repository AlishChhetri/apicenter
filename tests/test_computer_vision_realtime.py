from apicenter.universal_api_caller import apicenter
import cv2


def main():
    """Main function to test universal_api_caller with multiple fail-safe providers for real-time camera processing."""

    # Define the prompt for the real-time computer vision task
    prompt = {
        "task_type": "realtime",  # Task type set to "realtime"
        "camera_id": 0,  # Default camera, adjust if multiple cameras are connected
    }

    # Test with multiple fail-safes in order of priority
    try:
        # Start real-time camera processing with fail-safe providers
        for processed_frame, detections in apicenter.computer_vision(
            provider="ultralytics",
            model="yolov8m",  # Replace with actual model path if needed
            prompt=prompt,
            fail_safe=[
                ("ultralytics", "yolov8n"),  # Alternate model to try if primary fails
            ],
        ):
            # Display processed frame with bounding boxes and labels
            cv2.imshow("Real-Time Detection", processed_frame)

            # Print detection summary for each frame
            print("Detections Summary:")
            if hasattr(detections, "boxes") and detections.boxes is not None:
                for detection in detections.boxes.data.tolist():
                    x_min, y_min, x_max, y_max, confidence, class_id = detection[:6]
                    print(
                        f"Label: {int(class_id)}, Confidence: {confidence:.2f}, "
                        f"Bounding Box: [{x_min}, {y_min}, {x_max}, {y_max}]"
                    )
            else:
                print("No detections in this frame.")

            # Press 'q' to exit the loop
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Exiting real-time detection.")
                break
    finally:
        # Release resources and close OpenCV windows
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
