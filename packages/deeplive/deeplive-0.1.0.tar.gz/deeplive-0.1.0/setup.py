#!/usr/bin/env python3

from setuptools import setup, find_packages

# Core dependencies
install_requires = [
    "numpy>=1.23.5,<2",
    "typing-extensions>=4.8.0",
    "opencv-python==4.10.0.84",
    "cv2_enumerate_cameras==1.1.15",
    "onnx==1.16.0",
    "insightface==0.7.3",
    "psutil==5.9.8",
    "PyQt6>=6.5.0",
    "pillow==11.1.0",
    "protobuf==4.23.2",
    "opennsfw2==0.10.2",
]

# Platform-specific dependencies
install_requires.extend([
    "torch==2.5.1; sys_platform == 'darwin'",
    "torchvision==0.20.1; sys_platform == 'darwin'",
    "onnxruntime-silicon==1.16.3; sys_platform == 'darwin' and platform_machine == 'arm64'",
])

# CUDA-specific dependencies
install_requires.extend([
    "torch==2.5.1; sys_platform != 'darwin'",
    "torchvision==0.20.1; sys_platform != 'darwin'",
    "onnxruntime-gpu==1.16.3; sys_platform != 'darwin'",
    "tensorflow; sys_platform != 'darwin'",
])

# Define extra index URL for PyTorch CUDA builds
extra_index_urls = [
    "https://download.pytorch.org/whl/cu118"
]

setup(
    name="deeplive",
    version="0.1.0",
    description="Transform Reality in Real-Time: Instant Face Swap Technology with Just One Image. Create Stunning Live Deepfakes with Audio - No Training Required!",
    long_description="DeepLive lets you instantly transform videos and livestreams with revolutionary one-click face swap technology. Using just a single reference image, seamlessly replace faces in real-time while preserving audio quality. Perfect for content creators, streamers, and entertainment professionals seeking to create engaging, high-quality digital transformations without complex training.",
    author="DeepLive Team",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extra_index_urls=extra_index_urls,
    entry_points={
        'console_scripts': [
            'deeplive=deeplive.app:run',
        ],
    },
    python_requires='>=3.9',
)