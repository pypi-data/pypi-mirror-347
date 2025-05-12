"""UI utilities for DeepLive."""

import os
import cv2
import numpy as np
from typing import Tuple, List, Optional
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QSize, Qt

import platform
from deeplive.face_analyser import get_one_face


def get_available_cameras() -> Tuple[List[int], List[str]]:
    """Returns a list of available camera indices and names."""
    if platform.system() == "Windows":
        try:
            from pygrabber.dshow_graph import FilterGraph
            graph = FilterGraph()
            devices = graph.get_input_devices()

            # Create list of indices and names
            camera_indices = list(range(len(devices)))
            camera_names = devices

            # If no cameras found through DirectShow, try OpenCV fallback
            if not camera_names:
                # Try to open camera with index -1 and 0
                test_indices = [-1, 0]
                working_cameras = []

                for idx in test_indices:
                    cap = cv2.VideoCapture(idx)
                    if cap.isOpened():
                        working_cameras.append(f"Camera {idx}")
                        cap.release()

                if working_cameras:
                    return test_indices[:len(working_cameras)], working_cameras

            # If still no cameras found, return empty lists
            if not camera_names:
                return [], ["No cameras found"]

            return camera_indices, camera_names

        except Exception as e:
            print(f"Error detecting cameras: {str(e)}")
            return [], ["No cameras found"]
    else:
        # Unix-like systems (Linux/Mac) camera detection
        camera_indices = []
        camera_names = []

        if platform.system() == "Darwin":  # macOS specific handling
            # Try to open the default FaceTime camera first
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                camera_indices.append(0)
                camera_names.append("FaceTime Camera")
                cap.release()

            # On macOS, additional cameras typically use indices 1 and 2
            for i in [1, 2]:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    camera_indices.append(i)
                    camera_names.append(f"Camera {i}")
                    cap.release()
        else:
            # Linux camera detection - test first 10 indices
            for i in range(10):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    camera_indices.append(i)
                    camera_names.append(f"Camera {i}")
                    cap.release()

        if not camera_names:
            return [], ["No cameras found"]

        return camera_indices, camera_names


def cv2_to_qpixmap(cv_img: np.ndarray, target_size: Optional[QSize] = None) -> QPixmap:
    """Convert a CV2 image to QPixmap."""
    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    
    # Create QImage from the RGB image
    q_img = QImage(rgb_image.data, w, h, w * ch, QImage.Format.Format_RGB888)
    
    # Convert to QPixmap
    pixmap = QPixmap.fromImage(q_img)
    
    # Resize if needed
    if target_size:
        pixmap = pixmap.scaled(target_size, 
                              Qt.AspectRatioMode.KeepAspectRatio, 
                              Qt.TransformationMode.SmoothTransformation)
    
    return pixmap


def fit_image_to_size(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """Resize an image to fit within the specified dimensions while preserving aspect ratio."""
    if width is None or height is None or width <= 0 or height <= 0:
        return image
    
    h, w, _ = image.shape
    ratio_w = width / w
    ratio_h = height / h
    
    # Use the smaller ratio to ensure the image fits within the given dimensions
    ratio = min(ratio_w, ratio_h)
    
    # Compute new dimensions, ensuring they're at least 1 pixel
    new_width = max(1, int(ratio * w))
    new_height = max(1, int(ratio * h))
    
    return cv2.resize(image, (new_width, new_height)) 