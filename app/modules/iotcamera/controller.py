from app.utils.detection_util import DetectionUtil
from app.db.conection import db_connection
import logging
from werkzeug.datastructures import FileStorage

class IotcameraController:
    def __init__(self):
        self.db = db_connection
        self.detection_util = DetectionUtil(confidence_threshold=0.5)
        
    def index(self):
        return {'message':'Hello, World!'}
    
    def process_video_for_fire_detection(self, video_file: FileStorage) -> dict:
        """
        Process uploaded video file and detect fire.
        
        Args:
            video_file: Uploaded video file from request
            
        Returns:
            Dictionary with detection results
        """
        temp_video_path = None
        
        try:
            # Validate video file
            if not video_file:
                return {
                    'error': 'No video file provided',
                    'success': False
                }
            
            # Check file extension
            allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
            filename = video_file.filename.lower()
            
            if not any(filename.endswith(ext) for ext in allowed_extensions):
                return {
                    'error': f'Invalid file format. Allowed formats: {", ".join(allowed_extensions)}',
                    'success': False
                }
            
            # Read video bytes
            video_bytes = video_file.read()
            
            # Check file size (limit to 100MB)
            max_size = 100 * 1024 * 1024  # 100MB
            if len(video_bytes) > max_size:
                return {
                    'error': f'Video file too large. Maximum size: {max_size / (1024*1024)}MB',
                    'success': False
                }
            
            logging.info(f"Processing video file: {video_file.filename}, size: {len(video_bytes)} bytes")
            
            # Save video to temporary file
            temp_video_path = self.detection_util.save_video_from_bytes(
                video_bytes, 
                filename=video_file.filename
            )
            
            # Perform fire detection
            detection_results = self.detection_util.detect_fire_in_video(temp_video_path)
            
            # Prepare response
            response = {
                'message': 'Video processed successfully',
                'success': True,
                'file_info': {
                    'filename': video_file.filename,
                    'size_bytes': len(video_bytes),
                    'size_mb': round(len(video_bytes) / (1024 * 1024), 2)
                },
                'detection_results': detection_results
            }
            
            # Add alert if fire detected
            if detection_results.get('fire_detected'):
                response['alert'] = {
                    'level': 'HIGH' if detection_results['fire_percentage'] > 10 else 'MEDIUM',
                    'message': f"⚠️ FIRE DETECTED! Fire present in {detection_results['fire_percentage']:.1f}% of frames",
                    'recommendation': 'Immediate action required. Verify the area and contact emergency services if necessary.'
                }
            else:
                response['alert'] = {
                    'level': 'LOW',
                    'message': 'No fire detected in the video',
                    'recommendation': 'Continue monitoring. System is operational.'
                }
            
            return response
            
        except Exception as e:
            logging.error(f"Error processing video for fire detection: {e}")
            return {
                'error': f'Failed to process video: {str(e)}',
                'success': False
            }
        
        finally:
            # Cleanup temporary file
            if temp_video_path:
                self.detection_util.cleanup_temp_file(temp_video_path)
    
    def get_fire_statistics(self) -> dict:
        """
        Get statistics about fire detection system.
        
        Returns:
            Dictionary with system statistics
        """
        try:
            return {
                'message': 'Fire detection system statistics',
                'success': True,
                'system_info': {
                    'model_loaded': self.detection_util.model_loaded,
                    'confidence_threshold': self.detection_util.confidence_threshold,
                    'detection_methods': [
                        'YOLO-based object detection',
                        'Color-based fire detection (HSV analysis)',
                        'Brightness and saturation analysis'
                    ],
                    'supported_formats': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'],
                    'max_file_size_mb': 100,
                    'recommended_duration': '10-30 seconds'
                }
            }
        except Exception as e:
            logging.error(f"Error getting fire statistics: {e}")
            return {
                'error': f'Failed to get statistics: {str(e)}',
                'success': False
            }
