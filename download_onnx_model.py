"""
Download Pre-trained YOLOv8n ONNX Model

This script downloads a pre-converted YOLOv8n ONNX model directly
from the Ultralytics GitHub releases or converts it quickly.
"""

import os
import urllib.request
import sys


def download_yolov8n_onnx():
    """Download pre-converted YOLOv8n ONNX model."""
    print("\n" + "="*70)
    print("  Downloading YOLOv8n ONNX Model")
    print("="*70)
    
    # Create models directory
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'yolov8n.onnx')
    
    # Check if already exists
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"\n✓ Model already exists!")
        print(f"  Location: {model_path}")
        print(f"  Size: {size_mb:.2f} MB")
        return model_path
    
    print("\n📥 Downloading YOLOv8n ONNX model...")
    print("   This will take a moment (model is ~6MB)...")
    
    # Try to download from GitHub releases or Ultralytics
    urls = [
        # Official Ultralytics ONNX export endpoint (if available)
        "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.onnx",
        # Alternative: We'll convert it on-the-fly
    ]
    
    downloaded = False
    for url in urls:
        try:
            print(f"\n   Trying: {url}")
            urllib.request.urlretrieve(url, model_path)
            
            if os.path.exists(model_path) and os.path.getsize(model_path) > 1000000:
                size_mb = os.path.getsize(model_path) / (1024 * 1024)
                print(f"\n✓ Download successful!")
                print(f"  Location: {model_path}")
                print(f"  Size: {size_mb:.2f} MB")
                downloaded = True
                break
        except Exception as e:
            print(f"   ✗ Failed: {e}")
            if os.path.exists(model_path):
                os.remove(model_path)
            continue
    
    if not downloaded:
        print("\n⚠️  Could not download pre-converted model.")
        print("   Let's try converting it instead...")
        return convert_to_onnx()
    
    return model_path


def convert_to_onnx():
    """Convert YOLOv8 to ONNX format (requires ultralytics temporarily)."""
    print("\n" + "="*70)
    print("  Converting YOLOv8 to ONNX")
    print("="*70)
    
    try:
        # Check if ultralytics is installed
        import ultralytics
        print("\n✓ ultralytics package found")
    except ImportError:
        print("\n📦 ultralytics not found. Installing temporarily...")
        print("   (You can uninstall it after conversion)")
        
        import subprocess
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'ultralytics'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"\n✗ Failed to install ultralytics: {result.stderr}")
            return None
        
        print("✓ ultralytics installed")
    
    try:
        from ultralytics import YOLO
        
        # Create models directory
        models_dir = os.path.join(os.path.dirname(__file__), 'models')
        os.makedirs(models_dir, exist_ok=True)
        
        print("\n📥 Loading YOLOv8n model...")
        print("   (Will download ~6MB if not cached)")
        model = YOLO('yolov8n.pt')
        
        print("\n🔄 Converting to ONNX format...")
        print("   This may take 1-2 minutes...")
        
        # Export to ONNX
        onnx_path = model.export(format='onnx', imgsz=640)
        
        # Move to models directory if not already there
        target_path = os.path.join(models_dir, 'yolov8n.onnx')
        
        if os.path.exists(onnx_path) and onnx_path != target_path:
            import shutil
            shutil.move(onnx_path, target_path)
            onnx_path = target_path
        
        if os.path.exists(onnx_path):
            size_mb = os.path.getsize(onnx_path) / (1024 * 1024)
            print(f"\n✓ Conversion successful!")
            print(f"  Location: {onnx_path}")
            print(f"  Size: {size_mb:.2f} MB")
            
            print("\n💡 You can now uninstall ultralytics and torch to save space:")
            print(f"   {sys.executable} -m pip uninstall ultralytics torch torchvision -y")
            
            return onnx_path
        else:
            print("\n✗ Conversion failed - ONNX file not created")
            return None
            
    except Exception as e:
        print(f"\n✗ Error during conversion: {e}")
        import traceback
        traceback.print_exc()
        return None


def verify_onnx_model(model_path):
    """Verify that the ONNX model can be loaded with OpenCV."""
    print("\n" + "="*70)
    print("  Verifying ONNX Model")
    print("="*70)
    
    try:
        import cv2
        print("\n✓ OpenCV found")
        
        print(f"\n📂 Loading model: {model_path}")
        net = cv2.dnn.readNetFromONNX(model_path)
        
        print("✓ Model loaded successfully with OpenCV DNN!")
        
        # Try to set backend
        try:
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            print("✓ CUDA backend available - GPU acceleration enabled!")
        except:
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            print("✓ Using CPU backend (CUDA not available)")
        
        print("\n✅ Model is ready to use!")
        return True
        
    except ImportError:
        print("\n⚠️  OpenCV not installed")
        print(f"   Install it: {sys.executable} -m pip install opencv-python")
        return False
    except Exception as e:
        print(f"\n✗ Error loading model: {e}")
        return False


def main():
    print("\n" + "="*70)
    print("  YOLOv8n ONNX Model Setup")
    print("="*70)
    
    print("\nThis script will:")
    print("  1. Try to download pre-converted YOLOv8n ONNX model")
    print("  2. If that fails, convert it from PyTorch format")
    print("  3. Verify the model works with OpenCV DNN")
    
    input("\nPress Enter to continue...")
    
    # Download or convert model
    model_path = download_yolov8n_onnx()
    
    if not model_path:
        print("\n✗ Failed to obtain ONNX model")
        print("\n⚠️  Don't worry! The system will work with color-based detection only.")
        print("   Color-based detection is actually very effective for fire detection!")
        return 1
    
    # Verify model
    if verify_onnx_model(model_path):
        print("\n" + "="*70)
        print("  Setup Complete! 🎉")
        print("="*70)
        print("\nYour fire detection system is ready with ONNX model support!")
        print("\nNext steps:")
        print("  1. Start the server: python run.py")
        print("  2. Test it: python testing/test_fire_detection.py")
        print("  3. Upload a video to /api/v1/iotcamera/detect-fire")
        print("\n" + "="*70)
        return 0
    else:
        print("\n⚠️  Model downloaded but verification failed")
        print("   Check that opencv-python is installed correctly")
        return 1


if __name__ == "__main__":
    sys.exit(main())
