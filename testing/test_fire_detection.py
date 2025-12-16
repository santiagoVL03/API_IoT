"""
Test script for Fire Detection Camera Endpoint

This script tests the /api/v1/iotcamera/detect-fire endpoint
with various scenarios and video files.
"""

import requests
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
FIRE_DETECTION_ENDPOINT = "/api/v1/iotcamera/detect-fire"
STATISTICS_ENDPOINT = "/api/v1/iotcamera/statistics"


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def test_statistics():
    """Test the statistics endpoint"""
    print_section("TEST 1: Get Fire Detection System Statistics")
    
    try:
        url = f"{BASE_URL}{STATISTICS_ENDPOINT}"
        print(f"Request: GET {url}")
        
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✓ Statistics retrieved successfully!")
            print(f"\nSystem Information:")
            system_info = data.get('data', {}).get('system_info', {})
            print(f"  - Model Loaded: {system_info.get('model_loaded')}")
            print(f"  - Confidence Threshold: {system_info.get('confidence_threshold')}")
            print(f"  - Max File Size: {system_info.get('max_file_size_mb')}MB")
            print(f"  - Supported Formats: {', '.join(system_info.get('supported_formats', []))}")
            print(f"\nDetection Methods:")
            for method in system_info.get('detection_methods', []):
                print(f"  - {method}")
        else:
            print(f"✗ Failed: {response.text}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def test_fire_detection_with_video(video_path, test_name):
    """Test fire detection with a video file"""
    print_section(f"TEST: {test_name}")
    
    # Check if file exists
    if not os.path.exists(video_path):
        print(f"✗ Video file not found: {video_path}")
        print(f"  Please create or provide a video file at this path to test.")
        return
    
    try:
        url = f"{BASE_URL}{FIRE_DETECTION_ENDPOINT}"
        print(f"Request: POST {url}")
        print(f"Video File: {video_path}")
        print(f"File Size: {os.path.getsize(video_path) / (1024*1024):.2f} MB")
        
        # Open and send file
        with open(video_path, 'rb') as video_file:
            files = {'video': video_file}
            response = requests.post(url, files=files)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            print("\n✓ Video processed successfully!")
            
            # File info
            file_info = data.get('file_info', {})
            print(f"\nFile Information:")
            print(f"  - Filename: {file_info.get('filename')}")
            print(f"  - Size: {file_info.get('size_mb')} MB")
            
            # Detection results
            detection = data.get('detection_results', {})
            print(f"\nDetection Results:")
            print(f"  - Fire Detected: {'YES ⚠️' if detection.get('fire_detected') else 'NO ✓'}")
            print(f"  - Confidence: {detection.get('confidence')}")
            print(f"  - Fire Percentage: {detection.get('fire_percentage')}%")
            print(f"  - Total Frames: {detection.get('total_frames')}")
            print(f"  - Frames with Fire: {detection.get('frames_with_fire')}")
            print(f"  - Video Duration: {detection.get('video_duration')}s")
            print(f"  - Detection Count: {detection.get('detection_count')}")
            
            # Alert
            alert = data.get('alert', {})
            print(f"\nAlert Information:")
            print(f"  - Level: {alert.get('level')}")
            print(f"  - Message: {alert.get('message')}")
            print(f"  - Recommendation: {alert.get('recommendation')}")
            
            # Show some detections
            detections = detection.get('detections', [])
            if detections:
                print(f"\nSample Detections (showing first {min(5, len(detections))}):")
                for i, det in enumerate(detections[:5], 1):
                    print(f"  {i}. Frame {det['frame']} @ {det['timestamp']}s - "
                          f"Confidence: {det['confidence']} - Method: {det['method']}")
        else:
            error_data = response.json().get('data', {})
            print(f"✗ Failed: {error_data.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def test_missing_video():
    """Test with missing video file"""
    print_section("TEST: Missing Video File")
    
    try:
        url = f"{BASE_URL}{FIRE_DETECTION_ENDPOINT}"
        print(f"Request: POST {url} (no video file)")
        
        response = requests.post(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            error_data = response.json().get('data', {})
            print(f"\n✓ Test PASSED - Error handled correctly")
            print(f"Error Message: {error_data.get('error')}")
        else:
            print(f"✗ Test FAILED - Expected 400 status code")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def test_invalid_file_format():
    """Test with invalid file format"""
    print_section("TEST: Invalid File Format")
    
    try:
        # Create a temporary text file
        temp_file = "temp_test.txt"
        with open(temp_file, 'w') as f:
            f.write("This is not a video file")
        
        url = f"{BASE_URL}{FIRE_DETECTION_ENDPOINT}"
        print(f"Request: POST {url}")
        print(f"File: {temp_file} (text file, not video)")
        
        with open(temp_file, 'rb') as file:
            files = {'video': file}
            response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        
        # Cleanup
        os.remove(temp_file)
        
        if response.status_code == 400:
            error_data = response.json().get('data', {})
            print(f"\n✓ Test PASSED - Invalid format rejected")
            print(f"Error Message: {error_data.get('error')}")
        else:
            print(f"✗ Test FAILED - Expected 400 status code")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        # Cleanup in case of error
        if os.path.exists("temp_test.txt"):
            os.remove("temp_test.txt")


def run_all_tests():
    """Run all test cases"""
    print("\n" + "=" * 70)
    print(" FIRE DETECTION CAMERA ENDPOINT TESTS")
    print(f" Testing: {BASE_URL}")
    print(f" Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/v1/iotcamera/")
        print(f"\n✓ Server is running (Status: {response.status_code})")
    except Exception as e:
        print(f"\n✗ Cannot connect to server: {e}")
        print("Please make sure the Flask server is running on http://localhost:5000")
        return
    
    # Run tests
    test_statistics()
    test_missing_video()
    test_invalid_file_format()
    
    # Test with actual video files if available
    print_section("VIDEO FILE TESTS")
    print("\nTo test with actual video files, place your videos in the testing directory:")
    
    test_videos = [
        ("./testing/fire_sample.mp4", "Fire Detection Test - Sample with Fire"),
        ("./testing/normal_sample.mp4", "Fire Detection Test - Normal Video"),
        ("./testing/test_video.mp4", "Fire Detection Test - Custom Video"),
    ]
    
    found_videos = False
    for video_path, test_name in test_videos:
        if os.path.exists(video_path):
            found_videos = True
            test_fire_detection_with_video(video_path, test_name)
        else:
            print(f"\n  - {video_path} (not found - skipping)")
    
    if not found_videos:
        print("\n⚠️  No test video files found.")
        print("   To test fire detection, add video files to the testing directory:")
        print("   - ./testing/fire_sample.mp4")
        print("   - ./testing/normal_sample.mp4")
        print("   - ./testing/test_video.mp4")
    
    # Final summary
    print_section("TEST SUMMARY")
    print("All automated tests completed.")
    print("For complete testing, provide actual video files.")
    print("\nHow to test with your own video:")
    print("  1. Record a 15-second video on your phone")
    print("  2. Place it in ./testing/test_video.mp4")
    print("  3. Run this script again")
    print("\nOr use curl directly:")
    print('  curl -X POST http://localhost:5000/api/v1/iotcamera/detect-fire \\')
    print('    -F "video=@your_video.mp4"')
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
