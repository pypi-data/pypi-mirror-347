#!/usr/bin/env python3

import sys
from PyQt6.QtWidgets import QApplication
from deeplive import core
from deeplive.ui import MainWindow
import deeplive.globals

def init_frame_processors():
    """Initialize required frame processors."""
    # Always include face_swapper in the frame processors list
    if 'face_swapper' not in deeplive.globals.frame_processors:
        deeplive.globals.frame_processors.append('face_swapper')
    
    # Initialize face enhancer state if needed
    if 'face_enhancer' not in deeplive.globals.fp_ui:
        deeplive.globals.fp_ui['face_enhancer'] = False

def run():
    """Run the PyQt6 application."""
    # Parse command line arguments
    core.parse_args()
    
    # Initialize required frame processors
    init_frame_processors()
    
    # Initialize the application
    app = QApplication(sys.argv)
    
    # Create the main window
    window = MainWindow(
        start_callback=core.start,
        destroy_callback=lambda: sys.exit(app.exec()),
        lang=deeplive.globals.lang
    )
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    run()
