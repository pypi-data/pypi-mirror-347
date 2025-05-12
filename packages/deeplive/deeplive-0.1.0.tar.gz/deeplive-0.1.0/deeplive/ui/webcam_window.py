"""Webcam window for DeepLive."""

import cv2
import time
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QPixmap, QCloseEvent

import deeplive.globals
from deeplive.face_analyser import get_one_face
from deeplive.processors.frame.core import get_frame_processors_modules
from deeplive.video_capture import VideoCapturer
from deeplive.ui.constants import (
    PREVIEW_DEFAULT_WIDTH, PREVIEW_DEFAULT_HEIGHT
)
from deeplive.ui.utils import cv2_to_qpixmap, fit_image_to_size


class WebcamWindow(QMainWindow):
    """Window for live webcam processing."""
    
    def __init__(self, parent, camera_index: int):
        super().__init__(parent)
        self.parent = parent
        self.camera_index = camera_index
        
        # Make sure frame processors are initialized
        self.init_frame_processors()
        
        # Initialize video capturer
        self.cap = VideoCapturer(camera_index)
        
        # Set window properties
        self.setWindowTitle(self.parent._("Live Preview"))
        self.resize(PREVIEW_DEFAULT_WIDTH, PREVIEW_DEFAULT_HEIGHT)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create preview label
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.preview_label)
        
        # Initialize source image once
        self.source_image = None
        if not deeplive.globals.map_faces and deeplive.globals.source_path:
            self.load_source_face()
                
        # FPS calculation variables
        self.prev_time = time.time()
        self.fps_update_interval = 0.5
        self.frame_count = 0
        self.fps = 0
        
        # Start video capture
        if not self.cap.start(PREVIEW_DEFAULT_WIDTH, PREVIEW_DEFAULT_HEIGHT, 60):
            self.parent.update_status("Failed to start camera")
            self.close()
            return
            
        # Start timer for frame updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(16)  # ~60 FPS
    
    def init_frame_processors(self):
        """Initialize frame processors."""
        # Make sure face_swapper is in the frame processors list
        if 'face_swapper' not in deeplive.globals.frame_processors:
            deeplive.globals.frame_processors.append('face_swapper')
            
        # Initialize the frame processors
        self.frame_processors = get_frame_processors_modules(
            deeplive.globals.frame_processors
        )
        
        # Print loaded processors for debugging
        print(f"Loaded {len(self.frame_processors)} frame processors:")
        for proc in self.frame_processors:
            print(f" - {proc.__name__}")
    
    def load_source_face(self):
        """Load the source face for processing."""
        try:
            source_img = cv2.imread(deeplive.globals.source_path)
            if source_img is not None:
                self.source_image = get_one_face(source_img)
                if self.source_image:
                    print(f"Source face loaded successfully from {deeplive.globals.source_path}")
                    print(f"Source face details: {self.source_image.keys()}")
                else:
                    print(f"No face detected in the source image: {deeplive.globals.source_path}")
            else:
                print(f"Failed to load source image: {deeplive.globals.source_path}")
        except Exception as e:
            print(f"Error loading source face: {e}")
            self.source_image = None
    
    def update_frame(self):
        """Update the frame from webcam."""
        try:
            # Read frame from camera
            ret, frame = self.cap.read()
            if not ret or frame is None:
                print("Failed to read frame from camera")
                return
                
            # Make a copy of the frame to avoid modifying the original
            temp_frame = frame.copy()
            
            # Apply mirror effect if enabled
            if deeplive.globals.live_mirror:
                temp_frame = cv2.flip(temp_frame, 1)
                
            # Resize frame if needed
            if deeplive.globals.live_resizable:
                temp_frame = fit_image_to_size(
                    temp_frame, self.width(), self.height()
                )
            else:
                temp_frame = fit_image_to_size(
                    temp_frame, PREVIEW_DEFAULT_WIDTH, PREVIEW_DEFAULT_HEIGHT
                )
                
            # Check if frame is valid
            if temp_frame is None or not isinstance(temp_frame, np.ndarray):
                print("Invalid frame for processing")
                return
                
            # Process the frame
            processed_frame = self.process_frame(temp_frame)
                
            # Calculate and display FPS
            self.calculate_fps()
            if deeplive.globals.show_fps and processed_frame is not None:
                cv2.putText(
                    processed_frame,
                    f"FPS: {self.fps:.1f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )
                
            # Display the processed frame
            if processed_frame is not None:
                pixmap = cv2_to_qpixmap(processed_frame)
                self.preview_label.setPixmap(pixmap)
                
        except Exception as e:
            print(f"Error in update_frame: {e}")
    
    def process_frame(self, frame):
        """Process a single frame through all frame processors."""
        if frame is None:
            return None
            
        # Create a copy for processing
        processed = frame.copy()
        
        try:
            if not deeplive.globals.map_faces:
                # Single face swap mode
                if self.source_image is not None:
                    # Process through each frame processor
                    for processor in self.frame_processors:
                        try:
                            if hasattr(processor, 'NAME') and processor.NAME == "DLC.FACE-ENHANCER":
                                if deeplive.globals.fp_ui.get("face_enhancer", False):
                                    processed = processor.process_frame(None, processed)
                            else:
                                # This is the main face swap processor
                                processed = processor.process_frame(self.source_image, processed)
                                
                            # Print progress for debugging
                            print(f"Applied {processor.__name__} to frame")
                            
                        except Exception as e:
                            print(f"Error applying {processor.__name__}: {e}")
                else:
                    # No source face available
                    self.parent.update_status("No source face loaded - video not processed")
                    print("No source face available for processing")
            else:
                # Map faces mode (multiple face swaps)
                for processor in self.frame_processors:
                    try:
                        if hasattr(processor, 'NAME') and processor.NAME == "DLC.FACE-ENHANCER":
                            if deeplive.globals.fp_ui.get("face_enhancer", False):
                                processed = processor.process_frame_v2(processed)
                        else:
                            processed = processor.process_frame_v2(processed)
                            
                        # Print progress for debugging    
                        print(f"Applied {processor.__name__} to frame in map faces mode")
                            
                    except Exception as e:
                        print(f"Error in map faces mode with {processor.__name__}: {e}")
                        
            return processed
                
        except Exception as e:
            print(f"Error processing frame: {e}")
            return frame  # Return original frame on error
    
    def calculate_fps(self):
        """Calculate frames per second."""
        current_time = time.time()
        self.frame_count += 1
        
        if current_time - self.prev_time >= self.fps_update_interval:
            self.fps = self.frame_count / (current_time - self.prev_time)
            self.frame_count = 0
            self.prev_time = current_time
        
    def closeEvent(self, event: QCloseEvent):
        """Handle window close event."""
        # Stop the timer
        if hasattr(self, 'timer'):
            self.timer.stop()
        
        # Release the video capture
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
            
        # Accept the event to close the window
        event.accept() 