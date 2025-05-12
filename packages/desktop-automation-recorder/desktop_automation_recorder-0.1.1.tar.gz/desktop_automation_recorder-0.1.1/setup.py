from setuptools import setup, find_packages

setup(
    name="desktop-automation-recorder",
    version="0.1.1",
    description="A user-friendly desktop application to record and replay user interactions",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["assets/*"],
    },
    install_requires=[
        "pyautogui",
        "pynput",
        "pillow",
        "pyperclip",
        "PyQt6",
    ],
    entry_points={
        "console_scripts": [
            "desktop-automation-recorder=desktop_automation_recorder.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 