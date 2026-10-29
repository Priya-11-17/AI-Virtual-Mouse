# AI Virtual Mouse Using Hand Gestures

An AI-powered virtual mouse application developed using
Python, OpenCV, MediaPipe, PyAutoGUI, and Flask.

## Features

- Real-time hand tracking
- Cursor movement using index finger
- Left-click using thumb and index finger
- Right-click using thumb and middle finger
- Scrolling using two fingers
- Flask-based web interface
- FPS display

## Technologies

- Python
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI
- Flask
- HTML
- CSS
- JavaScript

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download the MediaPipe Hand Landmarker model and place
it in the models folder as hand_landmarker.task.

## Run the Python Application

```bash
python main.py
```

## Run the Web Application

```bash
python app.py
```

Open the local address displayed in the terminal.

## Gesture Controls

| Gesture | Action |
|---|---|
| Index finger raised | Move cursor |
| Thumb + index pinch | Left-click |
| Thumb + middle pinch | Right-click |
| Index + middle raised | Scroll |
| Q key | Exit |

## Future Improvements

- Gesture sensitivity settings
- Drag-and-drop support
- Better scroll controls
- Gesture calibration
- Multi-hand detection

## Project Type

Computer Vision / AI / Human-Computer Interaction