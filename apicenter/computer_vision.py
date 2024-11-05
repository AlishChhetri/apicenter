"""Computer vision module to handle requests for various vision models like YOLO and real-time processing"""

import cv2
from ultralytics import YOLO
import base64


class ComputerVision:
    """Handles requests for computer vision models"""

    def __init__(self):
        self.active_models = {}
        self.supported_providers = {
            "ultralytics": self._init_ultralytics_model,
        }

    def _init_ultralytics_model(self, model_name):
        """Initialize an Ultralytics YOLO model, downloading if not available"""
        if model_name not in self.active_models:
            try:
                # Attempt to load the model; this will download if not found
                self.active_models[model_name] = YOLO(model_name)
                print(f"Loaded model '{model_name}'.")
            except Exception as e:
                print(f"Error loading model '{model_name}': {e}")
                raise FileNotFoundError(
                    f"Failed to load or download the model '{model_name}'."
                )
        return self.active_models[model_name]

    def process_image(self, provider, model, image_path, **kwargs):
        """Process a single image with the specified model"""
        if provider.lower() not in self.supported_providers:
            raise ValueError(f"Unsupported provider: {provider}")

        # Initialize model if needed
        model_instance = self.supported_providers[provider.lower()](model)

        # Load and process image
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
        else:  # Assume numpy array
            image = image_path

        # Run inference
        results = model_instance(image, **kwargs)

        # Process results
        processed_image = results[0].plot()

        # Convert to base64 for easy transfer
        _, buffer = cv2.imencode(".jpg", processed_image)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        return {
            "image_base64": img_base64,
            "detections": results[0].boxes.data.tolist()
            if hasattr(results[0], "boxes")
            else None,
            "model_type": model_instance.task,
        }

    def process_video(self, provider, model, video_path, output_path=None, **kwargs):
        """Process a video file with the specified model"""
        if provider.lower() not in self.supported_providers:
            raise ValueError(f"Unsupported provider: {provider}")

        model_instance = self.supported_providers[provider.lower()](model)

        # Open video file
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Setup output video writer if path provided
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frames_processed = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process frame
            results = model_instance(frame, **kwargs)
            processed_frame = results[0].plot()

            if output_path:
                out.write(processed_frame)
            frames_processed.append(processed_frame)

        cap.release()
        if output_path:
            out.release()
            return output_path

        return frames_processed

    def realtime_camera(self, provider, model, camera_id=0, **kwargs):
        """Process real-time camera feed with the specified model"""
        if provider.lower() not in self.supported_providers:
            raise ValueError(f"Unsupported provider: {provider}")

        model_instance = self.supported_providers[provider.lower()](model)

        # Initialize camera
        cap = cv2.VideoCapture(camera_id)

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Process frame
                results = model_instance(frame, **kwargs)
                processed_frame = results[0].plot()

                yield processed_frame, results[0]

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        finally:
            cap.release()
