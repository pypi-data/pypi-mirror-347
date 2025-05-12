#!/usr/bin/env python3

"""Test script to verify face_swapper is working properly."""

import sys
import cv2
import numpy as np
import importlib
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deeplive.face_analyser import get_one_face
import deeplive.globals

def test_face_swap():
    """Test face swapping functionality."""
    print("Testing face swapper module...")
    
    # Set frame processors
    deeplive.globals.frame_processors = ['face_swapper']
    
    # Try to load the face_swapper module
    try:
        face_swapper = importlib.import_module('deeplive.processors.frame.face_swapper')
        print("Successfully imported face_swapper module")
        
        # Load test images (you need to provide a source and target image path)
        if len(sys.argv) < 3:
            print("Usage: python test_face_swap.py source_image.jpg target_image.jpg")
            sys.exit(1)
            
        source_path = sys.argv[1]
        target_path = sys.argv[2]
        
        # Load the source image and get face
        print(f"Loading source face from: {source_path}")
        source_img = cv2.imread(source_path)
        if source_img is None:
            print(f"ERROR: Could not load source image from {source_path}")
            sys.exit(1)
            
        source_face = get_one_face(source_img)
        if source_face is None:
            print("ERROR: No face detected in source image")
            sys.exit(1)
            
        print("Source face detected successfully")
        
        # Load the target image
        print(f"Loading target image from: {target_path}")
        target_img = cv2.imread(target_path)
        if target_img is None:
            print(f"ERROR: Could not load target image from {target_path}")
            sys.exit(1)
            
        # Process the frame
        print("Processing frame...")
        try:
            result = face_swapper.process_frame(source_face, target_img)
            print("Face swapping completed successfully")
            
            # Save the result
            output_path = "face_swap_test_result.jpg"
            cv2.imwrite(output_path, result)
            print(f"Result saved to: {output_path}")
            
        except Exception as e:
            print(f"ERROR in face swapper processing: {e}")
            import traceback
            traceback.print_exc()
            
    except ImportError as e:
        print(f"ERROR: Could not import face_swapper module: {e}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_face_swap() 