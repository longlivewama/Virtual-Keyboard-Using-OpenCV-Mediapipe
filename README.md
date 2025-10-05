
# Virtual Hand Keyboard using OpenCV & MediaPipe

![Demo](Screenshot%202025-10-05%20213953.png)

This project implements a virtual keyboard controlled by hand gestures using a webcam.
It uses MediaPipe Hands for real-time hand tracking and OpenCV for visualization.
You can type by moving your index finger over virtual keys and tapping with a simple gesture — no physical keyboard needed.

---

## Abstract

The goal of this project is to create a vision-based virtual keyboard that allows users to type through hand gestures instead of a physical device.
Using MediaPipe’s hand tracking and OpenCV’s image processing, this system detects finger movements, recognizes gestures, and translates them into virtual key presses in real time.

---

## Features

* Real-time hand tracking using MediaPipe Hands
* Full-screen virtual keyboard interface
* Tap gesture detection for key presses
* Support for Shift, Caps, Space, Enter, and Delete
* Transparent keyboard overlay (so the user remains visible)
* Saves typed text to `typed_output.txt`
* Works smoothly on standard webcams

---

## Tools & Technologies

| Tool      | Version | Description                                 |
| :-------- | :------ | :------------------------------------------ |
| Python    | 3.11    | Programming language                        |
| OpenCV    | ≥ 4.5   | Image processing and visualization          |
| MediaPipe | ≥ 0.8   | Real-time hand tracking                     |
| NumPy     | Latest  | Numerical operations and coordinate mapping |

**Project Date:** October 2025

---

## System Architecture

1. Capture webcam input
2. Detect hand landmarks using MediaPipe Hands
3. Identify index and middle finger positions
4. Detect tap gestures based on finger distance
5. Map coordinates to corresponding on-screen keys
6. Display the pressed key and append it to the output

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YourUsername/virtual-hand-keyboard.git
cd virtual-hand-keyboard
```

### 2. Install dependencies

```bash
pip install opencv-python mediapipe numpy
```

### 3. Run the project

```bash
python virtual_keyboard.py
```

---

## Controls

| Action            | Description            |
| :---------------- | :--------------------- |
| Move index finger | Hover over a key       |
| Tap gesture       | Press a key            |
| Caps / Shift      | Toggle uppercase       |
| Space             | Adds a space           |
| Delete            | Removes last character |
| Enter             | Saves line to file     |
| Q (keyboard)      | Quit manually          |

---

## Author

**Ahmed Fahim**
Faculty of Artificial Intelligence – Data Science Major

LinkedIn: [www.linkedin.com/in/longlivewama](https://www.linkedin.com/in/longlivewama)
