from flask import Blueprint, make_response, jsonify, request
from .controller import IotcameraController


iotcamera_bp = Blueprint('iotcamera', __name__)
iotcamera_controller = IotcameraController()

@iotcamera_bp.route('/', methods=['GET'])
def index():
    """ Example endpoint with simple greeting.
    ---
    tags:
      - Camera API
    responses:
      200:
        description: A simple greeting
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                message:
                  type: string
                  example: "Hello World!"
    """
    result = iotcamera_controller.index()
    return make_response(jsonify(data=result))

@iotcamera_bp.route('/detect-fire', methods=['POST'])
def detect_fire():
    """ 
    Detect fire in uploaded video recording.
    Upload a video file (up to 100MB) to analyze for fire presence.
    ---
    tags:
      - Camera API
    consumes:
      - multipart/form-data
    parameters:
      - name: video
        in: formData
        type: file
        required: true
        description: Video file to analyze for fire detection (mp4, avi, mov, mkv, flv, wmv, webm)
    responses:
      200:
        description: Video processed successfully
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                message:
                  type: string
                  example: "Video processed successfully"
                success:
                  type: boolean
                  example: true
                file_info:
                  type: object
                  properties:
                    filename:
                      type: string
                      example: "recording.mp4"
                    size_bytes:
                      type: integer
                      example: 5242880
                    size_mb:
                      type: number
                      example: 5.0
                detection_results:
                  type: object
                  properties:
                    fire_detected:
                      type: boolean
                      example: true
                    confidence:
                      type: number
                      example: 0.85
                    fire_percentage:
                      type: number
                      example: 15.5
                    total_frames:
                      type: integer
                      example: 450
                    frames_with_fire:
                      type: integer
                      example: 70
                    video_duration:
                      type: number
                      example: 15.0
                    detection_count:
                      type: integer
                      example: 70
                alert:
                  type: object
                  properties:
                    level:
                      type: string
                      example: "HIGH"
                    message:
                      type: string
                      example: "⚠️ FIRE DETECTED! Fire present in 15.5% of frames"
                    recommendation:
                      type: string
                      example: "Immediate action required. Verify the area and contact emergency services if necessary."
      400:
        description: Bad request - missing or invalid video file
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                error:
                  type: string
                  example: "No video file provided"
                success:
                  type: boolean
                  example: false
    """
    # Check if video file is in request
    if 'video' not in request.files:
        return make_response(jsonify(data={
            'error': 'No video file provided. Please upload a file with key "video"',
            'success': False
        }), 400)
    
    video_file = request.files['video']
    
    # Check if filename is empty
    if video_file.filename == '':
        return make_response(jsonify(data={
            'error': 'No file selected',
            'success': False
        }), 400)
    
    # Process video
    result = iotcamera_controller.process_video_for_fire_detection(video_file)
    
    # Return appropriate HTTP status code based on success
    status_code = 200 if result.get('success', False) else 400
    return make_response(jsonify(data=result), status_code)

@iotcamera_bp.route('/statistics', methods=['GET'])
def statistics():
    """
    Get fire detection system statistics and information.
    ---
    tags:
      - Camera API
    responses:
      200:
        description: System statistics retrieved successfully
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                message:
                  type: string
                  example: "Fire detection system statistics"
                success:
                  type: boolean
                  example: true
                system_info:
                  type: object
                  properties:
                    model_loaded:
                      type: boolean
                      example: true
                    confidence_threshold:
                      type: number
                      example: 0.5
                    detection_methods:
                      type: array
                      items:
                        type: string
                    supported_formats:
                      type: array
                      items:
                        type: string
                    max_file_size_mb:
                      type: integer
                      example: 100
    """
    result = iotcamera_controller.get_fire_statistics()
    status_code = 200 if result.get('success', False) else 400
    return make_response(jsonify(data=result), status_code)
      