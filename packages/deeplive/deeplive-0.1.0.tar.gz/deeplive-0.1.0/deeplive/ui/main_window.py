"""Main window for DeepLive."""

import os
import json
import webbrowser
import cv2
from typing import Callable, Tuple, Dict, Any, Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QCheckBox, 
    QComboBox, QVBoxLayout, QHBoxLayout, QFileDialog, QGridLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap

import deeplive.globals
import deeplive.metadata
from deeplive.utilities import is_image, is_video, resolve_relative_path
from deeplive.face_analyser import (
    get_one_face, get_unique_faces_from_target_image, 
    get_unique_faces_from_target_video, has_valid_map
)
from deeplive.capturer import get_video_frame
from deeplive.processors.frame.core import get_frame_processors_modules
from deeplive.gettext import LanguageManager

from deeplive.ui.constants import (
    ROOT_HEIGHT, ROOT_WIDTH, MAPPER_PREVIEW_MAX_HEIGHT, MAPPER_PREVIEW_MAX_WIDTH
)
from deeplive.ui.utils import get_available_cameras, cv2_to_qpixmap
from deeplive.ui.preview_window import PreviewWindow
from deeplive.ui.mapper_window import MapperWindow
from deeplive.ui.webcam_window import WebcamWindow


class MainWindow(QMainWindow):
    """Main application window for DeepLive."""
    
    def __init__(self, start_callback: Callable[[], None], destroy_callback: Callable[[], None], lang: str):
        super().__init__()
        
        # Store callbacks
        self.start_callback = start_callback
        self.destroy_callback = destroy_callback
        
        # Initialize language manager
        self.lang_manager = LanguageManager(lang)
        self._ = self.lang_manager._
        
        # Initialize recent directories
        self.recent_directory_source = None
        self.recent_directory_target = None
        self.recent_directory_output = None
        
        # Initialize file types
        img_ft_tuple, vid_ft_tuple = deeplive.globals.file_types
        # Convert tuple file types to strings for PyQt6 QFileDialog
        self.img_ft = self._format_filter_string(img_ft_tuple)
        self.vid_ft = self._format_filter_string(vid_ft_tuple)
        self.img_ext = self._get_default_extension(img_ft_tuple)
        self.vid_ext = self._get_default_extension(vid_ft_tuple)
        
        # Load saved switch states
        self.load_switch_states()
        
        # Initialize UI
        self.init_ui()
        
        # Initialize windows
        self.preview_window = PreviewWindow(self)
        self.mapper_window = None
        self.webcam_window = None

    def _format_filter_string(self, filter_tuple):
        """Convert a file filter tuple to a string format for QFileDialog."""
        if not filter_tuple or len(filter_tuple) < 2:
            return "All Files (*)"
            
        name, extensions = filter_tuple
        # If extensions is already a string, return it directly
        if isinstance(extensions, str):
            return extensions
            
        # If it's a tuple or list, convert it to string
        if isinstance(extensions, (tuple, list)):
            ext_string = " ".join(f"*{ext}" for ext in extensions)
            return f"{name} ({ext_string})"
            
        return "All Files (*)"
        
    def _get_default_extension(self, filter_tuple):
        """Get the default extension from a file filter tuple."""
        if not filter_tuple or len(filter_tuple) < 2:
            return ""
            
        _, extensions = filter_tuple
        
        # If extensions is a string, try to extract first extension
        if isinstance(extensions, str):
            # Extract extension from string like "Images (*.png *.jpg)"
            import re
            matches = re.findall(r"\*(\.\w+)", extensions)
            return matches[0] if matches else ""
            
        # If it's a tuple or list, get the first one
        if isinstance(extensions, (tuple, list)) and extensions:
            return extensions[0]
            
        return ""

    def init_ui(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle(f"{deeplive.metadata.name} {deeplive.metadata.version} {deeplive.metadata.edition}")
        self.setMinimumSize(ROOT_WIDTH, ROOT_HEIGHT)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Create source and target section
        source_target_layout = QHBoxLayout()
        
        # Source section
        source_section = QVBoxLayout()
        self.source_label = QLabel()
        self.source_label.setFixedSize(200, 200)
        self.source_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.source_label.setStyleSheet("border: 1px solid #ccc;")
        source_section.addWidget(self.source_label)
        
        # Target section
        target_section = QVBoxLayout()
        self.target_label = QLabel()
        self.target_label.setFixedSize(200, 200)
        self.target_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.target_label.setStyleSheet("border: 1px solid #ccc;")
        target_section.addWidget(self.target_label)
        
        # Add source and target to horizontal layout
        source_target_layout.addLayout(source_section)
        
        # Swap button in the middle
        swap_button_layout = QVBoxLayout()
        swap_button_layout.addStretch()
        swap_button = QPushButton("↔")
        swap_button.clicked.connect(self.swap_faces_paths)
        swap_button_layout.addWidget(swap_button)
        swap_button_layout.addStretch()
        source_target_layout.addLayout(swap_button_layout)
        
        source_target_layout.addLayout(target_section)
        
        # Add source/target layout to main layout
        main_layout.addLayout(source_target_layout)
        
        # Add select buttons
        select_buttons_layout = QHBoxLayout()
        
        select_face_button = QPushButton(self._("Select a face"))
        select_face_button.clicked.connect(self.select_source_path)
        select_buttons_layout.addWidget(select_face_button)
        
        select_target_button = QPushButton(self._("Select a target"))
        select_target_button.clicked.connect(self.select_target_path)
        select_buttons_layout.addWidget(select_target_button)
        
        main_layout.addLayout(select_buttons_layout)
        
        # Add options grid
        options_layout = QGridLayout()
        
        # Left column checkboxes
        self.mouth_mask_checkbox = QCheckBox(self._("Mouth Mask"))
        self.mouth_mask_checkbox.setChecked(deeplive.globals.mouth_mask)
        self.mouth_mask_checkbox.toggled.connect(
            lambda state: setattr(deeplive.globals, "mouth_mask", state)
        )
        options_layout.addWidget(self.mouth_mask_checkbox, 0, 0)
        
        self.keep_fps_checkbox = QCheckBox(self._("Keep fps"))
        self.keep_fps_checkbox.setChecked(deeplive.globals.keep_fps)
        self.keep_fps_checkbox.toggled.connect(
            lambda state: (
                setattr(deeplive.globals, "keep_fps", state), 
                self.save_switch_states()
            )
        )
        options_layout.addWidget(self.keep_fps_checkbox, 1, 0)
        
        self.keep_frames_checkbox = QCheckBox(self._("Keep frames"))
        self.keep_frames_checkbox.setChecked(deeplive.globals.keep_frames)
        self.keep_frames_checkbox.toggled.connect(
            lambda state: (
                setattr(deeplive.globals, "keep_frames", state), 
                self.save_switch_states()
            )
        )
        options_layout.addWidget(self.keep_frames_checkbox, 2, 0)
        
        self.enhancer_checkbox = QCheckBox(self._("Face Enhancer"))
        self.enhancer_checkbox.setChecked(deeplive.globals.fp_ui["face_enhancer"])
        self.enhancer_checkbox.toggled.connect(
            lambda state: (
                self.update_tumbler("face_enhancer", state), 
                self.save_switch_states()
            )
        )
        options_layout.addWidget(self.enhancer_checkbox, 3, 0)
        
        self.map_faces_checkbox = QCheckBox(self._("Map faces"))
        self.map_faces_checkbox.setChecked(deeplive.globals.map_faces)
        self.map_faces_checkbox.toggled.connect(
            lambda state: (
                setattr(deeplive.globals, "map_faces", state),
                self.save_switch_states(),
                self.close_mapper_window() if not state else None
            )
        )
        options_layout.addWidget(self.map_faces_checkbox, 4, 0)
        
        # Right column checkboxes
        self.show_mouth_mask_box_checkbox = QCheckBox(self._("Show Mouth Mask Box"))
        self.show_mouth_mask_box_checkbox.setChecked(deeplive.globals.show_mouth_mask_box)
        self.show_mouth_mask_box_checkbox.toggled.connect(
            lambda state: setattr(deeplive.globals, "show_mouth_mask_box", state)
        )
        options_layout.addWidget(self.show_mouth_mask_box_checkbox, 0, 1)
        
        self.keep_audio_checkbox = QCheckBox(self._("Keep audio"))
        self.keep_audio_checkbox.setChecked(deeplive.globals.keep_audio)
        self.keep_audio_checkbox.toggled.connect(
            lambda state: (
                setattr(deeplive.globals, "keep_audio", state), 
                self.save_switch_states()
            )
        )
        options_layout.addWidget(self.keep_audio_checkbox, 1, 1)
        
        self.many_faces_checkbox = QCheckBox(self._("Many faces"))
        self.many_faces_checkbox.setChecked(deeplive.globals.many_faces)
        self.many_faces_checkbox.toggled.connect(
            lambda state: (
                setattr(deeplive.globals, "many_faces", state), 
                self.save_switch_states()
            )
        )
        options_layout.addWidget(self.many_faces_checkbox, 2, 1)
        
        self.color_correction_checkbox = QCheckBox(self._("Fix Blueish Cam"))
        self.color_correction_checkbox.setChecked(deeplive.globals.color_correction)
        self.color_correction_checkbox.toggled.connect(
            lambda state: (
                setattr(deeplive.globals, "color_correction", state), 
                self.save_switch_states()
            )
        )
        options_layout.addWidget(self.color_correction_checkbox, 3, 1)
        
        self.show_fps_checkbox = QCheckBox(self._("Show FPS"))
        self.show_fps_checkbox.setChecked(deeplive.globals.show_fps)
        self.show_fps_checkbox.toggled.connect(
            lambda state: (
                setattr(deeplive.globals, "show_fps", state), 
                self.save_switch_states()
            )
        )
        options_layout.addWidget(self.show_fps_checkbox, 4, 1)
        
        main_layout.addLayout(options_layout)
        
        # Action buttons
        action_buttons_layout = QHBoxLayout()
        
        start_button = QPushButton(self._("Start"))
        start_button.clicked.connect(lambda: self.analyze_target())
        action_buttons_layout.addWidget(start_button)
        
        stop_button = QPushButton(self._("Destroy"))
        stop_button.clicked.connect(self.destroy_callback)
        action_buttons_layout.addWidget(stop_button)
        
        preview_button = QPushButton(self._("Preview"))
        preview_button.clicked.connect(self.toggle_preview)
        action_buttons_layout.addWidget(preview_button)
        
        main_layout.addLayout(action_buttons_layout)
        
        # Camera section
        camera_layout = QHBoxLayout()
        
        camera_label = QLabel(self._("Select Camera:"))
        camera_layout.addWidget(camera_label)
        
        # Get available cameras
        camera_indices, camera_names = get_available_cameras()
        
        self.camera_combo = QComboBox()
        self.camera_combo.addItems(camera_names)
        
        if not camera_names or camera_names[0] == "No cameras found":
            self.camera_combo.setEnabled(False)
        
        camera_layout.addWidget(self.camera_combo)
        
        live_button = QPushButton(self._("Live"))
        live_button.clicked.connect(lambda: self.webcam_preview())
        
        if not camera_names or camera_names[0] == "No cameras found":
            live_button.setEnabled(False)
            
        camera_layout.addWidget(live_button)
        
        main_layout.addLayout(camera_layout)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Donate link
        donate_label = QLabel("Deep Live Cam")
        donate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        donate_label.setStyleSheet("color: blue; text-decoration: underline;")
        donate_label.setOpenExternalLinks(True)
        donate_label.mousePressEvent = lambda event: webbrowser.open("https://deeplivecam.net")
        main_layout.addWidget(donate_label)

    def load_switch_states(self):
        """Load saved switch states from file."""
        try:
            with open("switch_states.json", "r") as f:
                switch_states = json.load(f)
            deeplive.globals.keep_fps = switch_states.get("keep_fps", True)
            deeplive.globals.keep_audio = switch_states.get("keep_audio", True)
            deeplive.globals.keep_frames = switch_states.get("keep_frames", False)
            deeplive.globals.many_faces = switch_states.get("many_faces", False)
            deeplive.globals.map_faces = switch_states.get("map_faces", False)
            deeplive.globals.color_correction = switch_states.get("color_correction", False)
            deeplive.globals.nsfw_filter = switch_states.get("nsfw_filter", False)
            deeplive.globals.live_mirror = switch_states.get("live_mirror", False)
            deeplive.globals.live_resizable = switch_states.get("live_resizable", False)
            deeplive.globals.fp_ui = switch_states.get("fp_ui", {"face_enhancer": False})
            deeplive.globals.show_fps = switch_states.get("show_fps", False)
            deeplive.globals.mouth_mask = switch_states.get("mouth_mask", False)
            deeplive.globals.show_mouth_mask_box = switch_states.get(
                "show_mouth_mask_box", False
            )
        except FileNotFoundError:
            # If the file doesn't exist, use default values
            pass

    def save_switch_states(self):
        """Save switch states to file."""
        switch_states = {
            "keep_fps": deeplive.globals.keep_fps,
            "keep_audio": deeplive.globals.keep_audio,
            "keep_frames": deeplive.globals.keep_frames,
            "many_faces": deeplive.globals.many_faces,
            "map_faces": deeplive.globals.map_faces,
            "color_correction": deeplive.globals.color_correction,
            "nsfw_filter": deeplive.globals.nsfw_filter,
            "live_mirror": deeplive.globals.live_mirror,
            "live_resizable": deeplive.globals.live_resizable,
            "fp_ui": deeplive.globals.fp_ui,
            "show_fps": deeplive.globals.show_fps,
            "mouth_mask": deeplive.globals.mouth_mask,
            "show_mouth_mask_box": deeplive.globals.show_mouth_mask_box,
        }
        with open("switch_states.json", "w") as f:
            json.dump(switch_states, f)

    def update_tumbler(self, var: str, value: bool) -> None:
        """Update a specific frame processor UI value."""
        deeplive.globals.fp_ui[var] = value
        self.save_switch_states()
        
        # If the preview window is visible, update the frame processors
        if self.preview_window.isVisible():
            self.frame_processors = get_frame_processors_modules(
                deeplive.globals.frame_processors
            )

    def update_status(self, text: str) -> None:
        """Update the status label."""
        self.status_label.setText(self._(text))

    def select_source_path(self) -> None:
        """Open file dialog to select a source image."""
        if self.preview_window.isVisible():
            self.preview_window.hide()
            
        source_path, _ = QFileDialog.getOpenFileName(
            self,
            self._("Select a source image"),
            self.recent_directory_source,
            self.img_ft
        )
        
        if is_image(source_path):
            deeplive.globals.source_path = source_path
            self.recent_directory_source = os.path.dirname(deeplive.globals.source_path)
            
            # Load and display the image
            pixmap = QPixmap(source_path)
            pixmap = pixmap.scaled(
                QSize(200, 200),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.source_label.setPixmap(pixmap)
        else:
            deeplive.globals.source_path = None
            self.source_label.clear()

    def swap_faces_paths(self) -> None:
        """Swap source and target paths."""
        source_path = deeplive.globals.source_path
        target_path = deeplive.globals.target_path

        if not is_image(source_path) or not is_image(target_path):
            return

        deeplive.globals.source_path = target_path
        deeplive.globals.target_path = source_path

        self.recent_directory_source = os.path.dirname(deeplive.globals.source_path)
        self.recent_directory_target = os.path.dirname(deeplive.globals.target_path)

        if self.preview_window.isVisible():
            self.preview_window.hide()

        # Update source image
        pixmap = QPixmap(deeplive.globals.source_path)
        pixmap = pixmap.scaled(
            QSize(200, 200),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.source_label.setPixmap(pixmap)

        # Update target image
        pixmap = QPixmap(deeplive.globals.target_path)
        pixmap = pixmap.scaled(
            QSize(200, 200),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.target_label.setPixmap(pixmap)

    def select_target_path(self) -> None:
        """Open file dialog to select a target image or video."""
        if self.preview_window.isVisible():
            self.preview_window.hide()
            
        target_path, _ = QFileDialog.getOpenFileName(
            self,
            self._("Select a target image or video"),
            self.recent_directory_target,
            f"{self.img_ft};;{self.vid_ft}"
        )
        
        if is_image(target_path):
            deeplive.globals.target_path = target_path
            self.recent_directory_target = os.path.dirname(deeplive.globals.target_path)
            
            # Load and display the image
            pixmap = QPixmap(target_path)
            pixmap = pixmap.scaled(
                QSize(200, 200),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.target_label.setPixmap(pixmap)
        elif is_video(target_path):
            deeplive.globals.target_path = target_path
            self.recent_directory_target = os.path.dirname(deeplive.globals.target_path)
            
            # Get first frame and display it
            frame = get_video_frame(target_path, 0)
            if frame is not None:
                pixmap = cv2_to_qpixmap(frame, QSize(200, 200))
                self.target_label.setPixmap(pixmap)
        else:
            deeplive.globals.target_path = None
            self.target_label.clear()

    def select_output_path(self) -> None:
        """Open file dialog to select output path."""
        if is_image(deeplive.globals.target_path):
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                self._("Save image output file"),
                os.path.join(self.recent_directory_output or "", "output.png"),
                self.img_ft,
                options=QFileDialog.Option.DontUseNativeDialog
            )
        elif is_video(deeplive.globals.target_path):
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                self._("Save video output file"),
                os.path.join(self.recent_directory_output or "", "output.mp4"),
                self.vid_ft,
                options=QFileDialog.Option.DontUseNativeDialog
            )
        else:
            output_path = None
            
        if output_path:
            # Ensure the file has the right extension
            if is_image(deeplive.globals.target_path) and not output_path.lower().endswith(self.img_ext):
                output_path += self.img_ext
            elif is_video(deeplive.globals.target_path) and not output_path.lower().endswith(self.vid_ext):
                output_path += self.vid_ext
                
            deeplive.globals.output_path = output_path
            self.recent_directory_output = os.path.dirname(deeplive.globals.output_path)
            self.start_callback()

    def toggle_preview(self) -> None:
        """Toggle preview window visibility."""
        if self.preview_window.isVisible():
            self.preview_window.hide()
        elif deeplive.globals.source_path and deeplive.globals.target_path:
            self.preview_window.init_preview()
            self.preview_window.update_preview()
            self.preview_window.show()

    def analyze_target(self) -> None:
        """Analyze target and start processing."""
        if self.mapper_window and self.mapper_window.isVisible():
            self.update_status("Please complete pop-up or close it.")
            return

        if deeplive.globals.map_faces:
            deeplive.globals.source_target_map = []

            if is_image(deeplive.globals.target_path):
                self.update_status("Getting unique faces")
                get_unique_faces_from_target_image()
            elif is_video(deeplive.globals.target_path):
                self.update_status("Getting unique faces")
                get_unique_faces_from_target_video()

            if len(deeplive.globals.source_target_map) > 0:
                self.mapper_window = MapperWindow(
                    self, 
                    deeplive.globals.source_target_map,
                    self.start_callback
                )
                self.mapper_window.show()
            else:
                self.update_status("No faces found in target")
        else:
            self.select_output_path()
            
    def close_mapper_window(self) -> None:
        """Close the mapper window if it exists."""
        if self.mapper_window and self.mapper_window.isVisible():
            self.mapper_window.close()
            self.mapper_window = None
            
        if self.webcam_window and self.webcam_window.isVisible():
            self.webcam_window.close()
            self.webcam_window = None
            
    def webcam_preview(self) -> None:
        """Open webcam preview."""
        # Get selected camera index
        camera_indices, camera_names = get_available_cameras()
        selected_camera = self.camera_combo.currentText()
        
        if selected_camera == "No cameras found":
            return
            
        camera_index = camera_indices[camera_names.index(selected_camera)]
        
        if self.webcam_window and self.webcam_window.isVisible():
            self.update_status("Webcam window is already open.")
            self.webcam_window.activateWindow()
            return

        if not deeplive.globals.map_faces:
            if deeplive.globals.source_path is None:
                self.update_status("Please select a source image first")
                return
                
            self.webcam_window = WebcamWindow(self, camera_index)
            self.webcam_window.show()
        else:
            deeplive.globals.source_target_map = []
            self.mapper_window = MapperWindow(
                self, 
                deeplive.globals.source_target_map,
                None,  # No start callback
                camera_index
            )
            self.mapper_window.show() 