"""
Example: Simple Fire Detection Client
This script demonstrates how to use the fire detection API from a client application.
"""

import requests
import time
import sys


def detect_fire_from_video(video_path, api_url="http://localhost:5000"):
    """
    Simple function to detect fire in a video file.
    
    Args:
        video_path: Path to video file
        api_url: Base URL of the API
        
    Returns:
        Dictionary with detection results
    """
    endpoint = f"{api_url}/api/v1/iotcamera/detect-fire"
    
    print(f"🎥 Analyzing video: {video_path}")
    print(f"📡 Sending to: {endpoint}")
    print("⏳ Processing...\n")
    
    try:
        # Open and upload video file
        with open(video_path, 'rb') as video_file:
            files = {'video': video_file}
            start_time = time.time()
            response = requests.post(endpoint, files=files)
            elapsed = time.time() - start_time
        
        print(f"⏱️  Processing completed in {elapsed:.2f} seconds\n")
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            
            # Print results
            print("=" * 60)
            print("                    DETECTION RESULTS")
            print("=" * 60)
            
            detection = data.get('detection_results', {})
            fire_detected = detection.get('fire_detected', False)
            
            if fire_detected:
                print("🔥 FIRE DETECTED! 🔥")
            else:
                print("✅ No fire detected")
            
            print(f"\nConfidence: {detection.get('confidence', 0):.2%}")
            print(f"Fire in {detection.get('fire_percentage', 0):.1f}% of frames")
            print(f"Duration: {detection.get('video_duration', 0):.1f}s")
            print(f"Frames analyzed: {detection.get('total_frames', 0)}")
            print(f"Frames with fire: {detection.get('frames_with_fire', 0)}")
            
            # Alert information
            alert = data.get('alert', {})
            print(f"\n{'='*60}")
            print(f"Alert Level: {alert.get('level', 'UNKNOWN')}")
            print(f"Message: {alert.get('message', '')}")
            print(f"Action: {alert.get('recommendation', '')}")
            print("=" * 60)
            
            return {
                'success': True,
                'fire_detected': fire_detected,
                'confidence': detection.get('confidence', 0),
                'alert_level': alert.get('level', 'UNKNOWN')
            }
        else:
            error_data = response.json().get('data', {})
            print(f"❌ Error: {error_data.get('error', 'Unknown error')}")
            return {
                'success': False,
                'error': error_data.get('error', 'Unknown error')
            }
            
    except FileNotFoundError:
        print(f"❌ Error: Video file not found: {video_path}")
        return {'success': False, 'error': 'File not found'}
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Cannot connect to API at {api_url}")
        print("   Make sure the server is running!")
        return {'success': False, 'error': 'Connection error'}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {'success': False, 'error': str(e)}


def main():
    """Main function - example usage"""
    
    print("\n" + "=" * 60)
    print("           FIRE DETECTION CLIENT EXAMPLE")
    print("=" * 60 + "\n")
    
    # Check if video path provided
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        print("Usage: python fire_detection_client_example.py <video_file>")
        print("\nExample:")
        print("  python fire_detection_client_example.py my_video.mp4")
        print("\nFor testing purposes, you can also edit this file and set")
        print("the video_path variable directly.\n")
        
        # Default example - change this to your video path
        video_path = "./testing/test_video.mp4"
        print(f"Using default video: {video_path}")
    
    # Detect fire
    result = detect_fire_from_video(video_path)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.get('success'):
        if result.get('fire_detected'):
            print("⚠️  ALERT: Fire was detected in the video!")
            print(f"    Confidence: {result.get('confidence', 0):.2%}")
            print(f"    Alert Level: {result.get('alert_level')}")
            print("\n⚠️  RECOMMENDED ACTIONS:")
            print("    1. Verify the area immediately")
            print("    2. Evacuate if necessary")
            print("    3. Contact emergency services (911)")
            print("    4. Do not attempt to fight large fires")
        else:
            print("✅ All clear - No fire detected")
            print("   Continue normal monitoring")
    else:
        print(f"❌ Detection failed: {result.get('error')}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
