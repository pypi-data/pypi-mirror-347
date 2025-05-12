"""Preview window for DeepLive."""

import cv2
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QSlider, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage

import deeplive.globals
from deeplive.face_analyser import get_one_face
from deeplive.capturer import get_video_frame, get_video_frame_total
from deeplive.processors.frame.core import get_frame_processors_modules
from deeplive.utilities import is_image, is_video
from deeplive.ui.constants import (
    PREVIEW_MAX_HEIGHT, PREVIEW_MAX_WIDTH
)
from deeplive.ui.utils import cv2_to_qpixmap


class PreviewWindow(QMainWindow):
    """Preview window for images and videos."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.setWindowTitle(self.parent._("Preview"))
        self.resize(PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create preview label
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.preview_label)
        
        # Create slider for videos
        self.preview_slider = QSlider(Qt.Orientation.Horizontal)
        self.preview_slider.setMinimum(0)
        self.preview_slider.setMaximum(0)
        self.preview_slider.valueChanged.connect(self.slider_value_changed)
        layout.addWidget(self.preview_slider)
        self.preview_slider.hide()
        
        # Hide window by default
        self.hide()
    
    def slider_value_changed(self, value):
        """Handle slider value change event."""
        self.update_preview(value)
    
    def init_preview(self):
        """Initialize preview contents based on target type."""
        if is_image(deeplive.globals.target_path):
            self.preview_slider.hide()
        elif is_video(deeplive.globals.target_path):
            video_frame_total = get_video_frame_total(deeplive.globals.target_path)
            self.preview_slider.setMaximum(video_frame_total - 1)
            self.preview_slider.setValue(0)
            self.preview_slider.show()
    
    def update_preview(self, frame_number: int = 0):
        """Update preview with processed frame."""
        if not (deeplive.globals.source_path and deeplive.globals.target_path):
            return
            
        self.parent.update_status("Processing...")
        
        # Get frame from target
        if is_image(deeplive.globals.target_path):
            temp_frame = cv2.imread(deeplive.globals.target_path)
        else:
            temp_frame = get_video_frame(deeplive.globals.target_path, frame_number)
        
        if temp_frame is None:
            self.parent.update_status("Failed to load frame")
            return
            
        # Check NSFW if enabled
        if deeplive.globals.nsfw_filter and self.check_and_ignore_nsfw(temp_frame):
            return
            
        # Apply frame processors
        source_face = get_one_face(cv2.imread(deeplive.globals.source_path))
        for frame_processor in get_frame_processors_modules(deeplive.globals.frame_processors):
            temp_frame = frame_processor.process_frame(source_face, temp_frame)
            
        # Display the result
        pixmap = cv2_to_qpixmap(temp_frame, QSize(PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT))
        self.preview_label.setPixmap(pixmap)
            
        self.parent.update_status("Processing succeed!")
    
    def check_and_ignore_nsfw(self, target):
        """Check if target is NSFW and should be ignored."""
        # Import prediction function
        from deeplive.predicter import predict_frame
        
        if predict_frame(target):
            self.parent.update_status("Processing ignored (NSFW content)!")
            return True
        
        return False
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.hide()
        event.ignore()  # Prevent actual window destruction 