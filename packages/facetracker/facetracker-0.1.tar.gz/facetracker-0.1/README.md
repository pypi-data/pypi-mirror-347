# FaceTracker

A lightweight face recognition package with live exportable recognition state. Use it as a library or CLI tool.

## Usage

```bash
pip install facetracker

from facetracker import start_recognition, recognized_people

start_recognition()

while True:
    print("Current:", recognized_people)

---

### ✅ Install Locally for Testing
```bash
pip install -e .