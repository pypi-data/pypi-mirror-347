"""Face mapping window for DeepLive."""

import cv2
from typing import List, Dict, Callable, Optional, Any
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, 
    QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout,
    QFileDialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap

import deeplive.globals
from deeplive.face_analyser import get_one_face, add_blank_map, has_valid_map, simplify_maps
from deeplive.utilities import is_image
from deeplive.ui.constants import (
    POPUP_WIDTH, POPUP_HEIGHT, POPUP_SCROLL_WIDTH, POPUP_SCROLL_HEIGHT,
    POPUP_LIVE_WIDTH, POPUP_LIVE_HEIGHT, POPUP_LIVE_SCROLL_WIDTH, POPUP_LIVE_SCROLL_HEIGHT,
    MAPPER_PREVIEW_MAX_HEIGHT, MAPPER_PREVIEW_MAX_WIDTH
)
from deeplive.ui.utils import cv2_to_qpixmap


class MapperWindow(QMainWindow):
    """Window for mapping source and target faces."""
    
    def __init__(self, parent, face_map: List[Dict[str, Any]], 
                 start_callback: Optional[Callable[[], None]] = None,
                 camera_index: Optional[int] = None):
        super().__init__(parent)
        self.parent = parent
        self.face_map = face_map
        self.start_callback = start_callback
        self.camera_index = camera_index
        
        # Dictionary to store image labels
        self.source_labels = {}
        self.target_labels = {}
        
        # Set window properties
        if camera_index is not None:
            self.setWindowTitle(self.parent._("Source x Target Mapper (Webcam)"))
            self.resize(POPUP_LIVE_WIDTH, POPUP_LIVE_HEIGHT)
            self.is_webcam_mode = True
        else:
            self.setWindowTitle(self.parent._("Source x Target Mapper"))
            self.resize(POPUP_WIDTH, POPUP_HEIGHT)
            self.is_webcam_mode = False
            
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Create scroll content widget
        scroll_content = QWidget()
        
        # Create grid layout for scroll content
        self.grid_layout = QGridLayout(scroll_content)
        
        # Set scroll area widget
        scroll_area.setWidget(scroll_content)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)
        
        # Add status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Add button layout
        button_layout = QHBoxLayout()
        
        # If webcam mode, add additional buttons
        if self.is_webcam_mode:
            add_button = QPushButton(self.parent._("Add"))
            add_button.clicked.connect(self.add_mapping)
            button_layout.addWidget(add_button)
            
            clear_button = QPushButton(self.parent._("Clear"))
            clear_button.clicked.connect(self.clear_mappings)
            button_layout.addWidget(clear_button)
            
            submit_button = QPushButton(self.parent._("Submit"))
            submit_button.clicked.connect(self.on_submit)
            button_layout.addWidget(submit_button)
        else:
            submit_button = QPushButton(self.parent._("Submit"))
            submit_button.clicked.connect(self.on_submit)
            button_layout.addWidget(submit_button)
        
        main_layout.addLayout(button_layout)
        
        # Setup initial faces
        if not face_map:  # If empty, add a blank mapping for webcam mode
            if self.is_webcam_mode:
                add_blank_map()
                self.face_map = deeplive.globals.source_target_map
                
        # Populate the UI
        self.refresh_ui()
    
    def refresh_ui(self):
        """Refresh the UI with current mappings."""
        # Clear existing widgets from grid
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        # Clear label dictionaries
        self.source_labels.clear()
        self.target_labels.clear()
        
        # Add face mappings
        for item in self.face_map:
            id = item["id"]
            row = id
            
            # Source button
            source_button = QPushButton(self.parent._("Select source image"))
            source_button.clicked.connect(lambda checked, idx=id: self.select_source_image(idx))
            self.grid_layout.addWidget(source_button, row, 0)
            
            # Source image placeholder
            if "source" in item:
                source_pixmap = cv2_to_qpixmap(
                    item["source"]["cv2"], 
                    QSize(MAPPER_PREVIEW_MAX_WIDTH, MAPPER_PREVIEW_MAX_HEIGHT)
                )
                source_label = QLabel(f"S-{id}")
                source_label.setPixmap(source_pixmap)
                self.grid_layout.addWidget(source_label, row, 1)
                self.source_labels[id] = source_label
            
            # X label
            x_label = QLabel("X")
            x_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(x_label, row, 2)
            
            # Target button/image
            if self.is_webcam_mode:
                target_button = QPushButton(self.parent._("Select target image"))
                target_button.clicked.connect(lambda checked, idx=id: self.select_target_image(idx))
                self.grid_layout.addWidget(target_button, row, 3)
                
                # Target image placeholder
                if "target" in item:
                    target_pixmap = cv2_to_qpixmap(
                        item["target"]["cv2"], 
                        QSize(MAPPER_PREVIEW_MAX_WIDTH, MAPPER_PREVIEW_MAX_HEIGHT)
                    )
                    target_label = QLabel(f"T-{id}")
                    target_label.setPixmap(target_pixmap)
                    self.grid_layout.addWidget(target_label, row, 4)
                    self.target_labels[id] = target_label
            else:
                # For non-webcam mode, just show the target image
                if "target" in item:
                    target_pixmap = cv2_to_qpixmap(
                        item["target"]["cv2"], 
                        QSize(MAPPER_PREVIEW_MAX_WIDTH, MAPPER_PREVIEW_MAX_HEIGHT)
                    )
                    target_label = QLabel(f"T-{id}")
                    target_label.setPixmap(target_pixmap)
                    self.grid_layout.addWidget(target_label, row, 3)
                    self.target_labels[id] = target_label
    
    def select_source_image(self, button_id: int):
        """Handle source image selection."""
        source_path, _ = QFileDialog.getOpenFileName(
            self,
            self.parent._("Select a source image"),
            self.parent.recent_directory_source,
            self.parent.img_ft
        )
        
        if not is_image(source_path):
            return
            
        # Remove existing source if any
        if "source" in self.face_map[button_id]:
            self.face_map[button_id].pop("source")
            if button_id in self.source_labels:
                self.source_labels[button_id].setParent(None)
                del self.source_labels[button_id]
        
        # Process new source image
        cv2_img = cv2.imread(source_path)
        face = get_one_face(cv2_img)
        
        if face:
            x_min, y_min, x_max, y_max = face["bbox"]
            
            # Store face in map
            self.face_map[button_id]["source"] = {
                "cv2": cv2_img[int(y_min):int(y_max), int(x_min):int(x_max)],
                "face": face,
            }
            
            # Update UI
            self.refresh_ui()
        else:
            self.update_status("Face could not be detected in last upload!")
    
    def select_target_image(self, button_id: int):
        """Handle target image selection (only for webcam mode)."""
        target_path, _ = QFileDialog.getOpenFileName(
            self,
            self.parent._("Select a target image"),
            self.parent.recent_directory_source,
            self.parent.img_ft
        )
        
        if not is_image(target_path):
            return
            
        # Remove existing target if any
        if "target" in self.face_map[button_id]:
            self.face_map[button_id].pop("target")
            if button_id in self.target_labels:
                self.target_labels[button_id].setParent(None)
                del self.target_labels[button_id]
        
        # Process new target image
        cv2_img = cv2.imread(target_path)
        face = get_one_face(cv2_img)
        
        if face:
            x_min, y_min, x_max, y_max = face["bbox"]
            
            # Store face in map
            self.face_map[button_id]["target"] = {
                "cv2": cv2_img[int(y_min):int(y_max), int(x_min):int(x_max)],
                "face": face,
            }
            
            # Update UI
            self.refresh_ui()
        else:
            self.update_status("Face could not be detected in last upload!")
    
    def add_mapping(self):
        """Add a new blank mapping row."""
        add_blank_map()
        self.face_map = deeplive.globals.source_target_map
        self.refresh_ui()
        self.update_status("Please provide mapping!")
    
    def clear_mappings(self):
        """Clear all mappings."""
        for item in self.face_map:
            if "source" in item:
                del item["source"]
            if "target" in item:
                del item["target"]
                
        # Clear UI
        self.refresh_ui()
        self.update_status("All mappings cleared!")
    
    def on_submit(self):
        """Handle submit button click."""
        if has_valid_map():
            if self.is_webcam_mode:
                simplify_maps()
                self.update_status("Mappings successfully submitted!")
                
                # Create webcam window
                from deeplive.ui.webcam_window import WebcamWindow
                webcam_window = WebcamWindow(self.parent, self.camera_index)
                webcam_window.show()
                
                # Close mapper window
                self.close()
            else:
                # For normal mode, proceed to output selection
                self.close()
                self.parent.select_output_path()
        else:
            self.update_status("At least 1 source with target is required!")
    
    def update_status(self, text: str):
        """Update status label."""
        self.status_label.setText(self.parent._(text)) 