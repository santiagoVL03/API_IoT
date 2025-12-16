import cv2
import numpy as np
import logging
import os
import tempfile
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import urllib.request

class DetectionUtil:
    """Utility class for fire detection using OpenCV DNN with ONNX and computer vision techniques."""
    
    def __init__(self, model_path: Optional[str] = None, confidence_threshold: float = 0.5):
        """
        Initialize the fire detection utility.
        
        Args:
            model_path: Path to ONNX YOLO model. If None, will attempt to download or use fallback methods
            confidence_threshold: Minimum confidence threshold for fire detection (0.0 to 1.0)
        """
        self.confidence_threshold = confidence_threshold
        self.net = None
        self.model_loaded = False
        self.class_names = []
        
        # Try to load YOLO ONNX model with OpenCV DNN
        try:
            if model_path and os.path.exists(model_path):
                self._load_onnx_model(model_path)
            else:
                # Try to load a pre-downloaded ONNX model or use color-based detection
                default_model_path = self._get_default_model_path()
                if default_model_path and os.path.exists(default_model_path):
                    self._load_onnx_model(default_model_path)
                else:
                    logging.info("No ONNX model found. Using color-based fire detection only.")
        except Exception as e:
            logging.warning(f"Could not load ONNX model: {e}. Will use color-based detection only.")
    
    def _get_default_model_path(self) -> Optional[str]:
        """Get the default ONNX model path."""
        # Check if model exists in models directory
        models_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
        os.makedirs(models_dir, exist_ok=True)
        
        model_path = os.path.join(models_dir, 'yolov8n.onnx')
        return model_path if os.path.exists(model_path) else None
    
    def _load_onnx_model(self, model_path: str):
        """
        Load ONNX model using OpenCV DNN module.
        
        Args:
            model_path: Path to ONNX model file
        """
        try:
            self.net = cv2.dnn.readNetFromONNX(model_path)
            
            # Set backend and target for optimal performance
            # Try CUDA first, fallback to CPU
            try:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                logging.info(f"Loaded ONNX model with CUDA acceleration: {model_path}")
            except:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
                logging.info(f"Loaded ONNX model with CPU: {model_path}")
            
            # Load class names (COCO dataset classes)
            self.class_names = self._get_coco_classes()
            self.model_loaded = True
            
        except Exception as e:
            logging.error(f"Error loading ONNX model: {e}")
            self.net = None
            self.model_loaded = False
    
    def _get_coco_classes(self) -> List[str]:
        """Get COCO dataset class names."""
        return [
            'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
            'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
            'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
            'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
            'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
            'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
            'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
            'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
            'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
            'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]
    
    def detect_fire_in_video(self, video_path: str) -> Dict:
        """
        Detect fire in a video recording using YOLO and color-based detection.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Dictionary containing detection results with fire presence, confidence, timestamps, and frame info
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise Exception("Could not open video file")
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            logging.info(f"Processing video: {total_frames} frames, {fps} FPS, {duration:.2f}s duration")
            
            fire_detections = []
            frame_count = 0
            frames_with_fire = 0
            
            # Process frames
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                timestamp = frame_count / fps if fps > 0 else 0
                
                # Detect fire in current frame
                fire_detected, confidence, detection_info = self._detect_fire_in_frame(frame)
                
                if fire_detected:
                    frames_with_fire += 1
                    fire_detections.append({
                        'frame': frame_count,
                        'timestamp': round(timestamp, 2),
                        'confidence': round(confidence, 3),
                        'method': detection_info.get('method', 'unknown'),
                        'details': detection_info
                    })
            
            cap.release()
            
            # Determine overall fire presence
            fire_detected_overall = frames_with_fire > 0
            fire_percentage = (frames_with_fire / frame_count * 100) if frame_count > 0 else 0
            
            # Calculate average confidence for detected frames
            avg_confidence = 0.0
            if fire_detections:
                avg_confidence = sum(d['confidence'] for d in fire_detections) / len(fire_detections)
            
            return {
                'fire_detected': fire_detected_overall,
                'confidence': round(avg_confidence, 3),
                'fire_percentage': round(fire_percentage, 2),
                'total_frames': frame_count,
                'frames_with_fire': frames_with_fire,
                'video_duration': round(duration, 2),
                'detections': fire_detections[:10],  # Return first 10 detections
                'detection_count': len(fire_detections),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error processing video for fire detection: {e}")
            raise e
    
    def _detect_fire_in_frame(self, frame: np.ndarray) -> Tuple[bool, float, Dict]:
        """
        Detect fire in a single frame using multiple methods.
        
        Args:
            frame: OpenCV frame (BGR format)
            
        Returns:
            Tuple of (fire_detected, confidence, detection_info)
        """
        # Method 1: Try ONNX model if available
        if self.model_loaded and self.net is not None:
            onnx_result = self._onnx_fire_detection(frame)
            if onnx_result[0]:
                return onnx_result
        
        # Method 2: Color-based fire detection (fallback or supplementary)
        color_result = self._color_based_fire_detection(frame)
        
        return color_result
    
    def _onnx_fire_detection(self, frame: np.ndarray) -> Tuple[bool, float, Dict]:
        """
        Use ONNX model with OpenCV DNN to detect fire/smoke in frame.
        
        Args:
            frame: OpenCV frame
            
        Returns:
            Tuple of (fire_detected, confidence, detection_info)
        """
        try:
            # Prepare input blob for YOLOv8
            # YOLOv8 expects 640x640 input
            input_size = (640, 640)
            blob = cv2.dnn.blobFromImage(
                frame, 
                scalefactor=1/255.0, 
                size=input_size, 
                swapRB=True, 
                crop=False
            )
            
            # Set input and run forward pass
            self.net.setInput(blob)
            outputs = self.net.forward()
            
            # Process YOLOv8 output
            # Output shape: [1, 84, 8400] for YOLOv8
            # First 4 values are bbox coordinates, rest are class scores
            detections = outputs[0]  # Shape: [84, 8400]
            
            # Transpose to [8400, 84]
            if len(detections.shape) == 3:
                detections = detections[0]
            detections = detections.T
            
            # Get frame dimensions
            frame_height, frame_width = frame.shape[:2]
            
            # Extract boxes and scores
            boxes = []
            confidences = []
            class_ids = []
            
            for detection in detections:
                # Get class scores (skip first 4 bbox values)
                scores = detection[4:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > self.confidence_threshold:
                    # Get bbox coordinates (center_x, center_y, width, height)
                    center_x = int(detection[0] * frame_width / input_size[0])
                    center_y = int(detection[1] * frame_height / input_size[1])
                    width = int(detection[2] * frame_width / input_size[0])
                    height = int(detection[3] * frame_height / input_size[1])
                    
                    # Convert to top-left corner coordinates
                    x = int(center_x - width / 2)
                    y = int(center_y - height / 2)
                    
                    boxes.append([x, y, width, height])
                    confidences.append(float(confidence))
                    class_ids.append(int(class_id))
            
            # Apply Non-Maximum Suppression
            indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, 0.4)
            
            # Look for fire-related objects
            fire_keywords = ['fire', 'smoke', 'flame', 'oven', 'toaster']
            max_confidence = 0.0
            fire_detections = []
            
            if len(indices) > 0:
                for i in indices.flatten():
                    class_id = class_ids[i]
                    confidence = confidences[i]
                    box = boxes[i]
                    
                    # Check if it's a fire-related class
                    class_name = self.class_names[class_id] if class_id < len(self.class_names) else 'unknown'
                    
                    # For now, we use color-based detection as primary
                    # Since COCO doesn't have fire class, we'll look for hot objects
                    if any(keyword in class_name.lower() for keyword in fire_keywords):
                        max_confidence = max(max_confidence, confidence)
                        fire_detections.append({
                            'class': class_name,
                            'confidence': confidence,
                            'bbox': box
                        })
            
            # Since COCO model doesn't have fire class, we combine with color detection
            # If we detect hot objects (oven, etc.), increase confidence
            fire_detected = max_confidence >= self.confidence_threshold
            
            return fire_detected, max_confidence, {
                'method': 'onnx_dnn',
                'detections': fire_detections,
                'note': 'COCO model - using hot objects as indicators'
            }
            
        except Exception as e:
            logging.error(f"ONNX DNN detection error: {e}")
            return False, 0.0, {'method': 'onnx_dnn', 'error': str(e)}
    
    def _color_based_fire_detection(self, frame: np.ndarray) -> Tuple[bool, float, Dict]:
        """
        Detect fire using color-based analysis (HSV color space).
        Fire typically has orange/red/yellow colors with high brightness.
        
        Args:
            frame: OpenCV frame (BGR format)
            
        Returns:
            Tuple of (fire_detected, confidence, detection_info)
        """
        try:
            # Convert to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Define fire color ranges in HSV
            # Fire typically has hue in orange/red/yellow range
            lower_fire1 = np.array([0, 50, 50])      # Red-orange lower bound
            upper_fire1 = np.array([35, 255, 255])   # Yellow upper bound
            
            lower_fire2 = np.array([160, 50, 50])    # Deep red lower bound
            upper_fire2 = np.array([180, 255, 255])  # Red upper bound
            
            # Create masks for fire colors
            mask1 = cv2.inRange(hsv, lower_fire1, upper_fire1)
            mask2 = cv2.inRange(hsv, lower_fire2, upper_fire2)
            fire_mask = cv2.bitwise_or(mask1, mask2)
            
            # Calculate percentage of fire-colored pixels
            fire_pixels = cv2.countNonZero(fire_mask)
            total_pixels = frame.shape[0] * frame.shape[1]
            fire_percentage = (fire_pixels / total_pixels) * 100
            
            # Additional check: fire should have high brightness and saturation
            # Check for bright regions in the masked area
            brightness_threshold = 150
            _, bright_mask = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 
                                          brightness_threshold, 255, cv2.THRESH_BINARY)
            combined_mask = cv2.bitwise_and(fire_mask, bright_mask)
            bright_fire_pixels = cv2.countNonZero(combined_mask)
            bright_fire_percentage = (bright_fire_pixels / total_pixels) * 100
            
            # Fire is detected if:
            # 1. Fire-colored pixels exceed threshold (0.5%)
            # 2. Bright fire pixels are present
            fire_detected = fire_percentage > 0.5 and bright_fire_percentage > 0.1
            
            # Confidence based on percentage and brightness
            confidence = min((fire_percentage * 0.1 + bright_fire_percentage * 0.2), 1.0)
            
            return fire_detected, confidence, {
                'method': 'color_based',
                'fire_percentage': round(fire_percentage, 2),
                'bright_fire_percentage': round(bright_fire_percentage, 2),
                'fire_pixels': fire_pixels,
                'total_pixels': total_pixels
            }
            
        except Exception as e:
            logging.error(f"Color-based detection error: {e}")
            return False, 0.0, {'method': 'color_based', 'error': str(e)}
    
    def save_video_from_bytes(self, video_bytes: bytes, filename: Optional[str] = None) -> str:
        """
        Save video bytes to a temporary file.
        
        Args:
            video_bytes: Video file bytes
            filename: Optional filename (will be sanitized)
            
        Returns:
            Path to saved temporary file
        """
        try:
            # Create temp directory if it doesn't exist
            temp_dir = tempfile.gettempdir()
            
            # Generate filename
            if filename:
                # Sanitize filename
                filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-', '.'))
            else:
                filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            
            temp_path = os.path.join(temp_dir, filename)
            
            # Write video bytes to file
            with open(temp_path, 'wb') as f:
                f.write(video_bytes)
            
            logging.info(f"Video saved to temporary file: {temp_path}")
            return temp_path
            
        except Exception as e:
            logging.error(f"Error saving video file: {e}")
            raise e
    
    def cleanup_temp_file(self, file_path: str):
        """
        Remove temporary file after processing.
        
        Args:
            file_path: Path to temporary file
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logging.warning(f"Could not remove temporary file {file_path}: {e}")
    
    def capture_video_from_camera(self, camera_url: str, duration_seconds: int = 15) -> Optional[str]:
        """
        Capture video from a camera stream URL for a specified duration.
        
        Args:
            camera_url: URL of the camera stream (e.g., "http://192.168.2.102:8080")
            duration_seconds: Duration of video to capture in seconds
            
        Returns:
            Path to saved video file, or None if capture failed
        """
        temp_video_path = None
        cap = None
        out = None
        
        # Common camera stream endpoints to try
        stream_endpoints = [
            camera_url,  # Try base URL first
            f"{camera_url}/video",  # IP Webcam app common endpoint
            f"{camera_url}/videofeed",  # Another common endpoint
            f"{camera_url}/mjpeg",  # MJPEG stream
            f"{camera_url}/stream",  # Generic stream endpoint
        ]
        
        # Try each endpoint until one works
        for stream_url in stream_endpoints:
            try:
                logging.info(f"Attempting to capture video from: {stream_url}")
                
                # Try to open camera stream
                cap = cv2.VideoCapture(stream_url)
                
                if cap.isOpened():
                    # Test if we can actually read a frame
                    ret, test_frame = cap.read()
                    if ret:
                        logging.info(f"✓ Successfully connected to: {stream_url}")
                        # Reset capture to beginning
                        cap.release()
                        cap = cv2.VideoCapture(stream_url)
                        break
                    else:
                        cap.release()
                        cap = None
                        logging.warning(f"✗ Could not read frame from: {stream_url}")
                else:
                    if cap:
                        cap.release()
                        cap = None
                    logging.warning(f"✗ Could not open stream: {stream_url}")
                    
            except Exception as e:
                if cap:
                    cap.release()
                    cap = None
                logging.warning(f"✗ Error trying {stream_url}: {e}")
                continue
        
        if not cap or not cap.isOpened():
            logging.error(f"Failed to open camera stream from any endpoint. Tried: {stream_endpoints}")
            return None
        
        try:
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            if fps == 0:
                fps = 30  # Default to 30 FPS if cannot detect
            
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            if width == 0 or height == 0:
                # Try to read a frame to get dimensions
                ret, frame = cap.read()
                if ret:
                    height, width = frame.shape[:2]
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to beginning
                else:
                    logging.error("Could not read frame from camera")
                    return None
            
            logging.info(f"Camera stream opened: {width}x{height} @ {fps} FPS")
            
            # Create temporary file for video
            temp_dir = tempfile.gettempdir()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_video_path = os.path.join(temp_dir, f"camera_capture_{timestamp}.mp4")
            
            # Define codec and create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))
            
            if not out.isOpened():
                logging.error("Failed to create video writer")
                return None
            
            # Calculate total frames to capture
            total_frames = fps * duration_seconds
            frames_captured = 0
            
            logging.info(f"Starting capture: {duration_seconds} seconds ({total_frames} frames)")
            
            # Capture frames
            while frames_captured < total_frames:
                ret, frame = cap.read()
                
                if not ret:
                    logging.warning(f"Failed to read frame {frames_captured}")
                    break
                
                out.write(frame)
                frames_captured += 1
                
                # Log progress every second
                if frames_captured % fps == 0:
                    logging.info(f"Captured {frames_captured}/{total_frames} frames ({frames_captured//fps}s)")
            
            logging.info(f"Video capture complete: {frames_captured} frames saved to {temp_video_path}")
            
            # Verify file was created
            if os.path.exists(temp_video_path) and os.path.getsize(temp_video_path) > 0:
                return temp_video_path
            else:
                logging.error("Video file was not created or is empty")
                return None
                
        except Exception as e:
            logging.error(f"Error capturing video from camera: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            # Release resources
            if cap is not None:
                cap.release()
            if out is not None:
                out.release()
    
    def detect_fire_from_camera_url(self, camera_url: str, duration_seconds: int = 15) -> Dict:
        """
        Capture video from camera URL and detect fire.
        
        Args:
            camera_url: URL of the camera stream
            duration_seconds: Duration of video to capture
            
        Returns:
            Dictionary with detection results
        """
        video_path = None
        
        try:
            # Capture video from camera
            logging.info(f"Starting fire detection from camera: {camera_url}")
            video_path = self.capture_video_from_camera(camera_url, duration_seconds)
            
            if not video_path:
                return {
                    'success': False,
                    'error': 'Failed to capture video from camera',
                    'camera_url': camera_url
                }
            
            # Detect fire in captured video
            detection_results = self.detect_fire_in_video(video_path)
            detection_results['success'] = True
            detection_results['camera_url'] = camera_url
            
            return detection_results
            
        except Exception as e:
            logging.error(f"Error in fire detection from camera: {e}")
            return {
                'success': False,
                'error': str(e),
                'camera_url': camera_url
            }
            
        finally:
            # Cleanup temporary video file
            if video_path:
                self.cleanup_temp_file(video_path)
    
    @staticmethod
    def detect_anomalies(data: list) -> list:
        """Detect anomalies in the provided data using a simple thresholding method."""
        anomalies = []
        for i, value in enumerate(data):
            if value > 100:  # Example threshold
                anomalies.append((i, value))
        return anomalies